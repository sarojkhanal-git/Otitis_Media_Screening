import io
import os
import base64
import torch
import torch.nn.functional as F
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from monai.transforms import LoadImage, EnsureChannelFirst, Resize, NormalizeIntensity
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
import numpy as np
from PIL import Image

from fastapi.middleware.cors import CORSMiddleware

# ------------------------
# Config
# ------------------------
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASS_NAMES_STAGE1 = ["Normal", "Abnormal", "Earwax"]
CLASS_NAMES_STAGE2 = ["AOM", "COM"]

MODEL_STAGE1_PATH = "3OM_86_mobilenet_model.pth"
MODEL_STAGE2_PATH = "AOM_COM_MODEL.pth"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------
# Load Models
# ------------------------
model_stage1 = torch.load(MODEL_STAGE1_PATH, map_location=DEVICE)
model_stage1.eval()
target_layers_stage1 = [model_stage1.features[-1]]

model_stage2 = torch.load(MODEL_STAGE2_PATH, map_location=DEVICE)
model_stage2.eval()
target_layers_stage2 = [model_stage2.features[-1]]

# ------------------------
# Preprocessing
# ------------------------
def preprocess_image(image_bytes):
    # Open with PIL directly from bytes
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img_np = np.array(pil_img)

    # Make channels-first (C, H, W)
    img = np.transpose(img_np, (2, 0, 1))

    # MONAI transforms but applied to numpy arrays
    img = Resize((500, 500))(img)
    img = NormalizeIntensity()(img)

    # To tensor
    img_tensor = torch.tensor(img, dtype=torch.float).unsqueeze(0).to(DEVICE)

    return img, img_tensor  # img is (C,H,W) numpy, used for visualization



# ------------------------
# Grad-CAM Generator
# ------------------------
def generate_gradcam(model, target_layers, input_tensor, orig_img_np):
    cam = GradCAM(model=model, target_layers=target_layers)
    grayscale_cam = cam(input_tensor=input_tensor)[0, :]
    orig_img_norm = (orig_img_np - orig_img_np.min()) / (orig_img_np.max() - orig_img_np.min())
    overlay = show_cam_on_image(orig_img_norm.astype(np.float32), grayscale_cam, use_rgb=True)
    return overlay

def encode_image_to_base64(img_np):
    pil_img = Image.fromarray(img_np.astype(np.uint8))
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def save_overlay_to_disk(img_np, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    Image.fromarray(img_np.astype(np.uint8)).save(path)
    return path

# ------------------------
# Referral Logic
# ------------------------
def get_referral(stage1_class, stage1_confidence):
    if stage1_class == "Abnormal":
        return "Urgent"
    elif stage1_class in ["Normal", "Earwax"] and stage1_confidence < 0.70:
        return "Routine"
    else:
        return "No Referral"

# ------------------------
# FastAPI App
# ------------------------
app = FastAPI(title="EarScope API", description="Otitis Media Screening with Grad-CAM")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend at http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

# ------------------------
# Single Prediction
# ------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    orig_img, img_tensor = preprocess_image(contents)


    # Stage 1 inference
    with torch.no_grad():
        outputs1 = model_stage1(img_tensor)
        probs1 = F.softmax(outputs1, dim=1).detach().cpu().numpy().flatten()
        pred1 = int(np.argmax(probs1))
        stage1_class = CLASS_NAMES_STAGE1[pred1]
        stage1_conf = float(probs1[pred1])

    referral = get_referral(stage1_class, stage1_conf)

    result = {
        "stage1_prediction": stage1_class,
        "stage1_probabilities": {cls: float(p) for cls, p in zip(CLASS_NAMES_STAGE1, probs1)},
        "referral": referral
    }

    # Always generate heatmap
    if stage1_class == "Abnormal":
        # Stage 2 inference
        with torch.no_grad():
            outputs2 = model_stage2(img_tensor)
            probs2 = F.softmax(outputs2, dim=1).detach().cpu().numpy().flatten()
            pred2 = int(np.argmax(probs2))
            stage2_class = CLASS_NAMES_STAGE2[pred2]

        overlay = generate_gradcam(model_stage2, target_layers_stage2, img_tensor, np.transpose(orig_img, (1, 2, 0)))
        overlay_b64 = encode_image_to_base64(overlay)

        result["stage2_prediction"] = stage2_class
        result["stage2_probabilities"] = {cls: float(p) for cls, p in zip(CLASS_NAMES_STAGE2, probs2)}
        result["gradcam"] = overlay_b64

    else:
        overlay = generate_gradcam(model_stage1, target_layers_stage1, img_tensor, np.transpose(orig_img, (1, 2, 0)))
        overlay_b64 = encode_image_to_base64(overlay)
        result["gradcam"] = overlay_b64

    return JSONResponse(content=result)

# ------------------------
# Batch Prediction
# ------------------------
# ------------------------
# Batch Prediction
# ------------------------
@app.post("/batch_predict")
async def batch_predict(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        orig_img, img_tensor = preprocess_image(contents)

        # Stage 1
        with torch.no_grad():
            outputs1 = model_stage1(img_tensor)
            probs1 = F.softmax(outputs1, dim=1).detach().cpu().numpy().flatten()
            pred1 = int(np.argmax(probs1))
            stage1_class = CLASS_NAMES_STAGE1[pred1]
            stage1_conf = float(probs1[pred1])

        referral = get_referral(stage1_class, stage1_conf)

        # Encode original image to base64
        orig_img_np = np.transpose(orig_img, (1, 2, 0))  # (H,W,C)
        orig_img_b64 = encode_image_to_base64(orig_img_np)

        result = {
            "filename": file.filename,
            "stage1_prediction": stage1_class,
            "stage1_probabilities": {cls: float(p) for cls, p in zip(CLASS_NAMES_STAGE1, probs1)},
            "referral": referral,
            "confidence": stage1_conf,
            "original_image": orig_img_b64  # <-- ADDED
        }

        # Stage 2 if abnormal
        if stage1_class == "Abnormal":
            with torch.no_grad():
                outputs2 = model_stage2(img_tensor)
                probs2 = F.softmax(outputs2, dim=1).detach().cpu().numpy().flatten()
                pred2 = int(np.argmax(probs2))
                stage2_class = CLASS_NAMES_STAGE2[pred2]
                stage2_conf = float(probs2[pred2])

            overlay = generate_gradcam(model_stage2, target_layers_stage2, img_tensor, orig_img_np)
            overlay_path = save_overlay_to_disk(overlay, f"{file.filename}_gradcam.png")

            result["stage2_prediction"] = stage2_class
            result["stage2_probabilities"] = {cls: float(p) for cls, p in zip(CLASS_NAMES_STAGE2, probs2)}
            result["stage2_confidence"] = stage2_conf
            result["gradcam_url"] = f"/outputs/{os.path.basename(overlay_path)}"

        else:
            overlay = generate_gradcam(model_stage1, target_layers_stage1, img_tensor, orig_img_np)
            overlay_path = save_overlay_to_disk(overlay, f"{file.filename}_gradcam.png")
            result["gradcam_url"] = f"/outputs/{os.path.basename(overlay_path)}"

        results.append(result)

    return JSONResponse(content={"results": results})



"""
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Serve static frontend files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")
"""


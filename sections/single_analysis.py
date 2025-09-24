import streamlit as st
import requests
import base64
import io
from PIL import Image
from utils.api_client import API_URL
from sections.batch_processing import create_pdf_report
from datetime import datetime


def render():
    st.markdown(
        """
        <style>
        /* ===== Global Background & Font ===== */
        div[data-testid="stAppViewContainer"] {
            background-color: #f8faff; /* light background */
            font-family: 'Segoe UI', sans-serif;
        }

        /* ===== Header Styling ===== */
        div[data-testid="stHeader"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 12px;
        }
        div[data-testid="stHeader"] h1 {
            color: white !important;
            font-size: 2.5rem !important;
            font-weight: 700;
        }

        /* ===== File Uploader ===== */
        /* ===== File Uploader (Square Box) ===== */
        div[data-testid="stFileUploader"] > section {
            border: 3px dashed #667eea !important;
            border-radius: 16px !important;
            background: #f0f4ff !important;
            width: 350px !important;   /* adjust width */
            height: 350px !important;  /* adjust height (same as width for square) */
            margin: 0 auto !important; /* center horizontally */
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            position: relative !important;
        }

        /* Hover effect */
        div[data-testid="stFileUploader"] > section:hover {
            border-color: #764ba2 !important;
            background: #e6eaff !important;
            transform: translateY(-3px) !important;
        }

        /* Hide all default inner elements */
        div[data-testid="stFileUploader"] > section * {
            display: none !important;
        }

        /* Custom text inside */
        div[data-testid="stFileUploader"] > section::before {
            content: "📤 Drag & Drop Image Here Or Click to Browse";
            color: #667eea;
            font-size: 1.5rem;
            font-weight: 700;
            display: block;
            margin-bottom: 1rem;
        }

        div[data-testid="stFileUploader"] > section::after {
            content: "Supported formats: JPG, JPEG, PNG, TIFF";
            color: #666;
            font-size: 1rem;
            display: block;
        }




        /* ===== Results / Cards ===== */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }

        .prediction-badge {
            display: inline-block;
            padding: 0.5rem 1.2rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1rem;
            margin: 0.5rem 0;
        }

        .normal {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }

        .abnormal {
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            color: white;
        }

        .earwax {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #333;
        }

        .aom {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            color: white;
        }

        .com {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }

        /* ===== Progress/Confidence Bar ===== */
        .confidence-bar {
            background: #e0e6ff;
            border-radius: 10px;
            height: 20px;
            margin: 0.5rem 0;
            overflow: hidden;
        }
        .confidence-fill {
            height: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.6s ease;
        }

        /* ===== Analyze Button ===== */
        .analyze-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .analyze-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # Header Section
    st.markdown("""
    <div class="main-header">
        <h1>🔬 Single Image Analysis</h1>
        <p>Upload an image for AI analysis</p>
    </div>
    """, unsafe_allow_html=True)

    if "single_result" not in st.session_state:
        st.session_state.single_result = None

    # Upload Section - Clean single drag and drop
    file = st.file_uploader("",
                            type=["jpg", "jpeg", "png", "tiff", "tif", "webp"],
                            key="single_file",
                            label_visibility="collapsed")

    # Auto-analyze when file is uploaded
    if file:
        # Automatically run analysis when file is uploaded
        if st.session_state.get("last_uploaded_file") != file.name:
            st.session_state.last_uploaded_file = file.name
            with st.spinner('🔄 Analyzing image... This may take a few moments'):
                files = {"file": (file.name, file, "multipart/form-data")}
                try:
                    response = requests.post(f"{API_URL}/predict", files=files, timeout=30)
                    if response.status_code == 200:
                        st.session_state.single_result = response.json()
                        st.success("✅ Analysis completed successfully!")
                    else:
                        st.error(f"❌ Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"🚫 API connection failed: {e}")
        
        # Display images side by side
        col1, col2 = st.columns([1, 1], gap="medium")
        
        with col1:
            st.markdown("##### Original Image")
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(file, width=400)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("##### Explainability Heatmap")
            if st.session_state.single_result and "gradcam" in st.session_state.single_result:
                result = st.session_state.single_result
                heatmap_data = base64.b64decode(result["gradcam"])
                heatmap_img = Image.open(io.BytesIO(heatmap_data))
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(heatmap_img, width=400)
                st.markdown('</div>', unsafe_allow_html=True)
                st.caption("Shows regions that influenced the model's descision.")
            else:
                st.markdown("""
                <div style="background: #f8faff; padding: 3rem; border-radius: 12px; text-align: center; border: 2px dashed #e0e6ff;">
                    <h3 style="color: #667eea; margin-bottom: 1rem;">🔍 Processing...</h3>
                    <p style="color: #666; font-size: 1.1rem;">Generating heatmap analysis</p>
                </div>
                """, unsafe_allow_html=True)

    # Results Section
    if st.session_state.single_result:
        result = st.session_state.single_result

        st.markdown("---")
        st.markdown("### 📊 Diagnostic Results")

        # === Primary Classification ===
        prediction = result.get("stage1_prediction", "Unknown")
        probs = result.get("stage1_probabilities", {})
        confidence = probs.get(prediction, None)
        confidence_percent = confidence * 100 if confidence is not None else 0

        st.markdown(f"""
        <div class="metric-card">
            <h4>🎯 Primary Classification</h4>
            <div class="prediction-badge {prediction.lower()}">{prediction}</div>
            <p><b>Confidence Level</b></p>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: {confidence_percent}%"></div>
            </div>
            <p style="margin: 0.5rem 0; font-weight: 600; color: #667eea;">
                {confidence_percent:.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

        # === Secondary Classification (only if available) ===
        if "stage2_prediction" in result:
            stage2_pred = result["stage2_prediction"]
            stage2_probs = result.get("stage2_probabilities", {})
            stage2_conf = stage2_probs.get(stage2_pred, None)
            stage2_confidence_percent = stage2_conf * 100 if stage2_conf is not None else 0

            st.markdown(f"""
            <div class="metric-card">
                <h4>🔬 Secondary Classification</h4>
                <div class="prediction-badge {stage2_pred.lower()}">{stage2_pred}</div>
                <p><b>Confidence Level</b></p>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {stage2_confidence_percent}%"></div>
                </div>
                <p style="margin: 0.5rem 0; font-weight: 600; color: #667eea;">
                    {stage2_confidence_percent:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)

        # === Clinical Recommendation ===
        # === Clinical Recommendation ===
        referral = result.get("referral", "Unknown")

        if referral.lower() == "urgent":
            rec_card = """
            <div class="metric-card">
                <h4>📋 Clinical Recommendation</h4>
                <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a6f); 
                        color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h3 style="margin: 0;">⚠️ URGENT</h3>
                    <p style="margin: 0.5rem 0 0 0;">Specialist consultation required</p>
                </div>
            </div>
            """
        elif referral.lower() == "routine":
            rec_card = """
            <div class="metric-card">
                <h4>📋 Clinical Recommendation</h4>
                <div style="background: linear-gradient(135deg, #fbbf24, #f59e0b); 
                        color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h3 style="margin: 0;">📅 ROUTINE</h3>
                    <p style="margin: 0.5rem 0 0 0;">Follow-up recommended</p>
                </div>
            </div>
            """
        elif referral.lower() == "no referral":
            rec_card = """
            <div class="metric-card">
                <h4>📋 Clinical Recommendation</h4>
                <div style="background: linear-gradient(135deg, #4facfe, #00f2fe); 
                        color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h3 style="margin: 0;">✅ NO REFERRAL</h3>
                    <p style="margin: 0.5rem 0 0 0;">No referral needed</p>
                </div>
            </div>
            """
        else:
            rec_card = f"""
            <div class="metric-card">
                <h4>📋 Clinical Recommendation</h4>
                <p>⚠️ Unknown referral status: {referral}</p>
            </div>
            """

        st.markdown(rec_card, unsafe_allow_html=True)

        # === PDF Download Section ===
        st.markdown("---")
        st.markdown("### 💾 Export Report")

        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("📄 Download PDF Report", key="single_pdf_download"):
                try:
                    with st.spinner("Generating PDF report..."):
                        # Get the uploaded file from session state
                        if file:
                            # Open the uploaded file as PIL Image
                            original_image = Image.open(file)

                            # Generate PDF
                            pdf_buffer = create_pdf_report(result, original_image, file.name)

                            # Create download button
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            filename = f"otoscopy_report_{file.name.split('.')[0]}_{timestamp}.pdf"

                            st.download_button(
                                label="📥 Download Report",
                                data=pdf_buffer,
                                file_name=filename,
                                mime="application/pdf",
                                key="download_single_pdf"
                            )
                            st.success("✅ PDF report generated successfully!")
                        else:
                            st.error("❌ No image available for PDF generation")

                except Exception as e:
                    st.error(f"❌ Error generating PDF: {str(e)}")

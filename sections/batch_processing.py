import streamlit as st
import requests
import base64
import io
from PIL import Image
from utils.api_client import API_URL
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import tempfile
import os
from datetime import datetime

def create_pdf_report(result, original_image, filename):
    """Create a PDF report for a single case"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f2937')
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.HexColor('#374151')
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )

    story = []

    # Title
    story.append(Paragraph("Otoscopy AI Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # Patient info
    story.append(Paragraph("Patient Information", heading_style))
    patient_data = [
        ['Patient ID:', filename],
        ['Analysis Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    ]

    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 16))

    # Diagnostic Results
    story.append(Paragraph("Diagnostic Results", heading_style))

    # Primary Classification
    primary_pred = result.get("stage1_prediction", "Unknown")
    primary_conf = result.get("stage1_probabilities", {}).get(primary_pred, 0) * 100

    results_data = [
        ['Primary Classification:', primary_pred],
        ['Confidence Level:', f'{primary_conf:.1f}%'],
    ]

    # Secondary Classification if available
    if "stage2_prediction" in result:
        secondary_pred = result["stage2_prediction"]
        secondary_conf = result["stage2_probabilities"][secondary_pred] * 100
        results_data.extend([
            ['Secondary Classification:', secondary_pred],
            ['Secondary Confidence:', f'{secondary_conf:.1f}%'],
        ])

    # Referral recommendation
    referral = result.get("referral", "Unknown")
    results_data.append(['Referral Recommendation:', referral])

    results_table = Table(results_data, colWidths=[2.5*inch, 3.5*inch])
    results_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 20))

    # Images section
    story.append(Paragraph("Image Analysis", heading_style))

    # Convert original image to bytes for ReportLab
    orig_img_bytes = io.BytesIO()
    original_image.save(orig_img_bytes, format='PNG')
    orig_img_bytes.seek(0)

    # Add original image
    story.append(Paragraph("Original Image:", normal_style))
    orig_img = RLImage(orig_img_bytes, width=3*inch, height=3*inch)
    story.append(orig_img)
    story.append(Spacer(1, 12))

    # Add Grad-CAM if available
    if "gradcam_url" in result:
        try:
            # Download Grad-CAM image
            gradcam_response = requests.get(f"{API_URL}{result['gradcam_url']}")
            if gradcam_response.status_code == 200:
                gradcam_img_bytes = io.BytesIO(gradcam_response.content)

                story.append(Paragraph("Grad-CAM Heatmap Analysis:", normal_style))
                gradcam_img = RLImage(gradcam_img_bytes, width=3*inch, height=3*inch)
                story.append(gradcam_img)
        except Exception as e:
            story.append(Paragraph(f"Grad-CAM image could not be included: {str(e)}", normal_style))

    # Footer
    story.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    story.append(Paragraph("Generated by Otoscopy AI Analysis System", footer_style))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_batch_pdf_report(results, uploaded_files):
    """Create a comprehensive PDF report for all cases"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f2937')
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.HexColor('#374151')
    )

    story = []

    # Title page
    story.append(Paragraph("Batch Otoscopy AI Analysis Report", title_style))
    story.append(Spacer(1, 20))

    # Summary statistics
    total_cases = len(results)
    urgent_cases = sum(1 for r in results if r.get("referral", "").lower() == "urgent")
    routine_cases = sum(1 for r in results if r.get("referral", "").lower() == "routine")
    no_referral_cases = total_cases - urgent_cases - routine_cases

    story.append(Paragraph("Batch Summary", heading_style))
    summary_data = [
        ['Total Cases Analyzed:', str(total_cases)],
        ['Urgent Referrals:', str(urgent_cases)],
        ['Routine Referrals:', str(routine_cases)],
        ['No Referral Needed:', str(no_referral_cases)],
        ['Analysis Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    ]

    summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 30))

    # Individual case details
    for i, result in enumerate(results):
        if i > 0:
            story.append(Spacer(1, 20))

        filename = result["filename"]
        story.append(Paragraph(f"Case {i+1}: {filename}", heading_style))

        # Get original image
        try:
            original_file = next(f for f in uploaded_files if f.name == filename)
            original_image = Image.open(original_file)

            # Case results table
            primary_pred = result.get("stage1_prediction", "Unknown")
            primary_conf = result.get("stage1_probabilities", {}).get(primary_pred, 0) * 100
            referral = result.get("referral", "Unknown")

            case_data = [
                ['Primary Classification:', primary_pred],
                ['Confidence:', f'{primary_conf:.1f}%'],
                ['Referral:', referral]
            ]

            if "stage2_prediction" in result:
                secondary_pred = result["stage2_prediction"]
                secondary_conf = result["stage2_probabilities"][secondary_pred] * 100
                case_data.insert(-1, ['Secondary Classification:', secondary_pred])
                case_data.insert(-1, ['Secondary Confidence:', f'{secondary_conf:.1f}%'])

            case_table = Table(case_data, colWidths=[2*inch, 3*inch])
            case_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(case_table)

        except StopIteration:
            story.append(Paragraph(f"Original image not found for {filename}", styles['Normal']))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def render():
    st.markdown(
        """"
        <style>
        .metric-card {
            background: white;
            padding: 1rem 1.2rem;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            margin: 0.8rem;
            border-left: 4px solid #667eea;
            max-width: 280px;   /* keep them smaller */
            display: inline-block;
            vertical-align: top;
        }
        .metric-card h4 {
            font-size: 1rem;
            margin-bottom: 0.5rem;
        }
        .metric-card p {
            font-size: 0.9rem;
            margin: 0.2rem 0;
        }
        .prediction-badge {
            font-size: 0.85rem;
            padding: 0.3rem 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown("## 📦 Batch Processing")
    st.write("Upload multiple otoscopy images for AI-based screening.")

    # File uploader (multiple files)
    uploaded_files = st.file_uploader(
        "Upload multiple images",
        type=["jpg", "jpeg", "png", "tiff", "tif"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("🚀 Run Batch Analysis"):
        with st.spinner("Analyzing all images..."):
            upload_files = [("files", (f.name, f, "multipart/form-data")) for f in uploaded_files]
            try:
                response = requests.post(f"{API_URL}/batch_predict", files=upload_files, timeout=180)
                if response.status_code == 200:
                    st.session_state.batch_results = response.json()["results"]
                    st.session_state.uploaded_files = uploaded_files  # keep originals for later
                    st.success("✅ Batch analysis completed!")
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"🚫 API connection failed: {e}")

    # Show results if available
    if "batch_results" in st.session_state:
        results = st.session_state.batch_results
        uploaded_files = st.session_state.uploaded_files

        # Controls row
        control_col1, control_col2, control_col3 = st.columns([2, 2, 2])

        with control_col1:
            # Sorting
            sort_by = st.selectbox("🔽 Sort results by", ["Patient ID", "Confidence", "Referral"])
            if sort_by == "Confidence":
                results = sorted(results, key=lambda x: x.get("confidence", 0), reverse=True)
            elif sort_by == "Patient ID":
                results = sorted(results, key=lambda x: x["filename"])
            elif sort_by == "Referral":
                urgency_order = {"Urgent": 0, "Routine": 1, "No Referral": 2}
                results = sorted(results, key=lambda x: urgency_order.get(x["referral"], 3))

        with control_col3:
            # Save All PDF Button
            if st.button("📋 Generate Batch PDF Report", key="save-all-pdf"):
                try:
                    with st.spinner("Generating comprehensive PDF report..."):
                        # Generate batch PDF
                        pdf_buffer = create_batch_pdf_report(results, uploaded_files)

                        # Download button for batch report
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        st.download_button(
                            label="📄 Download Batch PDF Report",
                            data=pdf_buffer,
                            file_name=f"batch_otoscopy_report_{timestamp}.pdf",
                            mime="application/pdf",
                            key="download-batch-pdf"
                        )
                        st.success(f"✅ Batch PDF report with {len(results)} cases generated successfully!")

                except Exception as e:
                    st.error(f"❌ Error generating batch PDF: {str(e)}")

        st.markdown("---")

        # Display each case as card
        for i, res in enumerate(results):
            filename = res["filename"]
            prediction = res.get("stage1_prediction", "Unknown")
            conf = res.get("confidence", 0) * 100
            referral = res.get("referral", "Unknown")

            # Background color by urgency
            if referral.lower() == "urgent":
                bg_color = "#fecaca"  # red-300
            elif referral.lower() == "routine":
                bg_color = "#fde68a"  # amber-300
            else:
                bg_color = "#bbf7d0"  # green-300

            with st.container():
                st.markdown(
                    f"""
                    <div style="background:{bg_color}; padding:1rem; border-radius:12px; 
                                margin-bottom:1rem; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <b>{filename}</b><br>
                            Prediction: {prediction} ({conf:.1f}%)<br>
                            Referral: {referral}
                        </div>
                        
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Instead of custom button hack, use Streamlit button with key
                if st.button(f"🔍 View {filename}", key=f"view-{i}"):
                    st.markdown(f"### 🧾 Patient: {filename}")
                    
                
                    st.markdown("<div style='display:flex; flex-wrap:wrap;'>", unsafe_allow_html=True)

                    # --- Results Section ---
                    st.markdown("### 📊 Diagnostic Results")

                    if "stage2_prediction" in res:
                        # 3 columns if secondary exists
                        col1, col2, col3 = st.columns(3)

                        # Primary classification
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>🎯 Primary Classification</h4>
                                <div class="prediction-badge {res['stage1_prediction'].lower()}">
                                    {res['stage1_prediction']}
                                </div>
                                <p><b>Confidence Level</b></p>
                                <p style="margin: 0.5rem 0; font-weight: 600; color: #667eea;">
                                    {res['stage1_probabilities'][res['stage1_prediction']]*100:.1f}%
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                        # Secondary classification
                        with col2:
                            stage2_pred = res["stage2_prediction"]
                            stage2_conf = res["stage2_probabilities"][stage2_pred]*100
                            st.markdown(f"""
                            <div class="metric-card">
                                <h4>🔬 Secondary Classification</h4>
                                <div class="prediction-badge {stage2_pred.lower()}">
                                    {stage2_pred}
                                </div>
                                <p><b>Confidence Level</b></p>
                                <p style="margin: 0.5rem 0; font-weight: 600; color: #667eea;">
                                    {stage2_conf:.1f}%
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                        # Referral
                        with col3:
                            referral = res.get("referral", "Unknown")
                            if referral.lower() == "urgent":
                                color = "linear-gradient(135deg, #ff6b6b, #ee5a6f)"
                                text = "⚠️ URGENT"
                            elif referral.lower() == "routine":
                                color = "linear-gradient(135deg, #fbbf24, #f59e0b)"
                                text = "📅 ROUTINE"
                            else:
                                color = "linear-gradient(135deg, #4facfe, #00f2fe)"
                                text = "✅ NO REFERRAL"

                            st.markdown(f"""
                            <div class="metric-card" style="background: {color}; color: white; text-align: center;">
                                <h4>📋 Referral</h4>
                                <h3 style="margin:0; font-size:1.5rem;">{text}</h3>
                            </div>
                            """, unsafe_allow_html=True)

                    else:
                        # Only 2 columns (Primary + Referral)
                        col1, col2 = st.columns(2)

                        with col1:
                            # Primary card same as above...
                            pass

                        with col2:
                            # Referral card same as above...
                            pass



                    # === Images side by side ===
                    img_col1, img_col2 = st.columns(2)
                    with img_col1:
                        st.markdown("##### 🖼️ Original Image")
                        try:
                            original_file = next(f for f in uploaded_files if f.name == filename)
                            img = Image.open(original_file)
                            st.image(img, width=350)
                        except StopIteration:
                            st.warning("⚠️ Original image not found in upload session.")

                    with img_col2:
                        st.markdown("##### 🔥 Heatmap Analysis")
                        if "gradcam_url" in res:
                            st.image(f"{API_URL}{res['gradcam_url']}", width=350)
                        else:
                            st.warning("⚠️ No heatmap available.")

                    # PDF Save Button for individual case
                    st.markdown("---")
                    col_pdf, col_spacer = st.columns([1, 3])
                    with col_pdf:
                        if st.button(f"💾 Save PDF Report", key=f"save-pdf-{i}"):
                            try:
                                # Get original image
                                original_file = next(f for f in uploaded_files if f.name == filename)
                                original_image = Image.open(original_file)

                                # Generate PDF
                                pdf_buffer = create_pdf_report(res, original_image, filename)

                                # Download button
                                st.download_button(
                                    label="📄 Download PDF Report",
                                    data=pdf_buffer,
                                    file_name=f"otoscopy_report_{filename.split('.')[0]}.pdf",
                                    mime="application/pdf",
                                    key=f"download-pdf-{i}"
                                )
                                st.success("✅ PDF report generated successfully!")

                            except Exception as e:
                                st.error(f"❌ Error generating PDF: {str(e)}")

                    st.markdown("---")

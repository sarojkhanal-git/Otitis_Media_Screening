import streamlit as st

def render():
    st.markdown("""
    <style>
    .help-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .help-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
    }
    .help-header p {
        color: #f0f4ff;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    .help-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .faq-item {
        background: #f8faff;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    .faq-question {
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
    }
    .faq-answer {
        color: #6b7280;
        line-height: 1.6;
    }
    .contact-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .contact-method {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem;
        backdrop-filter: blur(10px);
    }
    .tutorial-step {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid #10b981;
    }
    .step-number {
        background: #10b981;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
    }
    .troubleshooting-tip {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .feature-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="help-header">
        <h1>❓ Help & Support</h1>
        <p>Get assistance with EarScope AI system</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Start Guide
    st.markdown("""
    <div class="help-section">
        <h3>🚀 Quick Start Guide</h3>
        <p>Get up and running with EarScope AI in minutes:</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tutorial-step">
        <div style="display: flex; align-items: center;">
            <span class="step-number">1</span>
            <div>
                <strong>Upload an Image</strong>
                <p style="margin: 0.5rem 0 0 0; color: #666;">Navigate to 'Single Analysis' and drag & drop your otoscopy image or click to browse. Supported formats: JPG, PNG, TIFF</p>
            </div>
        </div>
    </div>

    <div class="tutorial-step">
        <div style="display: flex; align-items: center;">
            <span class="step-number">2</span>
            <div>
                <strong>View Results</strong>
                <p style="margin: 0.5rem 0 0 0; color: #666;">The AI will automatically analyze your image and provide diagnostic results with confidence levels and clinical recommendations</p>
            </div>
        </div>
    </div>

    <div class="tutorial-step">
        <div style="display: flex; align-items: center;">
            <span class="step-number">3</span>
            <div>
                <strong>Export Reports</strong>
                <p style="margin: 0.5rem 0 0 0; color: #666;">Download professional PDF reports containing complete analysis results, original images, and Grad-CAM visualizations</p>
            </div>
        </div>
    </div>

    <div class="tutorial-step">
        <div style="display: flex; align-items: center;">
            <span class="step-number">4</span>
            <div>
                <strong>Batch Processing</strong>
                <p style="margin: 0.5rem 0 0 0; color: #666;">For multiple images, use 'Batch Processing' to analyze several cases at once and generate comprehensive reports</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Features
    st.markdown("""
    <div class="help-section">
        <h3>✨ Key Features</h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-highlight">
            <h4>🔬 AI-Powered Analysis</h4>
            <p>Advanced CNN models trained specifically for otitis media detection with 94%+ accuracy</p>
        </div>

        <div class="feature-highlight">
            <h4>📊 Explainable AI</h4>
            <p>Grad-CAM heatmaps show exactly which regions influenced the AI's decision</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-highlight">
            <h4>📄 Professional Reports</h4>
            <p>Generate comprehensive PDF reports with diagnostic results and clinical recommendations</p>
        </div>

        <div class="feature-highlight">
            <h4>⚡ Fast Processing</h4>
            <p>Get results in under 2 seconds with real-time analysis and immediate feedback</p>
        </div>
        """, unsafe_allow_html=True)

    # FAQ Section
    st.markdown("""
    <div class="help-section">
        <h3>❓ Frequently Asked Questions</h3>
    </div>
    """, unsafe_allow_html=True)

    faqs = [
        {
            "q": "What image formats are supported?",
            "a": "EarScope AI supports JPG, JPEG, PNG, TIFF, and TIF formats. For best results, use high-resolution images with clear visibility of the tympanic membrane."
        },
        {
            "q": "How accurate is the AI diagnosis?",
            "a": "Our models achieve over 94% accuracy on validated datasets. However, AI results should always be interpreted by qualified healthcare professionals and not used as a sole diagnostic tool."
        },
        {
            "q": "What do the different classifications mean?",
            "a": "Normal: Healthy ear with clear tympanic membrane. AOM: Acute Otitis Media with active infection. COM: Chronic Otitis Media with long-term changes. Earwax: Cerumen impaction blocking proper visualization."
        },
        {
            "q": "How do I interpret the Grad-CAM heatmap?",
            "a": "The heatmap highlights regions that influenced the AI's decision. Red/warm colors indicate areas of high importance, while blue/cool colors show less relevant regions."
        },
        {
            "q": "Can I batch process multiple images?",
            "a": "Yes! Use the 'Batch Processing' section to upload and analyze multiple images simultaneously. You can also generate individual or comprehensive batch reports."
        },
        {
            "q": "Is my patient data secure?",
            "a": "Yes, all images are processed locally and not stored permanently. No patient data is transmitted to external servers for analysis."
        },
        {
            "q": "What should I do if I get an 'Urgent' recommendation?",
            "a": "Urgent recommendations suggest immediate specialist consultation is needed. Please refer the patient to an ENT specialist or appropriate healthcare provider promptly."
        },
        {
            "q": "Why might an analysis fail?",
            "a": "Analysis may fail due to poor image quality, unsupported formats, or network connectivity issues. Ensure images are clear, well-lit, and in supported formats."
        }
    ]

    for faq in faqs:
        st.markdown(f"""
        <div class="faq-item">
            <div class="faq-question">Q: {faq['q']}</div>
            <div class="faq-answer">A: {faq['a']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Troubleshooting
    st.markdown("""
    <div class="help-section">
        <h3>🔧 Troubleshooting</h3>
    </div>
    """, unsafe_allow_html=True)

    troubleshooting_tips = [
        {
            "issue": "Image upload fails",
            "solution": "Check file format (JPG, PNG, TIFF), ensure file size is under 10MB, and verify network connection."
        },
        {
            "issue": "Analysis takes too long",
            "solution": "Large images may take longer to process. Try reducing image size or check system status on the Dashboard."
        },
        {
            "issue": "Poor quality results",
            "solution": "Ensure images are well-lit, in focus, and show clear view of the ear canal. Avoid blurry or dark images."
        },
        {
            "issue": "PDF generation fails",
            "solution": "Check browser compatibility and ensure pop-up blockers are disabled. Try refreshing the page and regenerating."
        },
        {
            "issue": "Grad-CAM not displaying",
            "solution": "This may indicate processing issues. Try re-uploading the image or contact support if the issue persists."
        }
    ]

    for tip in troubleshooting_tips:
        st.markdown(f"""
        <div class="troubleshooting-tip">
            <strong>Issue:</strong> {tip['issue']}<br>
            <strong>Solution:</strong> {tip['solution']}
        </div>
        """, unsafe_allow_html=True)

    # System Requirements
    st.markdown("""
    <div class="help-section">
        <h3>💻 System Requirements</h3>
        <h4>Minimum Requirements:</h4>
        <ul>
            <li><strong>Browser:</strong> Chrome 80+, Firefox 75+, Safari 13+, Edge 80+</li>
            <li><strong>RAM:</strong> 4GB minimum (8GB recommended)</li>
            <li><strong>Internet:</strong> Stable broadband connection</li>
            <li><strong>JavaScript:</strong> Must be enabled</li>
        </ul>

        <h4>Recommended Setup:</h4>
        <ul>
            <li><strong>Display:</strong> 1920x1080 or higher resolution</li>
            <li><strong>Storage:</strong> 1GB free space for temporary files</li>
            <li><strong>Camera:</strong> High-resolution otoscope camera for best results</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Contact Support
    st.markdown("""
    <div class="contact-card">
        <h3>📞 Contact Support</h3>
        <p>Need additional help? Our support team is here to assist you.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="contact-method">
            <h4>📧 Email Support</h4>
            <p>support@earscope.ai</p>
            <p><small>Response within 24 hours</small></p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="contact-method">
            <h4>💬 Live Chat</h4>
            <p>Available 9 AM - 5 PM PST</p>
            <p><small>Click chat button in bottom right</small></p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="contact-method">
            <h4>📚 Documentation</h4>
            <p>docs.earscope.ai</p>
            <p><small>Comprehensive user guides</small></p>
        </div>
        """, unsafe_allow_html=True)

    # Training Resources
    st.markdown("""
    <div class="help-section">
        <h3>🎓 Training Resources</h3>
        <ul>
            <li><strong>Video Tutorials:</strong> Step-by-step guidance for all features</li>
            <li><strong>Webinar Series:</strong> Monthly training sessions with Q&A</li>
            <li><strong>User Manual:</strong> Comprehensive PDF guide available for download</li>
            <li><strong>Best Practices:</strong> Guidelines for optimal image capture and analysis</li>
            <li><strong>Case Studies:</strong> Real-world examples and clinical scenarios</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
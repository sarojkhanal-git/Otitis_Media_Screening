import streamlit as st
from streamlit_option_menu import option_menu
import urllib.parse

# Import section UIs
from sections import single_analysis, batch_processing, history, dashboard, help_support
# about temporarily disabled due to persistent encoding issue

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="EarScope AI - Otitis Media Screening",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Professional Styling
st.markdown("""
<style>
/* Global app styling */
.main {
    background-color: #f8faff;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stActionButton {display:none;}

/* Custom header styling */
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem 2rem;
    border-radius: 0 0 15px 15px;
    margin: -1rem -1rem 2rem -1rem;
    color: white;
    text-align: center;
}

/* Consistent card styling across all sections */
.main-content {
    padding: 0 1rem;
}

/* Professional typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    color: #1f2937;
}

/* Loading and success messages */
.stAlert > div {
    border-radius: 8px;
    border-left: 4px solid #667eea;
}

/* Button styling consistency */
.stButton > button {
    border-radius: 8px;
    border: none;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

/* Sidebar professional styling */
.css-1d391kg {
    background-color: white;
}

/* Download button styling */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

/* File uploader styling */
.css-1cpxqw2 {
    border-radius: 12px;
    border: 2px dashed #667eea;
}

/* Professional spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# Sidebar Navigation
# ------------------------
with st.sidebar:
    # Add custom CSS for title styling
    st.markdown(
        """
        <style>
        .sidebar-title {
            font-family: 'Segoe UI', sans-serif;
            font-size: 20px;
            font-weight: 700;
            color: #1f2937;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar Title
    st.markdown(
        "<div class='sidebar-title'>Middle Ear Infection Screening with AI</div>",
        unsafe_allow_html=True
    )

    # Sidebar Menu
    mode = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Single Analysis",
            "Batch Processing",
            "Analysis History",
            "Help & Support",
            "About"
        ],
        icons=[
            "speedometer2", "camera", "images", "clock-history", "question-circle", "info-circle"
        ],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f8faff"},
            "icon": {"color": "#667eea", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "font-weight": "500",
                "padding": "12px 20px",
                "margin": "4px 10px",
                "border-radius": "8px",
            },
            "nav-link-selected": {"background-color": "#e0e7ff", "color": "#1e3a8a"},
        }
    )

# ------------------------
# Main Area
# ------------------------

# Professional header
st.markdown("""
<div class="app-header">
    <h1 style="margin: 0; font-size: 2.2rem;">🩺 EarScope AI</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Advanced Otitis Media Screening with Artificial Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Routing
if mode == "Dashboard":
    dashboard.render()
elif mode == "Single Analysis":
    single_analysis.render()
elif mode == "Batch Processing":
    batch_processing.render()
elif mode == "Analysis History":
    history.render()
elif mode == "Help & Support":
    help_support.render()
elif mode == "About":
    about.render()



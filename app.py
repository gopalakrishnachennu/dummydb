"""
DataForge Pro - Enterprise Data Generation Platform
Premium Award-Winning Design
"""

import streamlit as st
from core.config import Config
from core.ui_config import UIConfig

# Page configuration
st.set_page_config(
    page_title=UIConfig.APP_NAME,
    page_icon="🔥",
    layout=Config.UI["layout"],
    initial_sidebar_state=Config.UI["sidebar_state"]
)

# Initialize session state
if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False
if 'db_connection' not in st.session_state:
    st.session_state.db_connection = None
if 'db_type' not in st.session_state:
    st.session_state.db_type = None
if 'schema_created' not in st.session_state:
    st.session_state.schema_created = False
if 'tables' not in st.session_state:
    st.session_state.tables = []

# Premium Award-Winning CSS (Same as Database Connection page)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .stApp { background: #e0e5ec; }
    
    /* Sidebar - Premium Design */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #d4dae6 0%, #e0e5ec 100%);
        border-right: 1px solid rgba(163, 177, 198, 0.2);
    }
    
    [data-testid="stSidebarNav"] a {
        background: #e0e5ec !important;
        border-radius: 12px !important;
        margin: 0.5rem 0.5rem !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 4px 4px 8px rgba(163, 177, 198, 0.4), -4px -4px 8px rgba(255, 255, 255, 0.6) !important;
        transition: all 0.3s ease !important;
        color: #4b5563 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.4), inset -3px -3px 6px rgba(255, 255, 255, 0.6) !important;
        transform: translateY(1px);
    }
    
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 4px 4px 8px rgba(102, 126, 234, 0.4), -4px -4px 8px rgba(255, 255, 255, 0.3) !important;
    }
    
    .main .block-container { padding: 2rem 3rem; max-width: 1200px; }
    
    /* Headers */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0 0.5rem 0;
        letter-spacing: -0.02em;
        text-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.4)); }
        50% { filter: drop-shadow(0 0 20px rgba(118, 75, 162, 0.6)); }
    }
    
    .app-icon {
        display: inline-block;
        font-size: 3rem;
        margin-right: 0.5rem;
        vertical-align: middle;
        animation: iconFloat 3s ease-in-out infinite;
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #4b5563;
        margin: 2.5rem 0 1.5rem 0;
    }
    
    /* Cards */
    .welcome-card {
        background: #e0e5ec;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 8px 8px 16px rgba(163, 177, 198, 0.5), -8px -8px 16px rgba(255, 255, 255, 0.6);
        text-align: center;
    }
    
    .welcome-card h2 {
        font-size: 1.6rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 1rem;
    }
    
    .welcome-card p {
        font-size: 1rem;
        color: #6b7280;
        line-height: 1.6;
    }
    
    /* Step Cards */
    .step-card {
        background: #e0e5ec;
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1rem 0;
        box-shadow: 6px 6px 12px rgba(163, 177, 198, 0.4), -6px -6px 12px rgba(255, 255, 255, 0.6);
        display: flex;
        align-items: flex-start;
        gap: 1.2rem;
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        box-shadow: 8px 8px 16px rgba(163, 177, 198, 0.5), -8px -8px 16px rgba(255, 255, 255, 0.7);
        transform: translateY(-2px);
    }
    
    .step-number {
        min-width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        box-shadow: 4px 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .step-content h3 {
        font-size: 1.1rem;
        font-weight: 600;
        color: #4b5563;
        margin: 0 0 0.5rem 0;
    }
    
    .step-content p {
        font-size: 0.9rem;
        color: #6b7280;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Feature Cards */
    .feature-card {
        background: #e0e5ec;
        border-radius: 14px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 5px 5px 10px rgba(163, 177, 198, 0.4), -5px -5px 10px rgba(255, 255, 255, 0.6);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        box-shadow: 7px 7px 14px rgba(163, 177, 198, 0.5), -7px -7px 14px rgba(255, 255, 255, 0.7);
        transform: translateX(4px);
    }
    
    .feature-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.5;
    }
    
    /* Status Cards */
    .status-card {
        background: #e0e5ec;
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        box-shadow: 6px 6px 12px rgba(163, 177, 198, 0.4), -6px -6px 12px rgba(255, 255, 255, 0.6);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .status-card:hover {
        box-shadow: 8px 8px 16px rgba(163, 177, 198, 0.5), -8px -8px 16px rgba(255, 255, 255, 0.7);
        transform: translateY(-3px);
    }
    
    .status-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }
    
    .status-title {
        font-size: 1rem;
        font-weight: 600;
        color: #4b5563;
        margin: 0.5rem 0;
    }
    
    .status-subtitle {
        font-size: 0.85rem;
        color: #6b7280;
    }
    
    /* Founder Card */
    .founder-card {
        background: #e0e5ec;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 8px 8px 16px rgba(163, 177, 198, 0.5), -8px -8px 16px rgba(255, 255, 255, 0.6);
        margin: 3rem 0;
    }
    
    .profile-frame {
        width: 120px;
        height: 120px;
        margin: 0 auto 1.5rem auto;
        border-radius: 24px;
        background: #e0e5ec;
        box-shadow: inset 5px 5px 10px rgba(163, 177, 198, 0.4), inset -5px -5px 10px rgba(255, 255, 255, 0.6);
        padding: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .profile-frame img {
        width: 100%;
        height: 100%;
        border-radius: 18px;
        object-fit: cover;
    }
    
    .founder-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 0.5rem;
    }
    
    .founder-title {
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    
    .social-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.7rem 1.5rem;
        background: #e0e5ec;
        border-radius: 10px;
        color: #4b5563;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        box-shadow: 4px 4px 8px rgba(163, 177, 198, 0.4), -4px -4px 8px rgba(255, 255, 255, 0.6);
        transition: all 0.3s ease;
        margin: 0 0.5rem;
    }
    
    .social-btn:hover {
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.4), inset -3px -3px 6px rgba(255, 255, 255, 0.6);
        color: #667eea;
        text-decoration: none;
        transform: translateY(1px);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f'''
<h1 class="main-title">
    <span class="app-icon">🔥</span>{UIConfig.APP_NAME}
</h1>
''', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{UIConfig.APP_TAGLINE}</p>', unsafe_allow_html=True)

# Welcome Card
st.markdown(f"""
<div class="welcome-card">
    <h2>{UIConfig.PAGE_TITLES["home"]}</h2>
    <p>{UIConfig.APP_DESCRIPTION}</p>
</div>
""", unsafe_allow_html=True)

# Getting Started Steps
st.markdown('<h2 class="section-header">Getting Started</h2>', unsafe_allow_html=True)

for step in UIConfig.STEPS:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-number">{step["number"]}</div>
        <div class="step-content">
            <h3>{step["title"]}</h3>
            <p>{step["description"]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Features
st.markdown('<h2 class="section-header">Key Features</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    for feature in UIConfig.FEATURES["left"]:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{feature["title"]}</div>
            <div class="feature-desc">{feature["description"]}</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    for feature in UIConfig.FEATURES["right"]:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{feature["title"]}</div>
            <div class="feature-desc">{feature["description"]}</div>
        </div>
        """, unsafe_allow_html=True)

# System Status
st.markdown('<h2 class="section-header">System Status</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.db_connected:
        db_info = UIConfig.get_database_info(st.session_state.db_type) if st.session_state.db_type else {}
        st.markdown(f"""
        <div class="status-card">
            <div class="status-icon">✅</div>
            <div class="status-title">Connected</div>
            <div class="status-subtitle">{db_info.get("name", "Database")}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">⏳</div>
            <div class="status-title">Not Connected</div>
            <div class="status-subtitle">Configure connection</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if st.session_state.schema_created:
        st.markdown(f"""
        <div class="status-card">
            <div class="status-icon">✅</div>
            <div class="status-title">Schema Ready</div>
            <div class="status-subtitle">{len(st.session_state.tables)} tables</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">⏳</div>
            <div class="status-title">Schema Pending</div>
            <div class="status-subtitle">Setup required</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    if st.session_state.db_connected and st.session_state.schema_created:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">🚀</div>
            <div class="status-title">Ready</div>
            <div class="status-subtitle">All systems go</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">ℹ️</div>
            <div class="status-title">Setup Required</div>
            <div class="status-subtitle">Follow steps above</div>
        </div>
        """, unsafe_allow_html=True)

# Footer with Founder Info
founder_name = UIConfig.FOUNDER["name"]
founder_title = UIConfig.FOUNDER["title"]
founder_github = UIConfig.FOUNDER["github"]
founder_linkedin = UIConfig.FOUNDER["linkedin"]
app_name = UIConfig.APP_NAME
app_version = UIConfig.APP_VERSION
footer_tagline = UIConfig.FOOTER["tagline"]

st.markdown(f"""
<div class="founder-card">
    <div class="profile-frame">
        <img src="https://github.com/gopalakrishnachennu.png" alt="{founder_name}" />
    </div>
    <div class="founder-name">{founder_name}</div>
    <div class="founder-title">{founder_title}</div>
    <div style="margin-bottom: 1.5rem;">
        <a href="{founder_github}" target="_blank" class="social-btn"><i class="fab fa-github"></i> GitHub</a>
        <a href="{founder_linkedin}" target="_blank" class="social-btn"><i class="fab fa-linkedin"></i> LinkedIn</a>
    </div>
    <div style="padding-top: 1.5rem; border-top: 1px solid rgba(163, 177, 198, 0.2);">
        <div style="font-size: 1.1rem; font-weight: 600; color: #4b5563; margin-bottom: 0.5rem;">{app_name} v{app_version}</div>
        <div style="font-size: 0.9rem; color: #6b7280;">{footer_tagline}</div>
    </div>
</div>
""", unsafe_allow_html=True)

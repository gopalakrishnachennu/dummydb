"""
Page 1: Database Connection
Premium Award-Winning Design
"""

import streamlit as st
import tempfile
import os
from core.database import MySQLManager, PostgreSQLManager, MongoDBManager
from core.config import Config
from core.ui_config import UIConfig
from utils.validators import validate_connection, format_error

st.set_page_config(
    page_title=f"{UIConfig.APP_NAME} - Database Connection",
    page_icon="🔌",
    layout="wide"
)

# Premium Award-Winning CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Soft Background */
    .stApp { 
        background: #e0e5ec;
    }
    
    /* Sidebar - Premium Design */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #d4dae6 0%, #e0e5ec 100%);
        border-right: 1px solid rgba(163, 177, 198, 0.2);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Sidebar Navigation Items */
    [data-testid="stSidebarNav"] a {
        background: #e0e5ec !important;
        border-radius: 12px !important;
        margin: 0.5rem 0.5rem !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 4px 4px 8px rgba(163, 177, 198, 0.4), 
                    -4px -4px 8px rgba(255, 255, 255, 0.6) !important;
        transition: all 0.3s ease !important;
        color: #4b5563 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.4), 
                    inset -3px -3px 6px rgba(255, 255, 255, 0.6) !important;
        transform: translateY(1px);
    }
    
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 4px 4px 8px rgba(102, 126, 234, 0.4), 
                    -4px -4px 8px rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Main Container */
    .main .block-container { 
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Page Headers - Soft Colors */
    .page-title {
        font-size: 2.2rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Section Headers - Natural */
    h2, h3 {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #4b5563 !important;
        margin: 2rem 0 1.2rem 0 !important;
    }
    
    /* Labels - Soft Gray */
    label {
        color: #6b7280 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Text Inputs - Subtle Neumorphic */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #e0e5ec !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.3), 
                    inset -3px -3px 6px rgba(255, 255, 255, 0.5) !important;
        color: #374151 !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        box-shadow: inset 4px 4px 8px rgba(163, 177, 198, 0.35), 
                    inset -4px -4px 8px rgba(255, 255, 255, 0.55) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
        font-weight: 300 !important;
    }
    
    /* Select Boxes - Clean */
    .stSelectbox > div > div {
        background: #e0e5ec !important;
        border-radius: 10px !important;
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.3), 
                    inset -3px -3px 6px rgba(255, 255, 255, 0.5) !important;
    }
    
    .stSelectbox select {
        background: transparent !important;
        border: none !important;
        color: #374151 !important;
        font-size: 0.9rem !important;
        padding: 0.7rem 1rem !important;
        font-weight: 400 !important;
    }
    
    /* Number Input Buttons - Subtle */
    .stNumberInput button {
        background: #e0e5ec !important;
        border: none !important;
        border-radius: 6px !important;
        box-shadow: 2px 2px 4px rgba(163, 177, 198, 0.3), 
                    -2px -2px 4px rgba(255, 255, 255, 0.5) !important;
        color: #667eea !important;
        width: 28px !important;
        height: 28px !important;
    }
    
    .stNumberInput button:hover {
        box-shadow: inset 2px 2px 4px rgba(163, 177, 198, 0.3), 
                    inset -2px -2px 4px rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Buttons - Premium */
    .stButton > button {
        background: #e0e5ec !important;
        color: #4b5563 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 1.8rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        box-shadow: 4px 4px 8px rgba(163, 177, 198, 0.4), 
                    -4px -4px 8px rgba(255, 255, 255, 0.6) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.4), 
                    inset -3px -3px 6px rgba(255, 255, 255, 0.6) !important;
        transform: translateY(1px);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 4px 4px 8px rgba(102, 126, 234, 0.4), 
                    -4px -4px 8px rgba(255, 255, 255, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: inset 3px 3px 6px rgba(102, 126, 234, 0.5), 
                    inset -3px -3px 6px rgba(118, 75, 162, 0.5) !important;
    }
    
    /* Checkbox - Soft Purple */
    .stCheckbox {
        background: #e0e5ec;
        padding: 0.9rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        box-shadow: 4px 4px 8px rgba(163, 177, 198, 0.4), 
                    -4px -4px 8px rgba(255, 255, 255, 0.6);
    }
    
    .stCheckbox label {
        color: #4b5563 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    .stCheckbox input[type="checkbox"] {
        accent-color: #667eea !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: #e0e5ec;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.3), 
                    inset -3px -3px 6px rgba(255, 255, 255, 0.5);
    }
    
    .stFileUploader label {
        color: #4b5563 !important;
    }
    
    /* Success/Error Messages - Soft Colors */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border-left: 4px solid #10b981 !important;
        color: #047857 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid #ef4444 !important;
        color: #b91c1c !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.1) !important;
        border-left: 4px solid #fbbf24 !important;
        color: #b45309 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border-left: 4px solid #3b82f6 !important;
        color: #1e40af !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown(f'<h1 class="page-title">🔌 {UIConfig.PAGE_TITLES["connection"]}</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Configure your database connection settings</p>', unsafe_allow_html=True)

# Check if already connected
if st.session_state.get('db_connected', False):
    st.success(f"✅ Already connected to {st.session_state.db_type.upper()}")
    if st.button("Disconnect"):
        if st.session_state.db_connection:
            st.session_state.db_connection.close()
        st.session_state.db_connected = False
        st.session_state.db_connection = None
        st.session_state.db_type = None
        st.rerun()
    st.info("👉 Proceed to **Schema Setup** page")
    st.stop()

# Connection Form
st.markdown("## Database Configuration")

col1, col2 = st.columns([1, 2])

with col1:
    db_type = st.selectbox(
        "Database Type",
        options=list(UIConfig.DATABASES.keys()),
        format_func=lambda x: UIConfig.DATABASES[x]["name"]
    )

with col2:
    host = st.text_input("Host", value="localhost", placeholder="localhost or IP address")

col1, col2, col3 = st.columns(3)

with col1:
    port = st.number_input("Port", value=UIConfig.DATABASES[db_type].get("default_port", 3306), min_value=1, max_value=65535)

with col2:
    username = st.text_input("Username", value="root" if db_type == "mysql" else "postgres")

with col3:
    password = st.text_input("Password", type="password", placeholder="••••••••")

database = st.text_input("Database Name", value="test_db", help="Will be created if it doesn't exist")

# SSH Tunnel Configuration
st.markdown("## SSH Tunnel (Optional)")

use_ssh = st.checkbox("Enable SSH Tunnel for Remote Connection")

ssh_host = ssh_port = ssh_user = ssh_key_file = None

if use_ssh:
    col1, col2 = st.columns(2)
    with col1:
        ssh_host = st.text_input("SSH Host", placeholder="ssh.example.com")
        ssh_user = st.text_input("SSH Username", placeholder="ubuntu")
    with col2:
        ssh_port = st.number_input("SSH Port", value=22, min_value=1, max_value=65535)
        ssh_key_file = st.file_uploader("SSH Private Key", type=['pem', 'key', 'ppk'])

# Connection Actions
st.markdown("## Connect to Database")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    test_btn = st.button("🔍 Test Connection", use_container_width=True)

with col2:
    connect_btn = st.button("✅ Connect", use_container_width=True, type="primary")

if test_btn or connect_btn:
    config = {
        "db_type": db_type,
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "database": database,
        "use_ssh": use_ssh,
        "ssh_host": ssh_host,
        "ssh_port": ssh_port,
        "ssh_user": ssh_user
    }
    
    validation = validate_connection(config)
    
    if not validation["valid"]:
        st.error(format_error("Configuration Error", validation["errors"]))
    else:
        ssh_key_path = None
        if use_ssh and ssh_key_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pem') as tmp:
                tmp.write(ssh_key_file.getvalue())
                ssh_key_path = tmp.name
                os.chmod(ssh_key_path, 0o600)
        
        try:
            if db_type == "mysql":
                manager = MySQLManager(host, port, username, password, database, 
                                     ssh_host, ssh_port, ssh_user, ssh_key_path)
            elif db_type == "postgresql":
                manager = PostgreSQLManager(host, port, username, password, database,
                                          ssh_host, ssh_port, ssh_user, ssh_key_path)
            else:
                manager = MongoDBManager(host, port, username, password, database,
                                       ssh_host, ssh_port, ssh_user, ssh_key_path)
            
            manager.connect()
            
            if test_btn:
                st.success("✅ Connection successful!")
                manager.close()
            else:
                st.session_state.db_connected = True
                st.session_state.db_connection = manager
                st.session_state.db_type = db_type
                st.success("✅ Connected successfully! Proceed to Schema Setup →")
                st.balloons()
                
        except Exception as e:
            st.error(format_error("Connection Failed", [str(e)]))
            if ssh_key_path and os.path.exists(ssh_key_path):
                os.unlink(ssh_key_path)

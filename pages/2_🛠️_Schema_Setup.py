"""
Page 2: Schema Setup
Premium Award-Winning Design
"""

import streamlit as st
from core.config import Config
from core.ui_config import UIConfig
from utils.validators import validate_schema, format_error, get_table_icon

st.set_page_config(
    page_title=f"{UIConfig.APP_NAME} - Schema Setup",
    page_icon="🛠️",
    layout="wide"
)

# Premium Award-Winning CSS (Same as other pages)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .stApp { background: #e0e5ec; }
    
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
    }
    
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    .main .block-container { padding: 2rem 3rem; max-width: 1200px; }
    
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
    }
    
    h2, h3 {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #4b5563 !important;
        margin: 2rem 0 1.2rem 0 !important;
    }
    
    label {
        color: #6b7280 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: #e0e5ec !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.3), inset -3px -3px 6px rgba(255, 255, 255, 0.5) !important;
        color: #374151 !important;
        padding: 0.7rem 1rem !important;
    }
    
    .stButton > button {
        background: #e0e5ec !important;
        color: #4b5563 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 1.8rem !important;
        font-weight: 500 !important;
        box-shadow: 4px 4px 8px rgba(163, 177, 198, 0.4), -4px -4px 8px rgba(255, 255, 255, 0.6) !important;
    }
    
    .stButton > button:hover {
        box-shadow: inset 3px 3px 6px rgba(163, 177, 198, 0.4), inset -3px -3px 6px rgba(255, 255, 255, 0.6) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    .stCheckbox {
        background: #e0e5ec;
        padding: 0.9rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 4px 4px 8px rgba(163, 177, 198, 0.4), -4px -4px 8px rgba(255, 255, 255, 0.6);
    }
    
    .stCheckbox label {
        color: #4b5563 !important;
        font-weight: 500 !important;
    }
    
    .stCheckbox input[type="checkbox"] {
        accent-color: #667eea !important;
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border-left: 4px solid #10b981 !important;
        color: #047857 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid #ef4444 !important;
        color: #b91c1c !important;
        border-radius: 8px !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border-left: 4px solid #3b82f6 !important;
        color: #1e40af !important;
        border-radius: 8px !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown(f'<h1 class="page-title">🛠️ {UIConfig.PAGE_TITLES["schema"]}</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Design and deploy your database schema</p>', unsafe_allow_html=True)

# Check prerequisites
if not st.session_state.get('db_connected', False):
    st.warning("⚠️ Please connect to a database first!")
    st.info("👉 Go to **Database Connection** page")
    st.stop()

db_manager = st.session_state.db_connection
db_type = st.session_state.db_type

# Database Creation
st.markdown("## Database Management")

col1, col2 = st.columns([2, 1])

with col1:
    db_name = st.text_input("Database Name", value=st.session_state.get('database_name', 'test_db'))

with col2:
    st.write("")
    st.write("")
    if st.button("Create Database", use_container_width=True):
        try:
            db_manager.create_database(db_name)
            st.session_state.database_name = db_name
            st.success(f"✅ Database '{db_name}' created successfully!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Table Selection
st.markdown("## Select Tables to Create")

available_tables = Config.get_all_tables()
selected_tables = []

cols = st.columns(3)
for idx, table in enumerate(available_tables):
    with cols[idx % 3]:
        if st.checkbox(f"{get_table_icon(table)} {table.title()}", key=f"table_{table}"):
            selected_tables.append(table)

# Schema Preview
if selected_tables:
    st.markdown("## Schema Preview")
    
    for table in selected_tables:
        with st.expander(f"📋 {table.title()} Schema"):
            schema = Config.get_table_schema(table)
            st.json(schema)

# Create Tables
st.markdown("## Deploy Schema")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🚀 Create Selected Tables", use_container_width=True, type="primary", disabled=len(selected_tables) == 0):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        created_tables = []
        for idx, table in enumerate(selected_tables):
            try:
                status_text.text(f"Creating {table}...")
                schema = Config.get_table_schema(table)
                
                validation = validate_schema(schema)
                if not validation["valid"]:
                    st.error(format_error(f"Schema Error: {table}", validation["errors"]))
                    continue
                
                db_manager.create_table(table, schema)
                created_tables.append(table)
                progress_bar.progress((idx + 1) / len(selected_tables))
                
            except Exception as e:
                st.error(f"❌ Error creating {table}: {str(e)}")
        
        if created_tables:
            st.session_state.tables = created_tables
            st.session_state.schema_created = True
            st.success(f"✅ Created {len(created_tables)} table(s) successfully!")
            st.balloons()
            st.info("👉 Proceed to **Data Generation** page")

# Current Status
if st.session_state.get('schema_created', False):
    st.markdown("## Current Schema Status")
    st.success(f"✅ Schema deployed with {len(st.session_state.tables)} table(s)")
    
    cols = st.columns(len(st.session_state.tables))
    for idx, table in enumerate(st.session_state.tables):
        with cols[idx]:
            st.info(f"{get_table_icon(table)} **{table.title()}**")

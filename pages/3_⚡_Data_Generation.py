"""
Page 3: Data Generation
Premium Award-Winning Design
"""

import streamlit as st
import time
from core.generator import SQLDataGenerator, PerformanceMonitor
from core.config import Config
from core.ui_config import UIConfig

st.set_page_config(
    page_title=f"{UIConfig.APP_NAME} - Data Generation",
    page_icon="⚡",
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
        color: #4b5563 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    .main .block-container { padding: 2rem 3rem; max-width: 1400px; }
    
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
    
    h2 {
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
    
    .stSelectbox > div > div,
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
    
    /* Metric Cards */
    .metric-card {
        background: #e0e5ec;
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        box-shadow: 6px 6px 12px rgba(163, 177, 198, 0.4), -6px -6px 12px rgba(255, 255, 255, 0.6);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        border-left: 4px solid #10b981 !important;
        color: #047857 !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown(f'<h1 class="page-title">⚡ {UIConfig.PAGE_TITLES["generation"]}</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Generate realistic test data at scale</p>', unsafe_allow_html=True)

# Check prerequisites
if not st.session_state.get('db_connected', False):
    st.warning("⚠️ Please connect to a database first!")
    st.info("👉 Go to **Database Connection** page")
    st.stop()

if not st.session_state.get('schema_created', False):
    st.warning("⚠️ Please create schema first!")
    st.info("👉 Go to **Schema Setup** page")
    st.stop()

# Initialize session state
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'total_generated' not in st.session_state:
    st.session_state.total_generated = 0

db_manager = st.session_state.db_connection
tables = st.session_state.tables

# Configuration
st.markdown("## Generation Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    selected_table = st.selectbox("Target Table", options=tables, format_func=lambda x: x.title())

with col2:
    operation = st.selectbox("Operation Type", options=list(UIConfig.OPERATIONS.keys()), 
                            format_func=lambda x: UIConfig.OPERATIONS[x])

with col3:
    batch_size = st.number_input("Batch Size", min_value=1, max_value=10000, value=100)

col1, col2 = st.columns(2)

with col1:
    total_records = st.number_input("Total Records", min_value=1, max_value=1000000, value=1000)

with col2:
    speed = st.slider("Generation Speed (records/sec)", min_value=1, max_value=1000, value=100)

# Control Panel
st.markdown("## Control Panel")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    start_btn = st.button("▶️ Start Generation", use_container_width=True, type="primary", 
                         disabled=st.session_state.is_generating)

with col2:
    stop_btn = st.button("⏸️ Stop", use_container_width=True, 
                        disabled=not st.session_state.is_generating)

with col3:
    if st.button("🔄 Reset Counters", use_container_width=True):
        st.session_state.total_generated = 0
        st.rerun()

if stop_btn:
    st.session_state.is_generating = False
    st.rerun()

# Metrics Dashboard
st.markdown("## Live Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{st.session_state.total_generated}</div>
        <div class="metric-label">Records Generated</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    progress_pct = (st.session_state.total_generated / total_records * 100) if total_records > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{progress_pct:.1f}%</div>
        <div class="metric-label">Progress</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">0</div>
        <div class="metric-label">Current Speed</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    monitor = PerformanceMonitor()
    cpu_usage = monitor.get_cpu_usage()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{cpu_usage:.1f}%</div>
        <div class="metric-label">CPU Usage</div>
    </div>
    """, unsafe_allow_html=True)

# Generation Logic
if start_btn:
    st.session_state.is_generating = True

if st.session_state.is_generating:
    st.markdown("## Generation in Progress...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    generator = SQLDataGenerator()
    remaining = total_records - st.session_state.total_generated
    
    while remaining > 0 and st.session_state.is_generating:
        current_batch = min(batch_size, remaining)
        
        try:
            statements = generator.generate_batch(selected_table, current_batch, operation)
            
            for stmt in statements:
                db_manager.execute_query(stmt)
            
            st.session_state.total_generated += current_batch
            remaining -= current_batch
            
            progress = st.session_state.total_generated / total_records
            progress_bar.progress(progress)
            status_text.text(f"Generated {st.session_state.total_generated}/{total_records} records...")
            
            time.sleep(current_batch / speed)
            
            if remaining <= 0:
                st.session_state.is_generating = False
                st.success(f"✅ Successfully generated {total_records} records!")
                st.balloons()
                break
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.is_generating = False
            break
    
    st.rerun()

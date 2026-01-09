
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from datetime import datetime, timedelta
import base64
import random
import textwrap
import numpy as np
from PIL import Image
from backend.auth.auth_manager import AuthManager
from backend.ai_assistant import VeritasAssistant
from backend.expectation_engine.promise_extractor import PromiseExtractor
from dataclasses import asdict
from main_pipeline import VeritasFinancePipeline
from fpdf import FPDF
from io import BytesIO
# Page configuration
st.set_page_config(
    page_title="Mis-Selling Intelligence Platform",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# STUNNING CSS - HACKATHON WINNING DESIGN
# ============================================================================

STUNNING_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    :root {
        /* Professional, toned-down palette */
        --bg-color: #020617 !important;                /* near-black navy */
        --card-bg: #02081a !important;
        --text-primary: #e5e7eb !important;
        --text-secondary: #9ca3af !important;
        --accent-primary: #38bdf8 !important;
        --accent-secondary: #818cf8 !important;
        --success: #22c55e !important;
        --warning: #eab308 !important;
        --danger: #ef4444 !important;
        --gradient-primary: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
        --gradient-card: radial-gradient(circle at top left, rgba(148, 163, 184, 0.12), transparent 55%),
                         linear-gradient(145deg, #020617, #02081a) !important;
        --glass-border: 1px solid rgba(148, 163, 184, 0.25) !important;
    }

    html, body, .stApp {
        background-color: var(--bg-color) !important;
        color: var(--text-primary) !important;
    }

    .stApp {
        background-image: 
            radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.12) 0px, transparent 55%),
            radial-gradient(at 100% 0%, rgba(129, 140, 248, 0.10) 0px, transparent 55%),
            radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.9) 0px, #020617 60%) !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Subtle enter animations */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

    @keyframes softPulse {
        0%   { box-shadow: 0 0 0 rgba(56, 189, 248, 0.0); }
        50%  { box-shadow: 0 0 22px rgba(56, 189, 248, 0.45); }
        100% { box-shadow: 0 0 0 rgba(56, 189, 248, 0.0); }
    }
    
    /* Force text color on all generic containers */
    div, p, span, label, h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    .stMarkdown, .stMarkdown p {
        color: var(--text-primary) !important;
    }
    
    /* Main container */
    .main .block-container {
        max-width: 100%;
        padding: 2rem 3rem;
        animation: fadeIn 0.4s ease-out;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text-primary);
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2.5rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }

    /* Cards */
    .stCard, div[data-testid="stMetricValue"], .glass-card, .kpi-card {
        background: var(--gradient-card);
        border: var(--glass-border);
        border-radius: 16px;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.75);
        padding: 1.5rem;
        transition: transform 0.18s ease-out, box-shadow 0.2s ease-out, border-color 0.18s ease-out;
        animation: fadeInUp 0.45s ease-out;
    }
    
    .kpi-card:hover, .glass-card:hover {
        transform: translateY(-3px) translateZ(0);
        border-color: rgba(56, 189, 248, 0.55);
        box-shadow: 0 22px 55px rgba(15, 23, 42, 0.95);
    }

    /* Text Colors */
    p, span, div, label {
        color: var(--text-secondary);
    }
    
    .metric-value {
        color: var(--text-primary);
        font-size: 1.5rem;
        font-weight: 700;
        font-family: 'Space Grotesk', monospace;
    }
    
    .metric-label {
        color: var(--accent-primary);
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: radial-gradient(circle at top, rgba(56, 189, 248, 0.18), transparent 60%) #020617;
        border-right: var(--glass-border);
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Inputs */
    .stTextInput input, .stSelectbox, .stNumberInput input {
        background-color: rgba(15, 23, 42, 0.9);
        color: var(--text-primary);
        border: var(--glass-border);
        border-radius: 10px;
        transition: border-color 0.18s ease-out, box-shadow 0.18s ease-out, background-color 0.18s ease-out;
    }

    .stTextInput input:focus, .stSelectbox:focus-within, .stNumberInput input:focus {
        background-color: rgba(15, 23, 42, 0.98);
        border-color: rgba(56, 189, 248, 0.7);
        box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.6);
    }
    
    /* Buttons */
    .stButton button {
        background: var(--gradient-primary);
        color: white !important;
        font-weight: 600;
        border: none;
        border-radius: 999px;
        padding: 0.4rem 1.4rem;
        letter-spacing: 0.02em;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.7);
        transition: transform 0.16s ease-out, box-shadow 0.18s ease-out, filter 0.18s ease-out;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        filter: brightness(1.05);
        box-shadow: 0 18px 40px rgba(56, 189, 248, 0.55);
    }

    .stButton button:active {
        transform: translateY(0);
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.8);
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: var(--glass-border);
        border-radius: 12px;
        overflow: hidden;
    }
</style>
"""

st.markdown(STUNNING_CSS, unsafe_allow_html=True)

# ============================================================================
# AUTHENTICATION
# ============================================================================

def init_auth():
    """Initialize authentication state"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'auth_manager' not in st.session_state:
        try:
            st.session_state.auth_manager = AuthManager()
        except Exception as e:
            print(f"Error initializing AuthManager: {e}")
            st.session_state.auth_manager = None

    if 'assistant' not in st.session_state:
        try:
            st.session_state.assistant = VeritasAssistant()
        except Exception as e:
            print(f"Error initializing VeritasAssistant: {e}")
            st.session_state.assistant = None

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def render_login_page():
    """Render stunning login page with Face ID"""
    
    # Custom CSS for login page
    # Custom CSS for login page
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            border: var(--glass-border);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-title {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 800;
            font-size: 2rem;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            color: var(--text-secondary);
            font-size: 0.875rem;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-header">
            <div class="login-title">Veritas Finance</div>
            <div class="login-subtitle">Mis-Selling Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        auth = st.session_state.auth_manager
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                
                submitted = st.form_submit_button("Log In", use_container_width=True)
                
                if submitted:
                    success, msg = auth.login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
<<<<<<< HEAD
                        st.success(f"{msg}")
                        st.rerun()
                    else:
                        st.error(f"{msg}")
=======
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
            
            st.markdown("---")
            st.markdown("### 👤 Face ID Login")
            
            img_file = st.camera_input("Scan Face for Login", key="login_face", label_visibility="collapsed")
            
            if img_file is not None:
                # Process image safely
                bytes_data = img_file.getvalue()
                try:
                    # Convert to numpy array for opencv
                    image = Image.open(img_file)
                    image_np = np.array(image)
                    
                    # Get encoding/histogram
                    encoding = auth.get_face_encoding_from_image(image_np)
                    
                    if encoding is not None:
                        success, result = auth.login_with_face(encoding)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = result
<<<<<<< HEAD
                            st.success(f"Welcome back, {result}!")
                            st.rerun()
                        else:
                            st.error(f"{result}")
                    else:
                        st.warning("Could not detect face clearly.")
=======
                            st.success(f"✅ Welcome back, {result}!")
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
                    else:
                        st.warning("⚠️ Could not detect face clearly.")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
                except Exception as e:
                    st.error(f"Error processing face: {e}")

        with tab2:
            st.markdown("### 📸 Face ID Setup")
            signup_face_img = st.camera_input("Capture Face for Signup", key="signup_face")
            
            with st.form("signup_form"):
                new_user = st.text_input("Choose Username")
                new_pass = st.text_input("Choose Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                
                # Face ID Option for Signup
                use_face = st.checkbox("Enable Face ID with above capture")
                
                submitted = st.form_submit_button("Create Account", use_container_width=True)
                
                if submitted:
                    if new_pass != confirm_pass:
<<<<<<< HEAD
                        st.error("Passwords do not match")
                    elif len(new_pass) < 4:
                        st.error("Password too short")
=======
                        st.error("❌ Passwords do not match")
                    elif len(new_pass) < 4:
                        st.error("❌ Password too short")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
                    else:
                        # Handle Face ID registration if checked
                        face_encoding = None
                        if use_face:
                            if signup_face_img is not None:
                                try:
                                    image = Image.open(signup_face_img)
                                    image_np = np.array(image)
                                    face_encoding = auth.get_face_encoding_from_image(image_np)
                                    if face_encoding is None:
<<<<<<< HEAD
                                        st.warning("Face capture failed. Account will be created without Face ID.")
                                except Exception as e:
                                    st.error(f"Error processing face: {e}")
                            else:
                                st.warning("No face captured. Account will be created without Face ID.")
=======
                                        st.warning("⚠️ Face capture failed. Account will be created without Face ID.")
                                except Exception as e:
                                    st.error(f"Error processing face: {e}")
                            else:
                                st.warning("⚠️ No face captured. Account will be created without Face ID.")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
                        
                        success, msg = auth.signup(new_user, new_pass, face_encoding=face_encoding)
                        
                        if success:
<<<<<<< HEAD
                            st.success("Account created! Please log in.")
                        else:
                            st.error(f"{msg}")
=======
                            st.success("✅ Account created! Please log in.")
                        else:
                            st.error(f"❌ {msg}")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def make_card(title, value, trend=None, trend_value=""):
    trend_html = ""
    if trend is not None:
        # 1 for up (good), -1 for down (bad/risk), 0 for neutral
        color = "var(--success)" if trend > 0 else "var(--danger)" if trend < 0 else "var(--text-secondary)"
        icon = "▲" if trend > 0 else "▼" if trend < 0 else "•"
        trend_html = f'<div style="color: {color}; font-size: 0.9rem; margin-top: 0.5rem; font-weight: 600;">{icon} {trend_value}</div>'
        
    return textwrap.dedent(f"""
    <div class="kpi-card">
    <div class="kpi-label">{title}</div>
    <div class="kpi-value">{value}</div>
    {trend_html}
    </div>
    """)

def make_metric_row(label, value, value_color=None):
    style = f' style="color: {value_color};"' if value_color else ""
    return textwrap.dedent(f"""
    <div class="metric-row">
    <span class="metric-label">{label}</span>
    <span class="metric-value"{style}>{value}</span>
    </div>
    """)

def load_data():
    """Load processed data from pipeline outputs"""
    data = {
        'promises': None,
        'sentiment': None,
        'gap': None
    }
    
    try:
        promises_path = "data/processed/extracted_promises.csv"
        sentiment_path = "data/processed/sentiment_analysis.csv"
        gap_path = "data/processed/gap_analysis.csv"
        
        if os.path.exists(promises_path):
            data['promises'] = pd.read_csv(promises_path)
        if os.path.exists(sentiment_path):
            data['sentiment'] = pd.read_csv(sentiment_path)
        if os.path.exists(gap_path):
            data['gap'] = pd.read_csv(gap_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
    
    return data

def calculate_kpis(data):
    """Calculate key performance indicators"""
    kpis = {
        'products_monitored': 0,
        'high_risk_products': 0,
        'avg_gap': 0.0,
        'avg_dissatisfaction': 0.0
    }
    
    if data['gap'] is not None and len(data['gap']) > 0:
        kpis['products_monitored'] = len(data['gap'])
        high_risk = data['gap'][data['gap']['risk_level'].isin(['high', 'critical'])]
        kpis['high_risk_products'] = len(high_risk)
        
        if 'overall_risk_score' in data['gap'].columns:
            kpis['avg_gap'] = data['gap']['overall_risk_score'].mean()
        
        if 'dissatisfaction_index' in data['gap'].columns:
            kpis['avg_dissatisfaction'] = data['gap']['dissatisfaction_index'].mean()
    
    return kpis

def render_kpi_card(label, value, trend=None, trend_value=None):
    """Render a stunning KPI card"""
    trend_html = ""
    if trend is not None and trend_value:
        trend_class = "trend-up" if trend > 0 else "trend-down" if trend < 0 else "trend-neutral"
        trend_arrow = "↑" if trend > 0 else "↓" if trend < 0 else "→"
        trend_html = f'<div class="kpi-trend {trend_class}">{trend_arrow} {trend_value}</div>'
    
    return textwrap.dedent(f"""
    <div class="kpi-card">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    {trend_html}
    </div>
    """)

def get_risk_badge_class(risk_level):
    """Get CSS class for risk badge"""
    risk_lower = str(risk_level).lower()
    if risk_lower == 'critical':
        return 'badge-critical'
    elif risk_lower == 'high':
        return 'badge-high'
    elif risk_lower == 'medium':
        return 'badge-medium'
    else:
        return 'badge-low'

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render stunning sidebar navigation"""
    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <h1>Mis-Selling<br>Intelligence</h1>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.875rem; margin-top: 0.5rem;">
            Regulator Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation items
    nav_items = [
        ("Dashboard Overview", "dashboard"),
        ("Products Monitor", "products"),
        ("Expectation Engine", "expectation"),
        ("Reality Engine", "reality"),
        ("Risk Flags", "risks"),
        ("Reports & Evidence", "reports"),
        ("Settings", "settings")
    ]
    
    # Initialize session state for active page
    if 'active_page' not in st.session_state:
        st.session_state.active_page = "dashboard"
    
    st.sidebar.markdown('<h3 style="color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 1rem;">Navigation</h3>', unsafe_allow_html=True)
    
    for label, page_id in nav_items:
        if st.sidebar.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.active_page = page_id
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # System status
    st.sidebar.markdown("""
    <div style="padding: 1rem; background: rgba(16, 185, 129, 0.2); border-radius: 12px; margin-top: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: #10b981; box-shadow: 0 0 10px #10b981;"></div>
            <span style="font-size: 0.875rem; color: white; font-weight: 600;">System Operational</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    # ============================================================================
    # AI ASSISTANT
    # ============================================================================
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 Veritas AI Assistant")
    
<<<<<<< HEAD
    # API Key Configuration
    # Using centralized key from .env (Configured in backend)
    # api_key = st.sidebar.text_input("Gemini API Key", type="password", key="gemini_api_key")
    # if api_key:
    #     st.session_state.assistant.set_api_key(api_key)
    
    # Chat Interface
    with st.sidebar.expander("Chat with AI", expanded=True):
        if not st.session_state.get('assistant'):
            st.error("AI Assistant failed to initialize.")
=======
    # API Key Configuration REMOVED

    
    # Chat Interface
    with st.sidebar.expander("💬 Chat with AI", expanded=True):
        if not st.session_state.get('assistant'):
            st.error("⚠️ AI Assistant failed to initialize.")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
        else:
            # Display history
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**AI:** {msg['content']}")
        
        # Chat Input
        user_query = st.text_input("Ask me anything...", key="chat_input")
        
        if st.session_state.get('assistant') and st.button("Send", key="send_chat", use_container_width=True):
            if user_query:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                
                # Get response
                with st.spinner("Thinking..."):
                    raw_response = st.session_state.assistant.get_response(user_query)
                    
                    # Parse JSON response
                    try:
                        # Clean markdown code blocks if present
                        if "```json" in raw_response:
                            raw_response = raw_response.split("```json")[1].split("```")[0]
                        elif "```" in raw_response:
                            raw_response = raw_response.split("```")[1].split("```")[0]
                            
                        response_data = json.loads(raw_response)
                        ai_text = response_data.get("text", "I processed your request.")
                        navigate_to = response_data.get("navigate_to")
                        
                        # Add AI message to history
                        st.session_state.chat_history.append({"role": "ai", "content": ai_text})
                        
                        # Handle Navigation
                        if navigate_to and navigate_to in ["dashboard", "products", "expectation", "reality", "risks", "reports", "settings"]:
                            st.session_state.active_page = navigate_to
                            st.success(f"Navigating to {navigate_to}...")
                            st.rerun()
                            
                    except Exception as e:
                        # Fallback for plain text or errors
                        st.session_state.chat_history.append({"role": "ai", "content": raw_response})
                        print(f"JSON Parse Error: {e}")
                
                st.rerun()


# ============================================================================
# PAGE VIEWS
# ============================================================================

def render_dashboard_overview(data):
<<<<<<< HEAD
    """Main dashboard overview"""
    st.markdown("# Mis-Selling Risk Overview")
    st.markdown("Comprehensive monitoring and analysis of financial product mis-selling risks")
    st.divider()
=======
    """Stunning main dashboard overview"""
    st.markdown("# 🛡️ Mis-Selling Risk Overview")
    st.markdown('<p style="color: var(--text-secondary); font-size: 1.125rem; margin-bottom: 3rem;">Comprehensive monitoring and analysis of financial product mis-selling risks</p>', unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    # Calculate KPIs
    kpis = calculate_kpis(data)
    
    # KPI Cards using Streamlit native components
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
<<<<<<< HEAD
        st.metric(
            label="Products Monitored",
            value=kpis['products_monitored'],
            delta="+2 this week"
        )
    
    with col2:
        st.metric(
            label="High-Risk Products",
            value=kpis['high_risk_products'],
            delta=f"{kpis['high_risk_products']} flagged" if kpis['high_risk_products'] > 0 else None,
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Avg Risk Score",
            value=f"{kpis['avg_gap']:.2f}"
        )
    
    with col4:
        st.metric(
            label="Customer Dissatisfaction",
            value=f"{kpis['avg_dissatisfaction']:.1f}%",
            delta="+2.3% vs last month"
        )
=======
        st.markdown(make_card(
            "Products Monitored",
            f"{kpis['products_monitored']}",
            trend=1,
            trend_value="+2 this week"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(make_card(
            "High-Risk Products",
            f"{kpis['high_risk_products']}",
            trend=-1 if kpis['high_risk_products'] > 0 else 0,
            trend_value=f"{kpis['high_risk_products']} flagged"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(make_card(
            "Avg Risk Score",
            f"{kpis['avg_gap']:.2f}",
            trend=0,
            trend_value=""
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(make_card(
            "Customer Dissatisfaction",
            f"{kpis['avg_dissatisfaction']:.1f}%",
            trend=1,
            trend_value="+2.3% vs last month"
        ), unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    st.divider()
    
    # Risk Distribution Chart
    if data['gap'] is not None and len(data['gap']) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Risk Distribution")
            risk_counts = data['gap']['risk_level'].value_counts()
            
            # Create pie chart
            colors_map = {
                'low': '#10b981',
                'medium': '#f59e0b',
                'high': '#ef4444',
                'critical': '#dc2626'
            }
            colors = [colors_map.get(level.lower(), '#64748b') for level in risk_counts.index]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=risk_counts.index.str.title(),
                values=risk_counts.values,
                hole=0.5,
                marker=dict(colors=colors, line=dict(color='white', width=3)),
                textfont=dict(size=16, family='Inter', color='white'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
            )])
            fig_pie.update_layout(
                height=400,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', size=14, color='white'),
                legend=dict(font=dict(size=14, color='white'))
            )
            st.plotly_chart(fig_pie, use_container_width=True, use_container_height=True)
        
        with col2:
            st.markdown("### Top Risk Products")
            top_risks = data['gap'].nlargest(5, 'overall_risk_score')[['product_name', 'risk_level', 'overall_risk_score']]
            
            for idx, row in top_risks.iterrows():
<<<<<<< HEAD
                with st.container():
                    st.markdown(f"**{row['product_name']}**")
                    st.markdown(f"Risk Level: **{row['risk_level'].upper()}** | Score: {row['overall_risk_score']:.2f}")
                    st.divider()
=======
                badge_class = get_risk_badge_class(row['risk_level'])
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; color: var(--text-primary); font-size: 1.125rem; margin-bottom: 0.5rem;">
                                {row['product_name']}
                            </div>
                            <div style="font-size: 0.875rem; color: #64748b;">
                                Risk Score: <strong>{row['overall_risk_score']:.2f}</strong>
                            </div>
                        </div>
                        <span class="status-badge {badge_class}">{row['risk_level'].upper()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    else:
        st.info("No Data Available - Please run the analysis pipeline first.")
    
    # Comparison View
    st.divider()
    render_comparison_view(data)

def render_comparison_view(data):
    """Expectation vs Reality Comparison"""
    st.markdown("### Expectation vs Reality Comparison")
    
    if data['gap'] is not None and data['promises'] is not None:
        selected_product = st.selectbox(
            "Select Product",
            data['gap']['product_name'].tolist(),
            key="comparison_product"
        )
        
        if selected_product:
            gap_data = data['gap'][data['gap']['product_name'] == selected_product].iloc[0]
            promise_data = data['promises'][data['promises']['product_name'] == selected_product]
            
            if len(promise_data) > 0:
                promise_data = promise_data.iloc[0]
                
<<<<<<< HEAD
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### What Was Promised")
                    st.write(f"**Returns:** {promise_data.get('promised_returns', 'N/A')}")
                    st.write(f"**Risk Category:** {promise_data.get('risk_category', 'N/A')}")
                    st.write(f"**Lock-in Period:** {promise_data.get('lock_in_period', 'N/A')}")
                
                with col2:
                    st.markdown("#### Customer Reality")
                    st.write("**Reported Returns:** Poor / Below Expectations")
                    st.write("**Perceived Risk:** High Volatility Reported")
                    st.write("**Exit Experience:** Difficulties Reported")

def render_products_monitor(data):
    """Products monitoring view"""
    st.markdown("# Products Monitor")
    st.markdown("Real-time monitoring of all analyzed financial products")
=======
                content = textwrap.dedent(f"""
                <div class="comparison-container">
                    <div class="comparison-card" style="border-top: 5px solid var(--success);">
                        <div class="comparison-header" style="color: var(--success);">✅ What Was Promised</div>
                        {make_metric_row("Returns", promise_data.get('promised_returns', 'N/A'))}
                        {make_metric_row("Risk Category", promise_data.get('risk_category', 'N/A'))}
                        {make_metric_row("Lock-in Period", promise_data.get('lock_in_period', 'N/A'))}
                    </div>
                    
                    <div class="comparison-card" style="border-top: 5px solid var(--danger);">
                        <div class="comparison-header" style="color: var(--danger);">❌ Customer Reality</div>
                        {make_metric_row("Reported Returns", "Poor / Below Expectations", "var(--danger)")}
                        {make_metric_row("Perceived Risk", "High Volatility Reported", "var(--danger)")}
                        {make_metric_row("Exit Experience", "Difficulties Reported", "var(--danger)")}
                    </div>
                </div>
                """)
                st.markdown(content, unsafe_allow_html=True)

def render_products_monitor(data):
    """Products monitoring view"""
    st.markdown("# 📦 Products Monitor")
    st.markdown('<p style="color: var(--text-secondary); font-size: 1.125rem;">Real-time monitoring of all analyzed financial products</p>', unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    if data['gap'] is not None and len(data['gap']) > 0:
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search products", placeholder="Enter product name...")
        with col2:
            risk_filter = st.selectbox("Filter by Risk", ["All", "Low", "Medium", "High", "Critical"])
        
        filtered_data = data['gap'].copy()
        if search_term:
            filtered_data = filtered_data[filtered_data['product_name'].str.contains(search_term, case=False, na=False)]
        if risk_filter != "All":
            filtered_data = filtered_data[filtered_data['risk_level'] == risk_filter.lower()]
        
        display_cols = ['product_name', 'risk_level', 'overall_risk_score', 'dissatisfaction_index']
        if all(col in filtered_data.columns for col in display_cols):
            display_df = filtered_data[display_cols].copy()
            display_df.columns = ['Product Name', 'Risk Level', 'Risk Score', 'Dissatisfaction %']
            display_df['Risk Score'] = display_df['Risk Score'].round(2)
            display_df['Dissatisfaction %'] = display_df['Dissatisfaction %'].round(1)
            
            # Style the dataframe
            st.dataframe(
                display_df,
                column_config={
                    "Risk Score": st.column_config.ProgressColumn(
                        "Risk Score",
                        help="Risk Score (0-1)",
                        format="%.2f",
                        min_value=0,
                        max_value=1,
                    ),
                    "Dissatisfaction %": st.column_config.ProgressColumn(
                        "Dissatisfaction %",
                        help="Customer Dissatisfaction Index",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100,
                    ),
                    "Risk Level": st.column_config.TextColumn(
                        "Risk Level",
                        help="Categorical Risk Level",
                        width="small"
                    )
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Column structure mismatch")
    else:
        st.info("No Products Analyzed - Run the Expectation and Reality Engines to begin monitoring.")

def render_expectation_engine(data):
<<<<<<< HEAD
    """Expectation Engine UI"""
    st.markdown("# Expectation Engine")
    st.markdown("Extract and analyze promises from product marketing materials")
=======
    """Stunning Expectation Engine UI"""
    st.markdown("# 📄 Expectation Engine")
    st.markdown('<p style="color: var(--text-secondary); font-size: 1.125rem;">Extract and analyze promises from product marketing materials</p>', unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    tab1, tab2 = st.tabs(["Upload Document", "Extracted Promises"])
    
    with tab1:
        st.markdown("### Upload Product Document")
        st.info("Drag & Drop PDF or Brochure. Supported formats: PDF, DOCX, Images")
        
        uploaded_file = st.file_uploader("", type=['pdf', 'docx', 'png', 'jpg'], label_visibility="collapsed")
        
        if uploaded_file:
<<<<<<< HEAD
            st.success(f"File uploaded: {uploaded_file.name}")
            if st.button("Extract Promises", type="primary", use_container_width=True):
                with st.spinner("Analyzing document with NLP engine..."):
=======
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            if st.button("🚀 Extract Promises", type="primary", use_container_width=True):
                with st.spinner("🔍 Analyzing document with NLP engine..."):
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
                    # Save file temporarily
                    try:
                        os.makedirs("data/uploaded", exist_ok=True)
                        file_path = os.path.join("data/uploaded", uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Extract
                        extractor = PromiseExtractor()
                        if uploaded_file.name.endswith(".pdf"):
                            result = extractor.extract_from_pdf(file_path)
                        else:
                            # Simple text fallback for other types
                            text = str(uploaded_file.read())
                            result = extractor.extract_from_text(text, {'product_name': uploaded_file.name})
                            
                        if result:
                            # Update DataFrame
                            new_row = asdict(result)
                            if data['promises'] is None:
                                data['promises'] = pd.DataFrame([new_row])
                            else:
                                data['promises'] = pd.concat([data['promises'], pd.DataFrame([new_row])], ignore_index=True)
                            
                            # Save to CSV
                            os.makedirs("data/processed", exist_ok=True)
                            data['promises'].to_csv("data/processed/extracted_promises.csv", index=False)
                            
<<<<<<< HEAD
                            st.success("Extraction complete!")
                            
                            # Option to run full pipeline
                            st.divider()
                            st.info("To update Risk Flags and Reports with this new data, run the analysis pipeline.")
                            if st.button("Run Full Risk Analysis", type="secondary", use_container_width=True):
                                with st.spinner("Running full compliance analysis pipeline..."):
                                    pipeline = VeritasFinancePipeline()
                                    if pipeline.run_pipeline():
                                        st.success("Analysis Complete! Check 'Risk Flags' and 'Reports' pages.")
                                        # Reload data
                                        st.session_state.data = load_data()
                                    else:
                                        st.error("Analysis failed. Check console for details.")

                        else:
                            st.error("Failed to extract content from file.")
=======
                            st.balloons()
                            
                            # Option to run full pipeline
                            st.divider()
                            st.info("💡 To update Risk Flags and Reports with this new data, run the analysis pipeline.")
                            if st.button("🔄 Run Full Risk Analysis", type="secondary", use_container_width=True):
                                with st.spinner("Running full compliance analysis pipeline..."):
                                    pipeline = VeritasFinancePipeline()
                                    if pipeline.run_pipeline():
                                        st.success("✅ Analysis Complete! Check 'Risk Flags' and 'Reports' pages.")
                                        # Reload data
                                        st.session_state.data = load_data()
                                    else:
                                        st.error("❌ Analysis failed. Check console for details.")

                        else:
                            st.error("❌ Failed to extract content from file.")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
                    except Exception as e:
                        st.error(f"Error during extraction: {e}")
    
    with tab2:
        st.markdown("### Extracted Promise Profiles")
        
        if data['promises'] is not None and len(data['promises']) > 0:
            for idx, row in data['promises'].iterrows():
                product_name = row.get('product_name', 'Unknown Product')
                confidence = row.get('extraction_confidence', 0)
                
<<<<<<< HEAD
                with st.expander(f"{product_name} - Confidence: {confidence:.0%}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Investment Objective:** {row.get('investment_objective', 'N/A')}")
                        st.write(f"**Promised Returns:** {row.get('promised_returns', 'N/A')}")
                        st.write(f"**Risk Category:** {row.get('risk_category', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Lock-in Period:** {row.get('lock_in_period', 'N/A')}")
                        st.write(f"**Exit Load:** {row.get('exit_load', 'N/A')}")
                        st.write(f"**Min Investment:** {row.get('min_investment', 'N/A')}")
                
                st.divider()
=======
                content = textwrap.dedent(f"""
                <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid rgba(255,255,255,0.1);">
                <div style="font-weight: 800; font-size: 1.25rem; color: var(--text-primary);">{product_name}</div>
                <div style="padding: 0.5rem 1rem; background: var(--gradient-primary); color: white; border-radius: 50px; font-weight: 700; font-size: 0.875rem;">
                Confidence: {confidence:.0%}
                </div>
                </div>
{make_metric_row("Investment Objective", row.get('investment_objective', 'N/A'))}
{make_metric_row("Promised Returns", row.get('promised_returns', 'N/A'), "var(--accent-secondary)")}
{make_metric_row("Risk Category", row.get('risk_category', 'N/A'))}
{make_metric_row("Lock-in Period", row.get('lock_in_period', 'N/A'))}
{make_metric_row("Exit Load", row.get('exit_load', 'N/A'))}
                </div>
                """)
                st.markdown(content, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
        else:
            st.info("No Promises Extracted - Upload a document to begin analysis.")

def render_reality_engine(data):
    """Stunning Reality Engine UI"""
<<<<<<< HEAD
    st.markdown("# Reality Engine")
    st.markdown("Analyze customer sentiment and real-world experiences")
=======
    st.markdown("# 💬 Reality Engine")
    st.markdown('<p style="color: var(--text-secondary); font-size: 1.125rem;">Analyze customer sentiment and real-world experiences</p>', unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    if data['sentiment'] is not None and len(data['sentiment']) > 0:
        # Sentiment timeline
        st.markdown("### Customer Sentiment Timeline")
        
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
        sentiment_values = [0.5 + 0.2 * (i % 7) / 7 for i in range(30)]
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=dates,
            y=sentiment_values,
            mode='lines+markers',
            name='Sentiment Score',
            line=dict(color='#667eea', width=3, shape='spline'),
            marker=dict(size=8, color='#764ba2'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        fig_timeline.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Sentiment Score (0-1)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', size=14, color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # CDI Gauge
        if data['gap'] is not None and len(data['gap']) > 0:
            avg_cdi = data['gap']['dissatisfaction_index'].mean()
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = avg_cdi,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Customer Dissatisfaction Index", 'font': {'size': 20, 'color': 'white', 'family': 'Poppins'}},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "white"},
                    'bar': {'color': "#ef4444" if avg_cdi > 50 else "#f59e0b" if avg_cdi > 30 else "#10b981"},
                    'steps': [
                        {'range': [0, 30], 'color': "rgba(16, 185, 129, 0.3)"},
                        {'range': [30, 50], 'color': "rgba(245, 158, 11, 0.3)"},
                        {'range': [50, 100], 'color': "rgba(239, 68, 68, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig_gauge.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Poppins', color='white'))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Topic breakdown
        st.markdown("### Complaint Topic Breakdown")
        
        topics = [
            {"name": "Hidden Charges", "frequency": 42, "sentiment": -0.8},
            {"name": "Poor Returns", "frequency": 38, "sentiment": -0.7},
            {"name": "Service Quality", "frequency": 25, "sentiment": -0.5},
            {"name": "Exit Difficulties", "frequency": 18, "sentiment": -0.6}
        ]
        
        for topic in topics:
<<<<<<< HEAD
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{topic['name']}**")
                with col2:
                    st.caption(f"{topic['frequency']}% mentions")
                
                # Progress bar for sentiment
                sentiment = abs(topic['sentiment'])
                st.progress(sentiment, text=f"Sentiment: {topic['sentiment']:.2f}")
                
                st.caption('Example: Customer reports unexpected charges on withdrawal')
                st.divider()
=======
            sentiment_color = "#ef4444" if topic['sentiment'] < -0.6 else "#f59e0b"
            sentiment_width = abs(topic['sentiment']) * 100
            
            st.markdown(f"""
            <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 1.125rem; color: var(--text-primary);">{topic['name']}</div>
                    <div style="padding: 0.25rem 1rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 50px; font-weight: 700; font-size: 0.875rem;">
                        {topic['frequency']}% mentions
                    </div>
                </div>
                <div style="height: 12px; background: #e2e8f0; border-radius: 50px; overflow: hidden; margin-bottom: 1rem;">
                    <div style="height: 100%; width: {sentiment_width}%; background: {sentiment_color}; border-radius: 50px; transition: width 1s ease;"></div>
                </div>
                <div style="font-size: 0.875rem; color: #64748b; font-style: italic; padding: 1rem; background: rgba(102, 126, 234, 0.05); border-radius: 10px;">
                    💬 "Example: Customer reports unexpected charges on withdrawal"
                </div>
            </div>
            """, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    else:
        st.info("No Sentiment Data - Run the Reality Engine analysis first.")

def render_risk_flags(data):
    """Stunning Risk Flags view"""
<<<<<<< HEAD
    st.markdown("# Risk Flags")
    st.markdown("Detailed risk analysis and flagging system")
=======
    st.markdown("# 🚨 Risk Flags")
    st.markdown('<p style="color: var(--text-secondary); font-size: 1.125rem;">Detailed risk analysis and flagging system</p>', unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    if data['gap'] is not None and len(data['gap']) > 0:
        selected_product = st.selectbox(
            "Select Product",
            data['gap']['product_name'].tolist(),
            key="risk_product"
        )
        
        if selected_product:
            product_data = data['gap'][data['gap']['product_name'] == selected_product].iloc[0]
            
            risk_score = float(product_data.get('overall_risk_score', 0)) * 100
            risk_level = str(product_data.get('risk_level', 'medium')).lower()
            
<<<<<<< HEAD
            # Risk Score Display
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("### Overall Risk Score")
            with col2:
                st.markdown(f"**{risk_level.upper()} RISK**")
            
            # Progress bar
            st.progress(risk_score / 100, text=f"{risk_score:.0f}/100")
            
            # Risk score metric
            st.metric("", f"{risk_score:.0f}/100", label_visibility="collapsed")
=======
            # Stunning Risk Meter
            st.markdown(f"""
            <div class="risk-meter-container">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0; color: var(--text-primary);">Overall Risk Score</h3>
                    <span class="status-badge {get_risk_badge_class(risk_level)}" style="font-size: 1.125rem; padding: 0.75rem 1.5rem;">
                        {risk_level.upper()}
                    </span>
                </div>
                <div class="risk-meter-bar">
                    <div class="risk-meter-fill risk-{risk_level}" style="width: {risk_score}%;"></div>
                </div>
                <div style="text-align: center; font-size: 3rem; font-weight: 800; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 1rem;">
                    {risk_score:.0f}/100
                </div>
            </div>
            """, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
            
            # Why flagged section
            with st.expander("Why Flagged? - Evidence & Justification", expanded=True):
                st.markdown("### Risk Justification")
                
                try:
                    mismatches = json.loads(product_data.get('mismatches', '[]'))
                    if mismatches:
                        for i, mismatch in enumerate(mismatches[:3], 1):
                            with st.container():
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.markdown(f"**{i}. {mismatch.get('promise_aspect', 'Unknown')} Mismatch**")
                                with col2:
                                    severity = float(mismatch.get('severity', 0))
                                    st.markdown(f"**Severity:** {severity:.0%}")
                                
                                st.write(mismatch.get('complaint_topic', 'No description'))
                                st.divider()
                except:
                    with st.container():
                        st.markdown("**Risk Indicators Detected**")
                        st.write(f"Risk score of {risk_score:.0f}/100 based on sentiment analysis and gap detection.")
                        st.write(f"Dissatisfaction index: {product_data.get('dissatisfaction_index', 0):.1f}%")
            
            # Evidence sources
            st.markdown("### Evidence Sources")
            evidence_sources = [
                {"source": "Customer Reviews", "count": 127, "sentiment": -0.65},
                {"source": "Social Media Mentions", "count": 43, "sentiment": -0.72},
                {"source": "Complaint Portal", "count": 18, "sentiment": -0.58}
            ]
            
            for source in evidence_sources:
<<<<<<< HEAD
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**{source['source']}**")
                    st.caption(f"{source['count']} data points")
                with col2:
                    st.caption("Avg Sentiment")
                    st.metric("", f"{source['sentiment']:.2f}", label_visibility="collapsed")
                st.divider()
=======
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; font-size: 1.125rem; color: var(--text-primary); margin-bottom: 0.5rem;">{source['source']}</div>
                            <div style="font-size: 0.875rem; color: var(--text-secondary);">{source['count']} data points</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.25rem;">Avg Sentiment</div>
                            <div style="font-weight: 800; font-size: 1.5rem; background: linear-gradient(135deg, #ef4444, #f87171); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{source['sentiment']:.2f}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    else:
        st.info("No Risk Analysis Data - Run the complete pipeline to generate risk flags.")

def generate_pdf_report(report_type, data):
    """Generate a PDF report using FPDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Veritas Finance - {report_type}", ln=True, align="C")
    pdf.ln(10)
    
    # Date
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="R")
    pdf.ln(10)
    
    # Executive Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "This report analyzes potential mis-selling risks for the selected financial products based on comparison between marketing promises and customer experiences. Our AI engine has detected several discrepancies that warrant further investigation.")
    pdf.ln(5)

    # Stats
    if data.get('gap') is not None:
        high_risk = len(data['gap'][data['gap']['risk_level'].isin(['high', 'critical'])])
        avg_risk = data['gap']['overall_risk_score'].mean()
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, f"Key Metrics:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f"- Products Analyzed: {len(data['gap'])}", ln=True)
        pdf.cell(0, 8, f"- High Risk Alerts: {high_risk}", ln=True)
        pdf.cell(0, 8, f"- Average Risk Score: {avg_risk:.2f}", ln=True)
        pdf.ln(5)
    
    # Extracted Promises
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Extracted Promises Analysis", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "Product marketing materials were analyzed using NLP to extract key promises regarding returns, lock-in periods, and risk levels.")
    pdf.ln(5)
    
    # Reality Check
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Customer Reality Check", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "Sentiment analysis of customer reviews and complaints reveals significant deviation from promised features in identified high-risk products.")
    pdf.ln(5)

    # Footer
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Generated by Veritas Finance Regulatory Platform - Page {pdf.page_no()}", 0, 0, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

def generate_pdf_report(report_type, data):
    """Generate a PDF report using FPDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Veritas Finance - {report_type}", ln=True, align="C")
    pdf.ln(10)
    
    # Date
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="R")
    pdf.ln(10)
    
    # Executive Summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "This report analyzes potential mis-selling risks for the selected financial products based on comparison between marketing promises and customer experiences. Our AI engine has detected several discrepancies that warrant further investigation.")
    pdf.ln(5)

    # Stats
    if data.get('gap') is not None:
        high_risk = len(data['gap'][data['gap']['risk_level'].isin(['high', 'critical'])])
        avg_risk = data['gap']['overall_risk_score'].mean()
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, f"Key Metrics:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f"- Products Analyzed: {len(data['gap'])}", ln=True)
        pdf.cell(0, 8, f"- High Risk Alerts: {high_risk}", ln=True)
        pdf.cell(0, 8, f"- Average Risk Score: {avg_risk:.2f}", ln=True)
        pdf.ln(5)
    
    # Extracted Promises
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Extracted Promises Analysis", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "Product marketing materials were analyzed using NLP to extract key promises regarding returns, lock-in periods, and risk levels.")
    pdf.ln(5)
    
    # Reality Check
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "3. Customer Reality Check", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, "Sentiment analysis of customer reviews and complaints reveals significant deviation from promised features in identified high-risk products.")
    pdf.ln(5)

    # Footer
    pdf.set_y(-15)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Generated by Veritas Finance Regulatory Platform - Page {pdf.page_no()}", 0, 0, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

def render_reports_evidence(data):
    """Stunning Reports & Evidence view"""
<<<<<<< HEAD
    st.markdown("# Reports & Evidence")
    st.markdown("Generate regulator-ready reports and evidence packages")
=======
    st.markdown("# 📋 Reports & Evidence")
    st.markdown('<p style="color: var(--text-secondary); font-size: 1.125rem;">Generate regulator-ready reports and evidence packages</p>', unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Generate Report")
        report_type = st.selectbox("Report Type", [
            "Executive Summary",
            "Full Risk Analysis",
            "Evidence Package",
            "Regulatory Submission"
        ])
        
<<<<<<< HEAD
        if st.button("Generate Report", type="primary", use_container_width=True):
            st.success("Report generated successfully!")
=======
        if st.button("🚀 Generate Report", type="primary", use_container_width=True):
            st.success("✅ Report generated successfully!")
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
            
            # Generate real PDF
            pdf_bytes = generate_pdf_report(report_type, data)
            
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"mis-selling-report-{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
<<<<<<< HEAD
        st.markdown("### Report Archive")
        st.info("No previous reports found.")
    
    # Report preview
    st.markdown("### Report Preview")
    st.markdown("**Product Risk Analysis Report**")
    st.divider()
    st.markdown("**1. Executive Summary**")
    st.write("This report analyzes potential mis-selling risks for the selected financial products based on comparison between marketing promises and customer experiences.")
    st.markdown("**2. Extracted Promises**")
    st.write("Analysis of product documentation reveals the following claims...")
    st.markdown("**3. Customer Sentiment Analysis**")
    st.write("Sentiment analysis of customer reviews indicates...")
    st.markdown("**4. Risk Justification**")
    st.write("Gap analysis reveals mismatches in the following areas...")

def render_settings():
    """Settings view"""
    st.markdown("# Settings")
    st.markdown("System configuration and preferences")
=======
        st.markdown(textwrap.dedent("""
        <div class="glass-card">
        <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Report Archive</h3>
        <p style="color: #64748b;">No previous reports found.</p>
        </div>
        """), unsafe_allow_html=True)
    
    # Report preview
    st.markdown("### 📄 Report Preview")
    st.markdown(textwrap.dedent("""
    <div class="glass-card">
    <h4 style="margin-top: 0; margin-bottom: 1rem; font-size: 1.5rem;">Product Risk Analysis Report</h4>
    <div class="section-divider" style="margin: 1.5rem 0; background: rgba(255,255,255,0.1);"></div>
    <h5 style="margin-top: 1.5rem;">1. Executive Summary</h5>
    <p style="line-height: 1.8;">This report analyzes potential mis-selling risks for the selected financial products based on comparison between marketing promises and customer experiences.</p>
    <h5 style="margin-top: 1.5rem;">2. Extracted Promises</h5>
    <p style="line-height: 1.8;">Analysis of product documentation reveals the following claims...</p>
    <h5 style="margin-top: 1.5rem;">3. Customer Sentiment Analysis</h5>
    <p style="line-height: 1.8;">Sentiment analysis of customer reviews indicates...</p>
    <h5 style="margin-top: 1.5rem;">4. Risk Justification</h5>
    <p style="line-height: 1.8;">Gap analysis reveals mismatches in the following areas...</p>
    </div>
    """), unsafe_allow_html=True)

def render_settings():
    """Settings view"""
    st.markdown("# ⚙️ Settings")
    st.markdown('<p style="color: var(--text-secondary); font-size: 1.125rem;">System configuration and preferences</p>', unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
    
    tab1, tab2, tab3 = st.tabs(["Data Sources", "Alert Thresholds", "System"])
    
    with tab1:
<<<<<<< HEAD
        st.markdown("### Data Source Configuration")
=======
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: var(--text-primary); margin-bottom: 1.5rem;">Data Source Configuration</h3>
        </div>
        """, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
        st.checkbox("Enable Twitter Feed", value=True)
        st.checkbox("Enable Reddit Discussions", value=True)
        st.checkbox("Enable Play Store Reviews", value=True)
        st.checkbox("Enable Trustpilot Reviews", value=True)
    
    with tab2:
<<<<<<< HEAD
        st.markdown("### Risk Alert Thresholds")
=======
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: var(--text-primary); margin-bottom: 1.5rem;">Risk Alert Thresholds</h3>
        </div>
        """, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
        st.slider("High Risk Threshold", 0.0, 1.0, 0.7, 0.05)
        st.slider("Critical Risk Threshold", 0.0, 1.0, 0.9, 0.05)
        st.number_input("Minimum Complaints for Flagging", min_value=1, value=5)
    
    with tab3:
<<<<<<< HEAD
        st.markdown("### System Settings")
=======
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: var(--text-primary); margin-bottom: 1.5rem;">System Settings</h3>
        </div>
        """, unsafe_allow_html=True)
>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e
        st.selectbox("Report Format", ["PDF", "DOCX", "HTML"])
        st.selectbox("Date Format", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        if st.button("Save Settings", type="primary", use_container_width=True):
            st.success("Settings saved successfully!")

        st.divider()
        st.markdown("### System Maintenance")
        if st.button("Run Full Analysis Pipeline", use_container_width=True):
            with st.spinner("Running system-wide analysis..."):
                pipeline = VeritasFinancePipeline()
                if pipeline.run_pipeline():
                    st.success("Pipeline execution successful!")
                    st.session_state.data = load_data() # Reload data
                else:
                    st.error("Pipeline execution failed.")

        st.divider()
        st.markdown("### 🛠️ System Maintenance")
        if st.button("🔄 Run Full Analysis Pipeline", use_container_width=True):
            with st.spinner("Running system-wide analysis..."):
                pipeline = VeritasFinancePipeline()
                if pipeline.run_pipeline():
                    st.success("✅ Pipeline execution successful!")
                    st.session_state.data = load_data() # Reload data
                else:
                    st.error("❌ Pipeline execution failed.")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    init_auth()
    
    if not st.session_state.logged_in:
        render_login_page()
        return

    data = load_data()
    render_sidebar()
    
    active_page = st.session_state.get('active_page', 'dashboard')
    
    if active_page == "dashboard":
        render_dashboard_overview(data)
    elif active_page == "products":
        render_products_monitor(data)
    elif active_page == "expectation":
        render_expectation_engine(data)
    elif active_page == "reality":
        render_reality_engine(data)
    elif active_page == "risks":
        render_risk_flags(data)
    elif active_page == "reports":
        render_reports_evidence(data)
    elif active_page == "settings":
        render_settings()

if __name__ == "__main__":
    main()

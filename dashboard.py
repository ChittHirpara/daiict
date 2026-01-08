# dashboard.py - AI Regulatory Command Center
# Next-generation intelligence interface for financial mis-selling detection

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from datetime import datetime, timedelta
import random
import numpy as np

# Page configuration
st.set_page_config(
    page_title="VERITAS - AI Regulatory Command Center",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# COMMAND CENTER CSS - Regulator-Grade Design
# ============================================================================

COMMAND_CENTER_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --bg-primary: #0a0e1a;
        --bg-secondary: #141b2d;
        --bg-tertiary: #1a2332;
        
        --text-primary: #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        
        --accent-green: #10b981;
        --accent-amber: #f59e0b;
        --accent-red: #ef4444;
        
        --border-color: rgba(148, 163, 184, 0.1);
        --glow-active: rgba(16, 185, 129, 0.3);
    }
    
    .stApp {
        background: var(--bg-primary);
        background-image: 
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(148, 163, 184, 0.02) 2px,
                rgba(148, 163, 184, 0.02) 4px
            );
        font-family: 'Inter', 'IBM Plex Sans', sans-serif;
        color: var(--text-primary);
    }
    
    /* Subtle noise texture overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main content */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1800px;
        position: relative;
        z-index: 1;
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Sidebar - Minimal Command-Grade */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
        box-shadow: 2px 0 20px rgba(0, 0, 0, 0.5);
        min-width: 200px;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary);
    }
    
    /* Sidebar brand */
    .sidebar-brand {
        padding: 1.5rem 1rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    
    .sidebar-brand h1 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.5px;
        margin: 0;
        text-transform: uppercase;
    }
    
    .sidebar-brand p {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
        font-weight: 400;
    }
    
    /* Sidebar navigation buttons */
    .sidebar-nav {
        padding: 0 0.5rem;
    }
    
    .nav-item {
        position: relative;
        margin: 0.25rem 0;
    }
    
    .nav-item-active::before {
        content: '';
        position: absolute;
        left: -0.5rem;
        top: 0;
        bottom: 0;
        width: 3px;
        background: var(--accent-green);
        box-shadow: 0 0 8px var(--glow-active);
    }
    
    /* Command center header */
    .command-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    
    .command-title {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }
    
    .situation-bar {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.375rem 0.75rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        font-weight: 500;
    }
    
    .status-pill-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent-green);
        box-shadow: 0 0 8px var(--accent-green);
    }
    
    /* KPI Cards - Data-Driven */
    .kpi-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 1.25rem;
        transition: border-color 0.2s ease;
    }
    
    .kpi-card:hover {
        border-color: var(--text-muted);
    }
    
    .kpi-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 600;
        color: var(--text-primary);
        font-family: 'IBM Plex Sans', sans-serif;
        line-height: 1.2;
    }
    
    .kpi-value-number {
        font-size: 2.5rem;
    }
    
    .kpi-subtext {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    /* Status indicators - data-driven colors only */
    .status-green {
        color: var(--accent-green);
    }
    
    .status-amber {
        color: var(--accent-amber);
    }
    
    .status-red {
        color: var(--accent-red);
    }
    
    /* Intelligence cards */
    .intel-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .intel-card-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Signal nodes - Intelligence Ingestion */
    .signal-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .signal-node {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 1.25rem;
        position: relative;
        transition: border-color 0.2s ease;
    }
    
    .signal-node:hover {
        border-color: var(--text-muted);
    }
    
    .signal-node-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .signal-name {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.875rem;
    }
    
    .signal-status {
        font-size: 0.75rem;
        padding: 0.25rem 0.5rem;
        border-radius: 3px;
        font-weight: 500;
    }
    
    .signal-status-active {
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-green);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .signal-status-degraded {
        background: rgba(245, 158, 11, 0.15);
        color: var(--accent-amber);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .signal-status-offline {
        background: rgba(239, 68, 68, 0.15);
        color: var(--accent-red);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .signal-strength {
        margin-top: 0.75rem;
    }
    
    .signal-strength-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-bottom: 0.25rem;
    }
    
    .signal-strength-bar {
        height: 4px;
        background: var(--bg-primary);
        border-radius: 2px;
        overflow: hidden;
    }
    
    .signal-strength-fill {
        height: 100%;
        background: var(--accent-green);
        transition: width 0.3s ease;
    }
    
    .signal-freshness {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
    }
    
    /* Sentiment waveform background */
    .waveform-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 120px;
        opacity: 0.08;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .waveform-svg {
        width: 100%;
        height: 100%;
    }
    
    /* Risk badges - minimal */
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 3px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border: 1px solid;
    }
    
    .risk-badge-low {
        background: rgba(16, 185, 129, 0.15);
        color: var(--accent-green);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    .risk-badge-medium {
        background: rgba(245, 158, 11, 0.15);
        color: var(--accent-amber);
        border-color: rgba(245, 158, 11, 0.3);
    }
    
    .risk-badge-high {
        background: rgba(239, 68, 68, 0.15);
        color: var(--accent-red);
        border-color: rgba(239, 68, 68, 0.3);
    }
    
    .risk-badge-critical {
        background: rgba(220, 38, 38, 0.2);
        color: var(--accent-red);
        border-color: rgba(220, 38, 38, 0.4);
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.3);
    }
    
    /* Data table styling */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
    }
    
    .data-table th {
        text-align: left;
        padding: 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid var(--border-color);
    }
    
    .data-table td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-primary);
        font-size: 0.875rem;
    }
    
    .data-table tr:hover {
        background: var(--bg-tertiary);
    }
    
    /* Typography */
    h1 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 600;
        font-size: 1.75rem;
        color: var(--text-primary);
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
        color: var(--text-primary);
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        color: var(--text-primary);
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* System status at bottom of sidebar */
    .system-status {
        position: absolute;
        bottom: 1rem;
        left: 1rem;
        right: 1rem;
        padding: 0.75rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    .system-status-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent-green);
        box-shadow: 0 0 6px var(--accent-green);
        margin-right: 0.5rem;
    }
    
    /* Comparison panels */
    .comparison-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .comparison-panel {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 4px;
        padding: 1.5rem;
    }
    
    .comparison-header {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border-color);
    }
    
    .metric-label {
        color: var(--text-muted);
        font-size: 0.875rem;
    }
    
    .metric-value {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    /* Evidence items */
    .evidence-list {
        margin-top: 1rem;
    }
    
    .evidence-item {
        background: var(--bg-tertiary);
        border-left: 3px solid var(--border-color);
        padding: 1rem;
        margin-bottom: 0.75rem;
        border-radius: 0 4px 4px 0;
    }
    
    .evidence-source {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
    }
    
    .evidence-text {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.6;
    }
    
    /* Streamlit element overrides */
    .stSelectbox label,
    .stTextInput label,
    .stTextArea label {
        color: var(--text-muted);
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .stSelectbox > div > div {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    
    .stButton > button {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--bg-tertiary);
        border-color: var(--text-muted);
    }
    
    /* Active navigation state */
    button[kind="secondary"]:has(+ .stButton[kind="secondary"]) {
        border-left: 3px solid var(--accent-green);
        padding-left: calc(0.5rem - 3px);
    }
    
    /* Sidebar button styling */
    [data-testid="stSidebar"] button[kind="secondary"] {
        background: transparent;
        border: none;
        color: var(--text-primary);
        text-align: left;
        padding: 0.75rem 1rem;
        width: 100%;
        border-radius: 0;
        font-weight: 500;
        transition: all 0.2s ease;
        position: relative;
    }
    
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }
</style>
"""

st.markdown(COMMAND_CENTER_CSS, unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_data():
    """Load data from database first, fallback to CSV"""
    data = {
        'promises': None,
        'sentiment': None,
        'gap': None
    }
    
    # Try to load from database first
    try:
        from database.db_manager import DatabaseManager
        from database.schema import Promise, SentimentAnalysis, GapAnalysis, Product
        
        db = DatabaseManager()
        
        # Load products with promises
        products = db.get_all_products()
        if products:
            promises_list = []
            for product in products:
                promise = db.get_promise(product.id)
                if promise:
                    promises_list.append({
                        'product_name': product.name,
                        'investment_objective': promise.investment_objective,
                        'promised_returns': promise.promised_returns,
                        'risk_category': promise.risk_category,
                        'lock_in_period': promise.lock_in_period,
                        'exit_load': promise.exit_load,
                        'min_investment': promise.min_investment,
                        'key_features': promise.key_features or [],
                        'warnings': promise.warnings or [],
                        'extraction_confidence': promise.extraction_confidence
                    })
            
            if promises_list:
                data['promises'] = pd.DataFrame(promises_list)
            
            # Load sentiment analyses
            sentiment_list = []
            for product in products:
                sentiment = db.get_sentiment_analysis(product.id)
                if sentiment:
                    sentiment_list.append({
                        'product': product.name,
                        'avg_sentiment': sentiment.avg_sentiment,
                        'positive_count': sentiment.positive_count,
                        'negative_count': sentiment.negative_count,
                        'neutral_count': sentiment.neutral_count,
                        'total_reviews': sentiment.total_reviews,
                        'dissatisfaction_index': sentiment.dissatisfaction_index,
                        'risk_score': sentiment.risk_score
                    })
            
            if sentiment_list:
                data['sentiment'] = pd.DataFrame(sentiment_list)
            
            # Load gap analyses
            gap_list = []
            gap_analyses = db.get_all_gap_analyses()
            for gap in gap_analyses:
                product = db.get_product_by_id(gap.product_id)
                if product:
                    gap_list.append({
                        'product_name': product.name,
                        'promise_confidence': gap.promise_confidence,
                        'sentiment_score': gap.sentiment_score,
                        'dissatisfaction_index': gap.dissatisfaction_index,
                        'overall_risk_score': gap.overall_risk_score,
                        'risk_level': gap.risk_level,
                        'mismatches': gap.mismatches or [],
                        'recommendations': gap.recommendations or []
                    })
            
            if gap_list:
                data['gap'] = pd.DataFrame(gap_list)
            
            db.close()
            return data
        
    except Exception as e:
        st.warning(f"⚠️ Database not available, using CSV fallback: {e}")
    
    # Fallback to CSV files
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
        'avg_risk_score': 0.0,
        'avg_dissatisfaction': 0.0
    }
    
    if data['gap'] is not None and len(data['gap']) > 0:
        kpis['products_monitored'] = len(data['gap'])
        high_risk = data['gap'][data['gap']['risk_level'].isin(['high', 'critical'])]
        kpis['high_risk_products'] = len(high_risk)
        
        if 'overall_risk_score' in data['gap'].columns:
            kpis['avg_risk_score'] = data['gap']['overall_risk_score'].mean()
        
        if 'dissatisfaction_index' in data['gap'].columns:
            kpis['avg_dissatisfaction'] = data['gap']['dissatisfaction_index'].mean()
    
    return kpis

def get_risk_badge_class(risk_level):
    """Get CSS class for risk badge"""
    risk_lower = str(risk_level).lower()
    if risk_lower == 'critical':
        return 'risk-badge-critical'
    elif risk_lower == 'high':
        return 'risk-badge-high'
    elif risk_lower == 'medium':
        return 'risk-badge-medium'
    else:
        return 'risk-badge-low'

def generate_sentiment_waveform():
    """Generate live sentiment waveform for background"""
    # Generate smooth waveform data
    t = np.linspace(0, 20, 1000)
    # Multiple sine waves for complexity
    wave = (np.sin(t * 0.5) * 0.3 + 
            np.sin(t * 1.2) * 0.2 + 
            np.sin(t * 2.1) * 0.15 + 
            np.sin(t * 3.7) * 0.1)
    wave = (wave + 1) / 2  # Normalize to 0-1
    
    return wave

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render minimal command-grade sidebar"""
    st.sidebar.markdown("""
    <div class="sidebar-brand">
        <h1>VERITAS</h1>
        <p>AI Regulatory Command Center</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation items
    nav_items = [
        ("Overview", "overview"),
        ("Products", "products"),
        ("Expectation Engine", "expectation"),
        ("Reality Engine", "reality"),
        ("Risk Intelligence", "risks"),
        ("Evidence Vault", "evidence"),
        ("System Controls", "controls")
    ]
    
    # Initialize session state for active page
    if 'active_page' not in st.session_state:
        st.session_state.active_page = "overview"
    
    # Render navigation
    for label, page_id in nav_items:
        if st.sidebar.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.active_page = page_id
            st.rerun()
    st.sidebar.markdown("---")
    
    # System status
    st.sidebar.markdown("""
    <div class="system-status">
        <span class="system-status-dot"></span>
        AI Monitoring Active
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# COMMAND CENTER HEADER
# ============================================================================

def render_command_header(title, monitoring_count=None):
    """Render command center header with situation awareness"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'<div class="command-title">{title}</div>', unsafe_allow_html=True)
    
    with col2:
        situation_html = '<div class="situation-bar">'
        if monitoring_count:
            situation_html += f'<div class="status-pill"><span class="status-pill-dot"></span>Monitoring {monitoring_count} Products</div>'
        
        # Time range selector
        situation_html += '<div style="display: flex; gap: 0.5rem;">'
        situation_html += '<button style="padding: 0.375rem 0.75rem; background: var(--bg-tertiary); border: 1px solid var(--border-color); color: var(--text-secondary); border-radius: 4px; cursor: pointer; font-size: 0.75rem;">7d</button>'
        situation_html += '<button style="padding: 0.375rem 0.75rem; background: var(--bg-tertiary); border: 1px solid var(--border-color); color: var(--text-secondary); border-radius: 4px; cursor: pointer; font-size: 0.75rem;">30d</button>'
        situation_html += '<button style="padding: 0.375rem 0.75rem; background: var(--bg-tertiary); border: 1px solid var(--border-color); color: var(--text-secondary); border-radius: 4px; cursor: pointer; font-size: 0.75rem;">90d</button>'
        situation_html += '</div>'
        situation_html += '</div>'
        
        st.markdown(situation_html, unsafe_allow_html=True)

# ============================================================================
# PAGE VIEWS
# ============================================================================

def render_overview(data):
    """Intelligence Overview - Main dashboard"""
    kpis = calculate_kpis(data)
    
    render_command_header("Mis-Selling Intelligence Overview", kpis['products_monitored'])
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Products Monitored</div>
            <div class="kpi-value kpi-value-number">{kpis['products_monitored']}</div>
            <div class="kpi-subtext">Active surveillance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        risk_color = "status-red" if kpis['high_risk_products'] > 0 else "status-green"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">High-Risk Products</div>
            <div class="kpi-value kpi-value-number {risk_color}">{kpis['high_risk_products']}</div>
            <div class="kpi-subtext">Requiring attention</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Risk Score</div>
            <div class="kpi-value kpi-value-number">{kpis['avg_risk_score']:.1f}</div>
            <div class="kpi-subtext">System-wide metric</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Dissatisfaction Index</div>
            <div class="kpi-value kpi-value-number">{kpis['avg_dissatisfaction']:.1f}%</div>
            <div class="kpi-subtext">Customer sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Risk Distribution
    if data['gap'] is not None and len(data['gap']) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Risk Distribution")
            risk_counts = data['gap']['risk_level'].value_counts()
            
            colors_map = {
                'low': '#10b981',
                'medium': '#f59e0b',
                'high': '#ef4444',
                'critical': '#dc2626'
            }
            colors = [colors_map.get(level.lower(), '#64748b') for level in risk_counts.index]
            
            fig = go.Figure(data=[go.Bar(
                x=risk_counts.index.str.title(),
                y=risk_counts.values,
                marker_color=colors,
                text=risk_counts.values,
                textposition='outside',
            )])
            fig.update_layout(
                height=300,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', size=12, color='#e2e8f0'),
                margin=dict(l=20, r=20, t=20, b=40),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)'),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Recent Alerts")
            high_risk = data['gap'][data['gap']['risk_level'].isin(['high', 'critical'])].head(5)
            for _, row in high_risk.iterrows():
                badge_class = get_risk_badge_class(row['risk_level'])
                st.markdown(f"""
                <div class="intel-card" style="padding: 1rem; margin-bottom: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="color: var(--text-primary);">{row['product_name']}</strong>
                        <span class="{badge_class}">{row['risk_level'].upper()}</span>
                    </div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary);">
                        Risk Score: {row['overall_risk_score']:.1f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_products_monitor(data):
    """Products Monitor - Active surveillance"""
    render_command_header("Products Monitor")
    
    if data['gap'] is not None and len(data['gap']) > 0:
        # Filter options
        risk_filter = st.selectbox("Filter by Risk Level", ["All", "Critical", "High", "Medium", "Low"])
        
        filtered_data = data['gap'].copy()
        if risk_filter != "All":
            filtered_data = filtered_data[filtered_data['risk_level'].str.lower() == risk_filter.lower()]
        
        # Products table
        st.markdown("### Active Products")
        for _, row in filtered_data.iterrows():
            badge_class = get_risk_badge_class(row['risk_level'])
            st.markdown(f"""
            <div class="intel-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem;">{row['product_name']}</h3>
                        <div style="font-size: 0.875rem; color: var(--text-muted);">
                            Risk Score: <span style="color: var(--text-primary); font-weight: 600;">{row['overall_risk_score']:.2f}</span>
                        </div>
                    </div>
                    <span class="{badge_class}">{row['risk_level'].upper()}</span>
                </div>
                
                <div class="metric-row">
                    <span class="metric-label">Promise Confidence</span>
                    <span class="metric-value">{row.get('promise_confidence', 0):.1f}%</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Sentiment Score</span>
                    <span class="metric-value">{row.get('sentiment_score', 0):.2f}</span>
                </div>
                <div class="metric-row" style="border-bottom: none;">
                    <span class="metric-label">Dissatisfaction</span>
                    <span class="metric-value">{row.get('dissatisfaction_index', 0):.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No product data available")

def render_expectation_engine(data):
    """Expectation Engine - Promise extraction analysis"""
    render_command_header("Expectation Engine")
    
    if data['promises'] is not None and len(data['promises']) > 0:
        st.markdown("### Extracted Promises")
        for _, row in data['promises'].iterrows():
            st.markdown(f"""
            <div class="intel-card">
                <div class="intel-card-header">
                    <span>{row['product_name']}</span>
                    <span style="color: var(--text-muted);">Confidence: {row.get('extraction_confidence', 0):.1f}%</span>
                </div>
                <div class="comparison-grid">
                    <div>
                        <div class="metric-row">
                            <span class="metric-label">Investment Objective</span>
                            <span class="metric-value">{row.get('investment_objective', 'N/A')}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Promised Returns</span>
                            <span class="metric-value">{row.get('promised_returns', 'N/A')}</span>
                        </div>
                        <div class="metric-row" style="border-bottom: none;">
                            <span class="metric-label">Risk Category</span>
                            <span class="metric-value">{row.get('risk_category', 'N/A')}</span>
                        </div>
                    </div>
                    <div>
                        <div class="metric-row">
                            <span class="metric-label">Lock-in Period</span>
                            <span class="metric-value">{row.get('lock_in_period', 'N/A')}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Exit Load</span>
                            <span class="metric-value">{row.get('exit_load', 'N/A')}</span>
                        </div>
                        <div class="metric-row" style="border-bottom: none;">
                            <span class="metric-label">Min Investment</span>
                            <span class="metric-value">{row.get('min_investment', 'N/A')}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No promise data available")

def render_reality_engine(data):
    """Reality Engine - Customer sentiment analysis"""
    render_command_header("Reality Engine")
    
    if data['sentiment'] is not None and len(data['sentiment']) > 0:
        st.markdown("### Sentiment Analysis")
        for _, row in data['sentiment'].iterrows():
            sentiment_color = "status-green" if row['avg_sentiment'] > 0.2 else "status-amber" if row['avg_sentiment'] > -0.2 else "status-red"
            
            st.markdown(f"""
            <div class="intel-card">
                <div class="intel-card-header">
                    <span>{row['product']}</span>
                    <span class="{sentiment_color}">Avg Sentiment: {row['avg_sentiment']:.2f}</span>
                </div>
                <div class="comparison-grid">
                    <div>
                        <div class="metric-row">
                            <span class="metric-label">Total Reviews</span>
                            <span class="metric-value">{row['total_reviews']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Positive</span>
                            <span class="metric-value status-green">{row['positive_count']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Negative</span>
                            <span class="metric-value status-red">{row['negative_count']}</span>
                        </div>
                    </div>
                    <div>
                        <div class="metric-row">
                            <span class="metric-label">Neutral</span>
                            <span class="metric-value">{row['neutral_count']}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Dissatisfaction Index</span>
                            <span class="metric-value">{row['dissatisfaction_index']:.1f}%</span>
                        </div>
                        <div class="metric-row" style="border-bottom: none;">
                            <span class="metric-label">Risk Score</span>
                            <span class="metric-value">{row['risk_score']:.2f}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No sentiment data available")

def render_risk_intelligence(data):
    """Risk Intelligence - Gap analysis and alerts"""
    render_command_header("Risk Intelligence")
    
    if data['gap'] is not None and len(data['gap']) > 0:
        # Sort by risk score
        sorted_data = data['gap'].sort_values('overall_risk_score', ascending=False)
        
        for _, row in sorted_data.iterrows():
            badge_class = get_risk_badge_class(row['risk_level'])
            
            st.markdown(f"""
            <div class="intel-card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <h3 style="margin: 0; font-size: 1rem;">{row['product_name']}</h3>
                    <span class="{badge_class}">{row['risk_level'].upper()}</span>
                </div>
                
                <div class="metric-row">
                    <span class="metric-label">Overall Risk Score</span>
                    <span class="metric-value">{row['overall_risk_score']:.2f}</span>
                </div>
                
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                    <div class="intel-card-header" style="margin-bottom: 0.5rem;">Detected Mismatches</div>
                    <div class="evidence-list">
            """, unsafe_allow_html=True)
            
            if row.get('mismatches') and len(row['mismatches']) > 0:
                for mismatch in row['mismatches'][:3]:  # Show first 3
                    st.markdown(f"""
                    <div class="evidence-item">
                        <div class="evidence-text">{mismatch}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="evidence-item">
                    <div class="evidence-text" style="color: var(--text-muted);">No specific mismatches detected</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div></div>", unsafe_allow_html=True)
    else:
        st.info("No risk intelligence data available")

def render_evidence_vault(data):
    """Evidence Vault - Immutable evidence storage"""
    render_command_header("Evidence Vault")
    
    if data['gap'] is not None and len(data['gap']) > 0:
        st.markdown("### Collected Evidence")
        for _, row in data['gap'].iterrows():
            st.markdown(f"""
            <div class="intel-card">
                <div class="intel-card-header">
                    <span>{row['product_name']}</span>
                    <span style="color: var(--text-muted); font-size: 0.75rem;">Evidence ID: {hash(row['product_name']) % 10000}</span>
                </div>
                <div class="evidence-list">
                    <div class="evidence-item">
                        <div class="evidence-source">Promise Extraction Evidence</div>
                        <div class="evidence-text">Confidence: {row.get('promise_confidence', 0):.1f}% | Extracted from marketing materials</div>
                    </div>
                    <div class="evidence-item">
                        <div class="evidence-source">Sentiment Analysis Evidence</div>
                        <div class="evidence-text">Score: {row.get('sentiment_score', 0):.2f} | Based on customer reviews and social media</div>
                    </div>
                    <div class="evidence-item">
                        <div class="evidence-source">Gap Analysis Evidence</div>
                        <div class="evidence-text">Risk Score: {row['overall_risk_score']:.2f} | {len(row.get('mismatches', []))} mismatches detected</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No evidence data available")

def render_system_controls(data):
    """System Controls - Intelligence Ingestion Panel"""
    render_command_header("System Controls")
    
    st.markdown("### Reality Signal Ingestion")
    st.markdown('<p style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 1.5rem;">Configure data source monitoring and signal quality</p>', unsafe_allow_html=True)
    
    # Signal Nodes
    signal_sources = [
        {"name": "Twitter/X", "status": "active", "strength": 85, "freshness": "3 min ago"},
        {"name": "Reddit", "status": "active", "strength": 72, "freshness": "5 min ago"},
        {"name": "Customer Reviews", "status": "active", "strength": 91, "freshness": "1 min ago"},
        {"name": "News APIs", "status": "degraded", "strength": 45, "freshness": "12 min ago"},
    ]
    
    cols = st.columns(2)
    for idx, source in enumerate(signal_sources):
        col = cols[idx % 2]
        with col:
            status_class = f"signal-status-{source['status']}"
            st.markdown(f"""
            <div class="signal-node">
                <div class="signal-node-header">
                    <span class="signal-name">{source['name']}</span>
                    <span class="signal-status {status_class}">{source['status'].upper()}</span>
                </div>
                <div class="signal-strength">
                    <div class="signal-strength-label">Signal Strength</div>
                    <div class="signal-strength-bar">
                        <div class="signal-strength-fill" style="width: {source['strength']}%;"></div>
                    </div>
                </div>
                <div class="signal-freshness">Updated {source['freshness']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional system information
    st.markdown("### System Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="intel-card">
            <div class="intel-card-header">Database</div>
            <div style="color: var(--accent-green); font-size: 0.875rem; margin-top: 0.5rem;">● Connected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="intel-card">
            <div class="intel-card-header">AI Models</div>
            <div style="color: var(--accent-green); font-size: 0.875rem; margin-top: 0.5rem;">● Operational</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="intel-card">
            <div class="intel-card-header">API Server</div>
            <div style="color: var(--accent-green); font-size: 0.875rem; margin-top: 0.5rem;">● Active</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    
    # Add sentiment waveform to background
    wave = generate_sentiment_waveform()
    waveform_svg = f"""
    <div class="waveform-container">
        <svg class="waveform-svg" viewBox="0 0 1000 100" preserveAspectRatio="none">
            <path d="M 0,50 {' '.join([f'L {i*10},{50 - w*40}' for i, w in enumerate(wave)])} L 1000,50" 
                  fill="none" stroke="#10b981" stroke-width="0.5" opacity="0.5"/>
        </svg>
    </div>
    """
    st.markdown(waveform_svg, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Load data
    data = load_data()
    
    # Render active page
    page = st.session_state.active_page
    
    if page == "overview":
        render_overview(data)
    elif page == "products":
        render_products_monitor(data)
    elif page == "expectation":
        render_expectation_engine(data)
    elif page == "reality":
        render_reality_engine(data)
    elif page == "risks":
        render_risk_intelligence(data)
    elif page == "evidence":
        render_evidence_vault(data)
    elif page == "controls":
        render_system_controls(data)
    else:
        render_overview(data)

if __name__ == "__main__":
    main()

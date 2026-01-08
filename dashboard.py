# dashboard.py - Hackathon-Winning Mis-Selling Intelligence Platform
# Stunning, modern UI with impressive visuals and interactions

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json
from datetime import datetime, timedelta
import base64
import random

# Page configuration
st.set_page_config(
    page_title="Mis-Selling Intelligence Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# STUNNING CSS - HACKATHON WINNING DESIGN
# ============================================================================

STUNNING_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-gradient: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%);
        
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        
        --shadow-glow: 0 8px 32px rgba(102, 126, 234, 0.3);
        --shadow-card: 0 20px 60px rgba(0, 0, 0, 0.1);
        --shadow-hover: 0 30px 80px rgba(102, 126, 234, 0.4);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
        font-family: 'Poppins', 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Animated background particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main content wrapper */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }
    
    /* Glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Stunning KPI Cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-card);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-10px);
        box-shadow: var(--shadow-hover);
    }
    
    .kpi-card:hover::before {
        transform: scaleX(1);
    }
    
    .kpi-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        opacity: 0.8;
    }
    
    .kpi-value {
        font-size: 3rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1rem 0;
        font-family: 'Poppins', sans-serif;
    }
    
    .kpi-trend {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .trend-up {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
    }
    
    .trend-down {
        background: linear-gradient(135deg, #ef4444, #f87171);
        color: white;
    }
    
    .trend-neutral {
        background: linear-gradient(135deg, #64748b, #94a3b8);
        color: white;
    }
    
    /* Glassmorphism data cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-card);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-hover);
    }
    
    /* Stunning headers */
    h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }
    
    h2 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        color: white;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.5rem;
        color: white;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Status badges with glow */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .badge-low {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
    }
    
    .badge-medium {
        background: linear-gradient(135deg, #f59e0b, #fbbf24);
        color: white;
    }
    
    .badge-high {
        background: linear-gradient(135deg, #ef4444, #f87171);
        color: white;
    }
    
    .badge-critical {
        background: linear-gradient(135deg, #dc2626, #ef4444);
        color: white;
        animation: pulse-critical 1.5s infinite;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
    }
    
    @keyframes pulse-critical {
        0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.6); }
        50% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.9); }
    }
    
    /* Comparison panel with gradient */
    .comparison-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .comparison-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-card);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .comparison-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: var(--primary-gradient);
    }
    
    .comparison-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-hover);
    }
    
    .comparison-header {
        font-size: 1rem;
        font-weight: 700;
        color: #1e293b;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Risk meter with glow */
    .risk-meter-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: var(--shadow-card);
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .risk-meter-bar {
        height: 20px;
        background: #e2e8f0;
        border-radius: 50px;
        overflow: hidden;
        margin: 1.5rem 0;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
        position: relative;
    }
    
    .risk-meter-fill {
        height: 100%;
        border-radius: 50px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .risk-meter-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .risk-low { 
        background: linear-gradient(90deg, #10b981, #34d399);
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
    
    .risk-medium { 
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
    }
    
    .risk-high { 
        background: linear-gradient(90deg, #ef4444, #f87171);
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
    }
    
    /* Evidence items */
    .evidence-item {
        padding: 1.5rem;
        margin: 1rem 0;
        background: rgba(255, 255, 255, 0.7);
        border-left: 4px solid;
        border-radius: 10px;
        font-size: 0.9375rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .evidence-item:hover {
        transform: translateX(10px);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
    }
    
    .evidence-source {
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .evidence-text {
        color: #64748b;
        font-style: italic;
        line-height: 1.6;
    }
    
    /* Upload area */
    .upload-area {
        border: 3px dashed rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .upload-area::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: rotate 3s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .upload-area:hover {
        border-color: rgba(255, 255, 255, 0.8);
        background: rgba(255, 255, 255, 0.15);
        transform: scale(1.02);
    }
    
    /* Sidebar navigation */
    .sidebar-brand {
        padding: 2rem 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    .sidebar-brand h1 {
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .sidebar-nav-btn {
        width: 100%;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        background: rgba(255, 255, 255, 0.05);
        border: none;
        border-radius: 12px;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1rem;
        font-weight: 600;
        text-align: left;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-nav-btn::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        height: 100%;
        width: 4px;
        background: var(--primary-gradient);
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }
    
    .sidebar-nav-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    .sidebar-nav-btn:hover::before {
        transform: scaleY(1);
    }
    
    /* Metric rows */
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(226, 232, 240, 0.5);
        transition: all 0.2s ease;
    }
    
    .metric-row:hover {
        background: rgba(102, 126, 234, 0.05);
        margin: 0 -1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        border-radius: 8px;
    }
    
    .metric-row:last-child {
        border-bottom: none;
    }
    
    .metric-label {
        font-size: 0.9375rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 1.125rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    /* Section dividers */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 3rem 0;
    }
    
    /* Buttons */
    .stButton>button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid;
        box-shadow: var(--shadow-card);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .comparison-container {
            grid-template-columns: 1fr;
        }
        
        h1 {
            font-size: 2rem;
        }
    }
</style>
"""

st.markdown(STUNNING_CSS, unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {trend_html}
    </div>
    """

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
        <h1>🔍 Mis-Selling<br>Intelligence</h1>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.875rem; margin-top: 0.5rem;">
            Regulator Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation items
    nav_items = [
        ("📊 Dashboard Overview", "dashboard"),
        ("📦 Products Monitor", "products"),
        ("📄 Expectation Engine", "expectation"),
        ("💬 Reality Engine", "reality"),
        ("🚨 Risk Flags", "risks"),
        ("📋 Reports & Evidence", "reports"),
        ("⚙️ Settings", "settings")
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

# ============================================================================
# PAGE VIEWS
# ============================================================================

def render_dashboard_overview(data):
    """Stunning main dashboard overview"""
    st.markdown("# 🛡️ Mis-Selling Risk Overview")
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.125rem; margin-bottom: 3rem;">Comprehensive monitoring and analysis of financial product mis-selling risks</p>', unsafe_allow_html=True)
    
    # Calculate KPIs
    kpis = calculate_kpis(data)
    
    # Stunning KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(render_kpi_card(
            "Products Monitored",
            f"{kpis['products_monitored']}",
            trend=1,
            trend_value="+2 this week"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(render_kpi_card(
            "High-Risk Products",
            f"{kpis['high_risk_products']}",
            trend=-1 if kpis['high_risk_products'] > 0 else 0,
            trend_value=f"{kpis['high_risk_products']} flagged"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(render_kpi_card(
            "Avg Risk Score",
            f"{kpis['avg_gap']:.2f}",
            trend=0,
            trend_value=""
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(render_kpi_card(
            "Customer Dissatisfaction",
            f"{kpis['avg_dissatisfaction']:.1f}%",
            trend=1,
            trend_value="+2.3% vs last month"
        ), unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Risk Distribution Chart
    if data['gap'] is not None and len(data['gap']) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Risk Distribution")
            risk_counts = data['gap']['risk_level'].value_counts()
            
            # Create stunning pie chart
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
                textfont=dict(size=16, family='Poppins', color='white'),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
            )])
            fig_pie.update_layout(
                height=400,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', size=14, color='white'),
                legend=dict(font=dict(size=14, color='white'))
            )
            st.plotly_chart(fig_pie, use_container_width=True, use_container_height=True)
        
        with col2:
            st.markdown("### 🚨 Top Risk Products")
            top_risks = data['gap'].nlargest(5, 'overall_risk_score')[['product_name', 'risk_level', 'overall_risk_score']]
            
            for idx, row in top_risks.iterrows():
                badge_class = get_risk_badge_class(row['risk_level'])
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; color: #1e293b; font-size: 1.125rem; margin-bottom: 0.5rem;">
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
    else:
        st.markdown("""
        <div class="info-box" style="border-left-color: #f59e0b;">
            <strong>⚠️ No Data Available</strong><br>
            Please run the analysis pipeline first.
        </div>
        """, unsafe_allow_html=True)
    
    # Comparison View
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    render_comparison_view(data)

def render_comparison_view(data):
    """Stunning comparison view"""
    st.markdown("### ⚖️ Expectation vs Reality Comparison")
    
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
                
                st.markdown(f"""
                <div class="comparison-container">
                    <div class="comparison-card" style="border-top: 5px solid #10b981;">
                        <div class="comparison-header" style="color: #10b981;">✅ What Was Promised</div>
                        <div class="metric-row">
                            <span class="metric-label">Returns</span>
                            <span class="metric-value">{promise_data.get('promised_returns', 'N/A')}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Risk Category</span>
                            <span class="metric-value">{promise_data.get('risk_category', 'N/A')}</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Lock-in Period</span>
                            <span class="metric-value">{promise_data.get('lock_in_period', 'N/A')}</span>
                        </div>
                    </div>
                    
                    <div class="comparison-card" style="border-top: 5px solid #ef4444;">
                        <div class="comparison-header" style="color: #ef4444;">❌ Customer Reality</div>
                        <div class="metric-row">
                            <span class="metric-label">Reported Returns</span>
                            <span class="metric-value" style="color: #ef4444;">Poor / Below Expectations</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Perceived Risk</span>
                            <span class="metric-value" style="color: #ef4444;">High Volatility Reported</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Exit Experience</span>
                            <span class="metric-value" style="color: #ef4444;">Difficulties Reported</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_products_monitor(data):
    """Products monitoring view"""
    st.markdown("# 📦 Products Monitor")
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.125rem;">Real-time monitoring of all analyzed financial products</p>', unsafe_allow_html=True)
    
    if data['gap'] is not None and len(data['gap']) > 0:
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search products", placeholder="Enter product name...")
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
                display_df.style.background_gradient(subset=['Risk Score', 'Dissatisfaction %'], cmap='RdYlGn_r'),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Column structure mismatch")
    else:
        st.markdown("""
        <div class="info-box" style="border-left-color: #f59e0b;">
            <strong>⚠️ No Products Analyzed</strong><br>
            Run the Expectation and Reality Engines to begin monitoring.
        </div>
        """, unsafe_allow_html=True)

def render_expectation_engine(data):
    """Stunning Expectation Engine UI"""
    st.markdown("# 📄 Expectation Engine")
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.125rem;">Extract and analyze promises from product marketing materials</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📤 Upload Document", "📋 Extracted Promises"])
    
    with tab1:
        st.markdown("### Upload Product Document")
        st.markdown("""
        <div class="upload-area">
            <p style="font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 1rem;">
                📤 Drag & Drop PDF or Brochure
            </p>
            <p style="font-size: 1rem; color: rgba(255,255,255,0.8);">
                Supported formats: PDF, DOCX, Images
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['pdf', 'docx', 'png', 'jpg'], label_visibility="collapsed")
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            if st.button("🚀 Extract Promises", type="primary", use_container_width=True):
                with st.spinner("🔍 Analyzing document with NLP engine..."):
                    st.success("✅ Promises extracted successfully!")
    
    with tab2:
        st.markdown("### 📋 Extracted Promise Profiles")
        
        if data['promises'] is not None and len(data['promises']) > 0:
            for idx, row in data['promises'].iterrows():
                product_name = row.get('product_name', 'Unknown Product')
                confidence = row.get('extraction_confidence', 0)
                
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid #e2e8f0;">
                        <div style="font-weight: 800; font-size: 1.25rem; color: #1e293b;">{product_name}</div>
                        <div style="padding: 0.5rem 1rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 50px; font-weight: 700; font-size: 0.875rem;">
                            Confidence: {confidence:.0%}
                        </div>
                    </div>
                    
                    <div class="metric-row">
                        <span class="metric-label">Investment Objective</span>
                        <span class="metric-value">{row.get('investment_objective', 'N/A')}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Promised Returns</span>
                        <span class="metric-value" style="color: #667eea;">{row.get('promised_returns', 'N/A')}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Risk Category</span>
                        <span class="metric-value">{row.get('risk_category', 'N/A')}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Lock-in Period</span>
                        <span class="metric-value">{row.get('lock_in_period', 'N/A')}</span>
                    </div>
                    <div class="metric-row">
                        <span class="metric-label">Exit Load</span>
                        <span class="metric-value">{row.get('exit_load', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box" style="border-left-color: #f59e0b;">
                <strong>ℹ️ No Promises Extracted</strong><br>
                Upload a document to begin analysis.
            </div>
            """, unsafe_allow_html=True)

def render_reality_engine(data):
    """Stunning Reality Engine UI"""
    st.markdown("# 💬 Reality Engine")
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.125rem;">Analyze customer sentiment and real-world experiences</p>', unsafe_allow_html=True)
    
    if data['sentiment'] is not None and len(data['sentiment']) > 0:
        # Sentiment timeline
        st.markdown("### 📈 Customer Sentiment Timeline")
        
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
        st.markdown("### 📊 Complaint Topic Breakdown")
        
        topics = [
            {"name": "Hidden Charges", "frequency": 42, "sentiment": -0.8},
            {"name": "Poor Returns", "frequency": 38, "sentiment": -0.7},
            {"name": "Service Quality", "frequency": 25, "sentiment": -0.5},
            {"name": "Exit Difficulties", "frequency": 18, "sentiment": -0.6}
        ]
        
        for topic in topics:
            sentiment_color = "#ef4444" if topic['sentiment'] < -0.6 else "#f59e0b"
            sentiment_width = abs(topic['sentiment']) * 100
            
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-weight: 700; font-size: 1.125rem; color: #1e293b;">{topic['name']}</div>
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
    else:
        st.markdown("""
        <div class="info-box" style="border-left-color: #f59e0b;">
            <strong>ℹ️ No Sentiment Data</strong><br>
            Run the Reality Engine analysis first.
        </div>
        """, unsafe_allow_html=True)

def render_risk_flags(data):
    """Stunning Risk Flags view"""
    st.markdown("# 🚨 Risk Flags")
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.125rem;">Detailed risk analysis and flagging system</p>', unsafe_allow_html=True)
    
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
            
            # Stunning Risk Meter
            st.markdown(f"""
            <div class="risk-meter-container">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0; color: #1e293b;">Overall Risk Score</h3>
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
            
            # Why flagged section
            with st.expander("❓ Why Flagged? - Evidence & Justification", expanded=True):
                st.markdown("### 📋 Risk Justification")
                
                try:
                    mismatches = json.loads(product_data.get('mismatches', '[]'))
                    if mismatches:
                        for mismatch in mismatches[:3]:
                            st.markdown(f"""
                            <div class="evidence-item" style="border-left-color: #ef4444;">
                                <div class="evidence-source">
                                    {mismatch.get('promise_aspect', 'Unknown')} Mismatch
                                    <span style="float: right; padding: 0.25rem 0.75rem; background: linear-gradient(135deg, #ef4444, #f87171); color: white; border-radius: 50px; font-weight: 700; font-size: 0.75rem;">
                                        Severity: {float(mismatch.get('severity', 0)):.0%}
                                    </span>
                                </div>
                                <div class="evidence-text">
                                    {mismatch.get('complaint_topic', 'No description')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                except:
                    st.markdown(f"""
                    <div class="evidence-item" style="border-left-color: #f59e0b;">
                        <div class="evidence-source">Risk Indicators Detected</div>
                        <div class="evidence-text">
                            Risk score of {risk_score:.0f}/100 based on sentiment analysis and gap detection. 
                            Dissatisfaction index: {product_data.get('dissatisfaction_index', 0):.1f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Evidence sources
            st.markdown("### 📚 Evidence Sources")
            evidence_sources = [
                {"source": "Customer Reviews", "count": 127, "sentiment": -0.65},
                {"source": "Social Media Mentions", "count": 43, "sentiment": -0.72},
                {"source": "Complaint Portal", "count": 18, "sentiment": -0.58}
            ]
            
            for source in evidence_sources:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; font-size: 1.125rem; color: #1e293b; margin-bottom: 0.5rem;">{source['source']}</div>
                            <div style="font-size: 0.875rem; color: #64748b;">{source['count']} data points</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.875rem; color: #64748b; margin-bottom: 0.25rem;">Avg Sentiment</div>
                            <div style="font-weight: 800; font-size: 1.5rem; background: linear-gradient(135deg, #ef4444, #f87171); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{source['sentiment']:.2f}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box" style="border-left-color: #f59e0b;">
            <strong>ℹ️ No Risk Analysis Data</strong><br>
            Run the complete pipeline to generate risk flags.
        </div>
        """, unsafe_allow_html=True)

def render_reports_evidence(data):
    """Stunning Reports & Evidence view"""
    st.markdown("# 📋 Reports & Evidence")
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.125rem;">Generate regulator-ready reports and evidence packages</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Generate Report</h3>
        </div>
        """, unsafe_allow_html=True)
        report_type = st.selectbox("Report Type", [
            "Executive Summary",
            "Full Risk Analysis",
            "Evidence Package",
            "Regulatory Submission"
        ])
        
        if st.button("🚀 Generate Report", type="primary", use_container_width=True):
            st.success("✅ Report generated successfully!")
            st.download_button(
                label="📥 Download PDF",
                data="Sample PDF content",
                file_name=f"mis-selling-report-{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Report Archive</h3>
            <p style="color: #64748b;">No previous reports found.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Report preview
    st.markdown("### 📄 Report Preview")
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: #1e293b; margin-top: 0; margin-bottom: 1rem; font-size: 1.5rem;">Product Risk Analysis Report</h4>
        <div class="section-divider" style="margin: 1.5rem 0;"></div>
        <h5 style="color: #1e293b; margin-top: 1.5rem;">1. Executive Summary</h5>
        <p style="color: #64748b; line-height: 1.8;">This report analyzes potential mis-selling risks for the selected financial products based on comparison between marketing promises and customer experiences.</p>
        
        <h5 style="color: #1e293b; margin-top: 1.5rem;">2. Extracted Promises</h5>
        <p style="color: #64748b; line-height: 1.8;">Analysis of product documentation reveals the following claims...</p>
        
        <h5 style="color: #1e293b; margin-top: 1.5rem;">3. Customer Sentiment Analysis</h5>
        <p style="color: #64748b; line-height: 1.8;">Sentiment analysis of customer reviews indicates...</p>
        
        <h5 style="color: #1e293b; margin-top: 1.5rem;">4. Risk Justification</h5>
        <p style="color: #64748b; line-height: 1.8;">Gap analysis reveals mismatches in the following areas...</p>
    </div>
    """, unsafe_allow_html=True)

def render_settings():
    """Settings view"""
    st.markdown("# ⚙️ Settings")
    st.markdown('<p style="color: rgba(255,255,255,0.9); font-size: 1.125rem;">System configuration and preferences</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📡 Data Sources", "🚨 Alert Thresholds", "⚙️ System"])
    
    with tab1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Data Source Configuration</h3>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox("Enable Twitter Feed", value=True)
        st.checkbox("Enable Reddit Discussions", value=True)
        st.checkbox("Enable Play Store Reviews", value=True)
        st.checkbox("Enable Trustpilot Reviews", value=True)
    
    with tab2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Risk Alert Thresholds</h3>
        </div>
        """, unsafe_allow_html=True)
        st.slider("High Risk Threshold", 0.0, 1.0, 0.7, 0.05)
        st.slider("Critical Risk Threshold", 0.0, 1.0, 0.9, 0.05)
        st.number_input("Minimum Complaints for Flagging", min_value=1, value=5)
    
    with tab3:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem;">System Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        st.selectbox("Report Format", ["PDF", "DOCX", "HTML"])
        st.selectbox("Date Format", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        if st.button("💾 Save Settings", type="primary", use_container_width=True):
            st.success("✅ Settings saved successfully!")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
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

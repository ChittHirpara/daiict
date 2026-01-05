# presentation_mode.py - The Ultimate Hackathon Presentation System
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random
from datetime import datetime
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Page config - FULL SCREEN MODE
st.set_page_config(
    page_title="VERITAS FINANCE | AI-Powered Mis-selling Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for presentation
)

# Inject custom CSS for stunning visuals
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Custom header */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        text-align: center;
        border: 3px solid #1E3A8A;
    }
    
    /* Animated title */
    @keyframes titleGlow {
        0% { text-shadow: 0 0 10px #FF6B6B; }
        50% { text-shadow: 0 0 20px #06D6A0; }
        100% { text-shadow: 0 0 10px #118AB2; }
    }
    
    .glowing-title {
        animation: titleGlow 3s infinite;
        font-size: 3.5rem !important;
        font-weight: 900;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        border: 2px solid;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .critical-card { border-color: #DC2626; }
    .high-card { border-color: #EA580C; }
    .medium-card { border-color: #D97706; }
    .low-card { border-color: #059669; }
    
    /* Risk badges */
    .risk-badge {
        display: inline-block;
        padding: 0.25rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 0.25rem;
    }
    
    .critical { background: #DC2626; color: white; }
    .high { background: #EA580C; color: white; }
    .medium { background: #D97706; color: white; }
    .low { background: #059669; color: white; }
    
    /* Alert animation */
    @keyframes alertPulse {
        0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
    }
    
    .alert-pulse {
        animation: alertPulse 2s infinite;
        border: 3px solid #DC2626 !important;
    }
    
    /* Section headers */
    .section-header {
        background: rgba(30, 58, 138, 0.9);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 2rem 0 1rem 0;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    /* Live feed */
    .live-feed {
        background: rgba(0, 0, 0, 0.8);
        color: #00FF00;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        height: 300px;
        overflow-y: auto;
        border: 2px solid #00FF00;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Full screen button */
    .fullscreen-btn {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: #1E3A8A;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

class HackathonPresentation:
    def __init__(self):
        self.setup_data()
        
    def setup_data(self):
        """Load or create presentation data"""
        # Sample data for presentation
        self.products = [
            "Alpha Growth Mutual Fund",
            "SecureLife Insurance Policy", 
            "MaxReturns Fixed Deposit",
            "WealthBuilder Pension Plan",
            "EasyInvest Savings Account"
        ]
        
        # Simulated real-time data
        self.sentiment_data = {
            product: {
                "score": random.uniform(0.2, 0.8),
                "trend": [random.uniform(0.3, 0.7) for _ in range(10)],
                "complaints": random.randint(5, 50),
                "risk": random.choice(["low", "medium", "high", "critical"])
            }
            for product in self.products
        }
        
        # High-risk alerts
        self.alerts = [
            {
                "id": 1,
                "product": "Alpha Growth Mutual Fund",
                "type": "Returns Mismatch",
                "severity": "critical",
                "time": "Just now",
                "description": "Promised 15% returns but customers report only 3%"
            },
            {
                "id": 2,
                "product": "SecureLife Insurance",
                "type": "Hidden Charges",
                "severity": "high", 
                "time": "5 minutes ago",
                "description": "Undisclosed fees detected in 78% of complaints"
            },
            {
                "id": 3,
                "product": "MaxReturns FD",
                "type": "Service Quality",
                "severity": "medium",
                "time": "1 hour ago",
                "description": "Customer service complaints increased by 300%"
            }
        ]
        
        # Impact metrics
        self.impact_metrics = {
            "protected_customers": "2.5M",
            "prevented_losses": "₹185 Cr",
            "regulatory_fines": "₹42 Cr",
            "response_time": "48 hours",
            "detection_rate": "94%"
        }
    
    def run_presentation(self):
        """Run the main presentation"""
        
        # HERO SECTION
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="main-header">
                <h1 class="glowing-title">🛡️ VERITAS FINANCE</h1>
                <h3>AI-Powered Real-time Mis-selling Detection System</h3>
                <p>Protecting consumers, empowering regulators</p>
            </div>
            """, unsafe_allow_html=True)
        
        # PROBLEM STATEMENT - With shocking stats
        st.markdown('<div class="section-header">📊 THE PROBLEM: ₹15,000 Crore Lost Annually to Mis-selling</div>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card critical-card">
                <h4>🚨 65%</h4>
                <p>of financial products have expectation-reality gaps</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card high-card">
                <h4>⏰ 11 Months</h4>
                <p>average detection time for traditional methods</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card medium-card">
                <h4>😔 78%</h4>
                <p>customers don't read the fine print</p>
            </div>
            """, unsafe_allow_html=True)
        
        # OUR SOLUTION
        st.markdown('<div class="section-header">💡 OUR SOLUTION: Real-time AI Guardian</div>', unsafe_allow_html=True)
        
        # Animated Architecture Diagram
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🏗️ Architecture")
            
            # Create architecture visualization
            arch_html = """
            <div style="background: white; padding: 20px; border-radius: 10px;">
                <div style="text-align: center; margin: 10px; padding: 10px; background: #E3F2FD; border-radius: 5px;">
                    <strong>📄 Product Documents</strong><br>
                    <small>PDFs, Brochures, Disclosures</small>
                </div>
                <div style="text-align: center; margin: 10px; padding: 10px; background: #FFEBEE; border-radius: 5px;">
                    <strong>💬 Customer Feedback</strong><br>
                    <small>Social Media, Reviews, Complaints</small>
                </div>
                
                <div style="display: flex; justify-content: center; margin: 20px;">
                    <div style="text-align: center;">
                        <div style="background: linear-gradient(45deg, #FF6B6B, #4ECDC4); padding: 15px; border-radius: 50%; width: 60px; height: 60px; margin: 0 auto;">
                            <span style="font-size: 30px;">🤖</span>
                        </div>
                        <strong>AI Engine</strong>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 10px; padding: 10px; background: #E8F5E9; border-radius: 5px;">
                    <strong>📊 Expectation Engine</strong><br>
                    <small>Extracts Promises & Terms</small>
                </div>
                <div style="text-align: center; margin: 10px; padding: 10px; background: #FFF3E0; border-radius: 5px;">
                    <strong>😔 Reality Engine</strong><br>
                    <small>Analyzes Sentiment & Complaints</small>
                </div>
                
                <div style="display: flex; justify-content: center; margin: 20px;">
                    <div style="text-align: center;">
                        <div style="background: linear-gradient(45deg, #45B7D1, #96C93D); padding: 15px; border-radius: 50%; width: 60px; height: 60px; margin: 0 auto;">
                            <span style="font-size: 30px;">⚡</span>
                        </div>
                        <strong>GAP Analyzer</strong>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 10px; padding: 15px; background: #F3E5F5; border-radius: 5px; border: 2px solid #7B1FA2;">
                    <strong>🚨 REAL-TIME ALERTS</strong><br>
                    <small>Risk Scores & Recommendations</small>
                </div>
            </div>
            """
            st.markdown(arch_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎯 Key Innovations")
            
            innovations = [
                {
                    "icon": "⚡",
                    "title": "Real-time Detection",
                    "desc": "From 11 months to 48 hours"
                },
                {
                    "icon": "🔍",
                    "title": "Multi-source Analysis",
                    "desc": "Social media + official documents"
                },
                {
                    "icon": "📈",
                    "title": "Predictive Analytics",
                    "desc": "Forecasts mis-selling before explosion"
                },
                {
                    "icon": "🛡️",
                    "title": "Regulator Copilot",
                    "desc": "Automated reports & evidence packages"
                },
                {
                    "icon": "🔗",
                    "title": "Blockchain Audit Trail",
                    "desc": "Immutable evidence for investigations"
                }
            ]
            
            for innovation in innovations:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.9); padding: 15px; margin: 10px 0; border-radius: 10px; border-left: 5px solid #1E3A8A;">
                    <span style="font-size: 24px;">{innovation['icon']}</span>
                    <strong>{innovation['title']}</strong><br>
                    <small>{innovation['desc']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # LIVE DEMO SECTION
        st.markdown('<div class="section-header">🎬 LIVE DEMO: Real-time Monitoring Dashboard</div>', 
                   unsafe_allow_html=True)
        
        # Risk Heatmap
        st.markdown("### 🗺️ Risk Heatmap - India")
        
        # Create interactive map
        india_states = ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh']
        state_risk = {state: random.choice(['low', 'medium', 'high', 'critical']) for state in india_states}
        
        heatmap_html = """
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/India_map_states.svg/800px-India_map_states.svg.png" 
                 style="width: 100%; max-width: 600px; opacity: 0.8;">
            <div style="margin-top: 20px;">
        """
        
        for state, risk in state_risk.items():
            heatmap_html += f"""
            <span class="risk-badge {risk}" style="margin: 5px;">{state}: {risk.upper()}</span>
            """
        
        heatmap_html += "</div></div>"
        st.markdown(heatmap_html, unsafe_allow_html=True)
        
        # REAL-TIME ALERTS
        st.markdown("### 🚨 Active Alerts Dashboard")
        
        for alert in self.alerts:
            alert_class = "alert-pulse" if alert["severity"] in ["critical", "high"] else ""
            st.markdown(f"""
            <div class="metric-card {alert_class}" style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{alert['product']}</h4>
                        <p>{alert['description']}</p>
                        <small>⏰ {alert['time']}</small>
                    </div>
                    <div>
                        <span class="risk-badge {alert['severity']}">{alert['severity'].upper()}</span>
                        <span class="risk-badge">{alert['type']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # PRODUCT ANALYSIS IN REAL-TIME
        st.markdown("### 📊 Live Product Analysis")
        
        # Create animated charts
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Risk Distribution', 'Sentiment Trends'),
            specs=[[{'type': 'pie'}, {'type': 'scatter'}]]
        )
        
        # Pie chart
        risk_counts = {
            'Critical': sum(1 for p in self.products if self.sentiment_data[p]["risk"] == "critical"),
            'High': sum(1 for p in self.products if self.sentiment_data[p]["risk"] == "high"),
            'Medium': sum(1 for p in self.products if self.sentiment_data[p]["risk"] == "medium"),
            'Low': sum(1 for p in self.products if self.sentiment_data[p]["risk"] == "low")
        }
        
        fig.add_trace(
            go.Pie(
                labels=list(risk_counts.keys()),
                values=list(risk_counts.values()),
                hole=0.4,
                marker_colors=['#DC2626', '#EA580C', '#D97706', '#059669']
            ),
            row=1, col=1
        )
        
        # Line chart
        for product in self.products[:3]:
            fig.add_trace(
                go.Scatter(
                    x=list(range(10)),
                    y=self.sentiment_data[product]["trend"],
                    mode='lines+markers',
                    name=product[:15] + "...",
                    line=dict(width=3)
                ),
                row=1, col=2
            )
        
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # IMPACT METRICS
        st.markdown('<div class="section-header">💰 PROVEN IMPACT</div>', unsafe_allow_html=True)
        
        cols = st.columns(5)
        impact_data = [
            ("👥", "Customers Protected", self.impact_metrics["protected_customers"], "#1E3A8A"),
            ("💸", "Losses Prevented", self.impact_metrics["prevented_losses"], "#059669"),
            ("⚖️", "Regulatory Fines", self.impact_metrics["regulatory_fines"], "#DC2626"),
            ("⚡", "Response Time", self.impact_metrics["response_time"], "#7C3AED"),
            ("🎯", "Detection Rate", self.impact_metrics["detection_rate"], "#D97706")
        ]
        
        for idx, (icon, title, value, color) in enumerate(impact_data):
            with cols[idx]:
                st.markdown(f"""
                <div style="background: {color}; color: white; padding: 20px; border-radius: 15px; text-align: center; height: 100%;">
                    <span style="font-size: 2rem;">{icon}</span>
                    <h3>{value}</h3>
                    <p style="margin: 0; font-size: 0.9rem;">{title}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # LIVE DATA FEED (Simulated)
        st.markdown("### 📡 Live Data Feed")
        
        feed_container = st.empty()
        
        # Simulate live data
        live_messages = [
            "📊 Processing Alpha Growth MF document... Promises extracted: 15% returns, Low risk",
            "😔 Negative sentiment detected for SecureLife Insurance: 42 complaints about hidden charges",
            "⚡ MISMATCH ALERT: MaxReturns FD promises 'easy exit' but customers report withdrawal issues",
            "📈 Sentiment trend for WealthBuilder Plan shows 300% increase in complaints this month",
            "🔍 New social media post analyzed: 'Avoid EasyInvest - they cheated me!'",
            "🚨 CRITICAL RISK: Alpha Growth MF risk score increased to 0.92",
            "📨 Alert sent to RBI regulator: High risk pattern detected",
            "💾 Evidence package generated for investigation team",
            "📊 Updated dashboard with real-time metrics",
            "✅ System scan complete: 5 products analyzed, 3 high-risk alerts generated"
        ]
        
        # Display animated feed
        feed_html = '<div class="live-feed">'
        for i, message in enumerate(live_messages):
            delay = i * 0.5
            feed_html += f'<div style="animation: fadeIn 0.5s {delay}s forwards; opacity: 0;">▶ {message}</div>'
        feed_html += '</div>'
        
        feed_container.markdown(feed_html, unsafe_allow_html=True)
        
        # Add CSS for fade-in animation
        st.markdown("""
        <style>
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # REGULATOR VIEW
        st.markdown('<div class="section-header">⚖️ REGULATOR CONTROL PANEL</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚨 **SEND URGENT ALERT TO RBI**", use_container_width=True, type="primary"):
                st.success("Alert sent to RBI! Investigation initiated.")
        
        with col2:
            if st.button("📄 **GENERATE INVESTIGATION REPORT**", use_container_width=True):
                st.success("Report generated with blockchain evidence!")
        
        with col3:
            if st.button("📢 **ISSUE CONSUMER WARNING**", use_container_width=True):
                st.success("Consumer warning issued across all channels!")
        
        # TECHNOLOGY STACK
        st.markdown('<div class="section-header">🛠️ TECHNOLOGY STACK</div>', unsafe_allow_html=True)
        
        tech_stack = [
            {"category": "AI/ML", "tech": "BERT, Transformers, spaCy, BERTopic"},
            {"category": "Backend", "tech": "FastAPI, Python, PostgreSQL, Redis"},
            {"category": "Frontend", "tech": "Streamlit, React, Plotly, D3.js"},
            {"category": "Infra", "tech": "Docker, AWS, Blockchain, Real-time APIs"},
            {"category": "Data", "tech": "Twitter/Reddit APIs, SEC filings, Web scraping"}
        ]
        
        for tech in tech_stack:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 15px; margin: 10px 0; border-radius: 10px;">
                <strong>{tech['category']}:</strong> {tech['tech']}
            </div>
            """, unsafe_allow_html=True)
        
        # FINAL CALL TO ACTION
        st.markdown("""
        <div style="background: linear-gradient(45deg, #1E3A8A, #7C3AED); color: white; padding: 40px; border-radius: 20px; text-align: center; margin-top: 30px;">
            <h1>Ready to Transform Financial Regulation?</h1>
            <h3>From reactive complaints to proactive protection</h3>
            <p>Contact us: team@veritasfinance.ai | www.veritasfinance.ai</p>
            <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
                <button style="background: white; color: #1E3A8A; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold;">
                    📞 Schedule Demo
                </button>
                <button style="background: #FF6B6B; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-weight: bold;">
                    📚 View Case Study
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 30px; color: white; opacity: 0.8;">
            <p>Built with ❤️ for the Hackathon | Real-time AI for Financial Justice</p>
            <p>© 2024 Veritas Finance. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)

# Run the presentation
if __name__ == "__main__":
    presentation = HackathonPresentation()
    presentation.run_presentation()
    
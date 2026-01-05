# dashboard.py - Streamlit Dashboard for Live Demo
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Veritas Finance - Mis-selling Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-critical { color: #DC2626; font-weight: bold; }
    .risk-high { color: #EA580C; font-weight: bold; }
    .risk-medium { color: #D97706; font-weight: bold; }
    .risk-low { color: #059669; font-weight: bold; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class VeritasDashboard:
    def __init__(self):
        self.load_data()
        
    def load_data(self):
        """Load processed data"""
        self.promises_df = pd.read_csv("data/processed/extracted_promises.csv") \
            if os.path.exists("data/processed/extracted_promises.csv") else None
        
        self.sentiment_df = pd.read_csv("data/processed/sentiment_analysis.csv") \
            if os.path.exists("data/processed/sentiment_analysis.csv") else None
        
        self.gap_df = pd.read_csv("data/processed/gap_analysis.csv") \
            if os.path.exists("data/processed/gap_analysis.csv") else None
    
    def run(self):
        """Run the dashboard"""
        # Header
        st.markdown('<h1 class="main-header">🔍 Veritas Finance - Mis-selling Detection System</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar
        with st.sidebar:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
            st.title("Navigation")
            
            page = st.radio(
                "Go to",
                ["🏠 Dashboard", "📊 Product Analysis", "⚠️ Risk Alerts", "📈 Insights", "⚙️ Settings"]
            )
            
            st.markdown("---")
            st.info(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Main content based on page selection
        if page == "🏠 Dashboard":
            self.show_dashboard()
        elif page == "📊 Product Analysis":
            self.show_product_analysis()
        elif page == "⚠️ Risk Alerts":
            self.show_risk_alerts()
        elif page == "📈 Insights":
            self.show_insights()
        else:
            self.show_settings()
    
    def show_dashboard(self):
        """Show main dashboard"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>Products Analyzed</h3>
                <h2>5</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>High Risk Products</h3>
                <h2>2</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>Total Mismatches</h3>
                <h2>12</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>Avg Dissatisfaction</h3>
                <h2>45%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Risk Distribution")
            if self.gap_df is not None:
                fig = go.Figure(data=[go.Pie(
                    labels=self.gap_df['risk_level'],
                    values=[1] * len(self.gap_df),
                    hole=.3
                )])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top Mismatch Types")
            # Sample data - replace with actual
            mismatch_data = {'Returns': 5, 'Risk': 4, 'Fees': 3, 'Service': 2}
            fig = go.Figure(data=[go.Bar(
                x=list(mismatch_data.keys()),
                y=list(mismatch_data.values()),
                marker_color=['#FF6B6B', '#FFD166', '#06D6A0', '#118AB2']
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent Alerts
        st.subheader("🚨 Recent High-Risk Alerts")
        alerts = [
            {"product": "Alpha Growth Mutual Fund", "risk": "Critical", "issue": "Returns mismatch", "time": "2 hours ago"},
            {"product": "SecureLife Insurance", "risk": "High", "issue": "Hidden charges", "time": "5 hours ago"},
            {"product": "MaxReturns FD", "risk": "Medium", "issue": "Service complaints", "time": "1 day ago"}
        ]
        
        for alert in alerts:
            risk_class = f"risk-{alert['risk'].lower()}"
            st.markdown(f"""
            <div style="padding: 10px; border-left: 5px solid; margin: 5px 0; background: #f8f9fa">
                <strong>{alert['product']}</strong> • 
                <span class="{risk_class}">{alert['risk']}</span> • 
                {alert['issue']} • 
                <small>{alert['time']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    def show_product_analysis(self):
        """Show detailed product analysis"""
        st.subheader("Product Analysis")
        
        if self.gap_df is not None and self.promises_df is not None:
            # Product selector
            products = self.gap_df['product_name'].tolist()
            selected_product = st.selectbox("Select Product", products)
            
            if selected_product:
                product_gap = self.gap_df[self.gap_df['product_name'] == selected_product].iloc[0]
                product_promise = self.promises_df[self.promises_df['product_name'] == selected_product].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📝 Product Promises")
                    st.metric("Promised Returns", product_promise.get('promised_returns', 'N/A'))
                    st.metric("Risk Category", product_promise.get('risk_category', 'N/A'))
                    st.metric("Lock-in Period", product_promise.get('lock_in_period', 'N/A'))
                    
                    st.markdown("**Key Features:**")
                    for feature in eval(product_promise.get('key_features', '[]')):
                        st.write(f"- {feature}")
                
                with col2:
                    st.markdown("### 😔 Customer Reality")
                    risk_class = f"risk-{product_gap['risk_level'].lower()}"
                    st.markdown(f"**Risk Level**: <span class='{risk_class}'>{product_gap['risk_level'].upper()}</span>", 
                              unsafe_allow_html=True)
                    st.metric("Risk Score", f"{product_gap['overall_risk_score']:.2f}/1.0")
                    st.metric("Dissatisfaction", f"{product_gap['dissatisfaction_index']:.1f}%")
                    
                    if isinstance(product_gap.get('mismatches', ''), str):
                        try:
                            mismatches = eval(product_gap['mismatches'])
                            st.markdown("**Detected Mismatches:**")
                            for mismatch in mismatches[:3]:
                                st.write(f"- {mismatch.get('promise_aspect', 'Unknown')}: {mismatch.get('complaint_topic', '')}")
                        except:
                            pass
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                if isinstance(product_gap.get('recommendations', ''), str):
                    try:
                        recommendations = eval(product_gap['recommendations'])
                        for rec in recommendations[:5]:
                            st.info(rec)
                    except:
                        st.info("Review product disclosures and customer complaints")
    
    def show_risk_alerts(self):
        """Show risk alerts and notifications"""
        st.subheader("⚠️ Risk Alerts Dashboard")
        
        # Create sample alert data
        alerts_data = {
            "Product": ["Alpha Growth MF", "SecureLife Insurance", "MaxReturns FD", "WealthBuilder Plan"],
            "Risk Level": ["Critical", "High", "Medium", "Low"],
            "Score": [0.92, 0.78, 0.45, 0.22],
            "Mismatches": [4, 3, 2, 1],
            "Dissatisfaction": [85, 72, 45, 20],
            "Last Updated": ["2h ago", "5h ago", "1d ago", "2d ago"]
        }
        
        alerts_df = pd.DataFrame(alerts_data)
        
        # Color code risk levels
        def color_risk(val):
            if val == "Critical":
                return "background-color: #FFCCCC; color: #CC0000"
            elif val == "High":
                return "background-color: #FFE5CC; color: #FF6600"
            elif val == "Medium":
                return "background-color: #FFFFCC; color: #CC9900"
            else:
                return "background-color: #CCFFCC; color: #006600"
        
        styled_df = alerts_df.style.applymap(color_risk, subset=['Risk Level'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Alert details
        st.subheader("📋 Alert Details")
        selected_alert = st.selectbox("Select Alert for Details", alerts_df["Product"].tolist())
        
        if selected_alert:
            alert = alerts_df[alerts_df["Product"] == selected_alert].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Risk Score", f"{alert['Score']:.2f}")
                st.metric("Mismatches", alert['Mismatches'])
            with col2:
                st.metric("Dissatisfaction", f"{alert['Dissatisfaction']}%")
                st.metric("Status", "Active" if alert['Score'] > 0.5 else "Monitoring")
            
            # Action buttons
            st.markdown("### 🛠️ Recommended Actions")
            if alert['Risk Level'] in ['Critical', 'High']:
                st.warning("Immediate action required!")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🚨 Initiate Investigation", key="investigate"):
                        st.success("Investigation initiated!")
                with col2:
                    if st.button("📢 Issue Consumer Alert", key="alert"):
                        st.success("Consumer alert issued!")
                with col3:
                    if st.button("⏸️ Suspend Sales", key="suspend"):
                        st.success("Sales suspended pending review!")
    
    def show_insights(self):
        """Show insights and trends"""
        st.subheader("📈 Insights & Trends")
        
        # Sentiment trend chart
        st.markdown("### Customer Sentiment Trend")
        
        # Sample time series data
        dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
        sentiment_trend = pd.DataFrame({
            'Date': dates,
            'Alpha Growth MF': [0.6 + 0.2 * (i % 7)/7 for i in range(30)],
            'SecureLife Insurance': [0.4 + 0.3 * ((i+3) % 10)/10 for i in range(30)],
            'MaxReturns FD': [0.7 - 0.1 * (i % 5)/5 for i in range(30)]
        })
        
        fig = go.Figure()
        for col in sentiment_trend.columns[1:]:
            fig.add_trace(go.Scatter(
                x=sentiment_trend['Date'],
                y=sentiment_trend[col],
                mode='lines',
                name=col
            ))
        
        fig.update_layout(
            title="Sentiment Trends Over Time",
            xaxis_title="Date",
            yaxis_title="Sentiment Score",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Mismatch patterns
        st.markdown("### Common Mismatch Patterns")
        patterns = {
            "Pattern": ["Returns Overpromise", "Risk Undisclosed", "Hidden Fees", "Service Gap"],
            "Frequency": [45, 32, 28, 19],
            "Severity": [0.8, 0.9, 0.7, 0.5],
            "Affected Products": ["Mutual Funds", "Insurance", "All", "Insurance"]
        }
        
        patterns_df = pd.DataFrame(patterns)
        st.dataframe(patterns_df, use_container_width=True)
        
        # Regulatory impact
        st.markdown("### Estimated Regulatory Impact")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Potential Fines", "₹2.5 Cr", "25%")
        with col2:
            st.metric("Consumer Compensation", "₹15 Cr", "40%")
        with col3:
            st.metric("Prevented Losses", "₹50 Cr", "60%")
    
    def show_settings(self):
        """Show settings and configuration"""
        st.subheader("⚙️ System Configuration")
        
        with st.form("config_form"):
            st.markdown("### Data Sources")
            twitter_enabled = st.checkbox("Twitter Feed", value=True)
            reddit_enabled = st.checkbox("Reddit Discussions", value=True)
            playstore_enabled = st.checkbox("Play Store Reviews", value=True)
            trustpilot_enabled = st.checkbox("Trustpilot Reviews", value=True)
            
            st.markdown("### Alert Settings")
            risk_threshold = st.slider("Risk Threshold for Alerts", 0.0, 1.0, 0.7, 0.05)
            check_frequency = st.selectbox("Check Frequency", ["Real-time", "Hourly", "Daily", "Weekly"])
            
            st.markdown("### Notification Channels")
            email_alerts = st.checkbox("Email Alerts", value=True)
            sms_alerts = st.checkbox("SMS Alerts", value=False)
            webhook_alerts = st.checkbox("Webhook Alerts", value=False)
            
            submitted = st.form_submit_button("Save Configuration")
            if submitted:
                st.success("Configuration saved successfully!")

# Run the dashboard
if __name__ == "__main__":
    dashboard = VeritasDashboard()
    dashboard.run()
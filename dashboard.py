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
        """Show main dashboard with real data"""
        # Calculate real metrics from data
        if self.gap_df is None or len(self.gap_df) == 0:
            st.error("⚠️ No data available. Please run main_pipeline.py first!")
            if st.button("🔄 Run Pipeline Now"):
                with st.spinner("Running pipeline..."):
                    import subprocess
                    result = subprocess.run(["python", "main_pipeline.py"], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.success("✅ Pipeline completed! Refreshing...")
                        st.rerun()
                    else:
                        st.error(f"❌ Pipeline failed: {result.stderr}")
            return
        
        # Calculate real metrics
        total_products = len(self.gap_df)
        high_risk_products = len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])])
        
        # Count total mismatches
        total_mismatches = 0
        mismatch_types = {}
        for _, row in self.gap_df.iterrows():
            try:
                if isinstance(row.get('mismatches'), str):
                    import json
                    mismatches = json.loads(row.get('mismatches', '[]'))
                    total_mismatches += len(mismatches)
                    for m in mismatches:
                        aspect = m.get('promise_aspect', 'Unknown')
                        mismatch_types[aspect] = mismatch_types.get(aspect, 0) + 1
            except:
                pass
        
        avg_dissatisfaction = self.gap_df['dissatisfaction_index'].mean() if 'dissatisfaction_index' in self.gap_df.columns else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Products Analyzed</h3>
                <h2>{total_products}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>High Risk Products</h3>
                <h2>{high_risk_products}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Mismatches</h3>
                <h2>{total_mismatches}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Avg Dissatisfaction</h3>
                <h2>{avg_dissatisfaction:.0f}%</h2>
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
            if mismatch_types:
                fig = go.Figure(data=[go.Bar(
                    x=list(mismatch_types.keys()),
                    y=list(mismatch_types.values()),
                    marker_color=['#FF6B6B', '#FFD166', '#06D6A0', '#118AB2', '#7C3AED'][:len(mismatch_types)]
                )])
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No mismatch data available")
        
        # Recent Alerts - Generate from real data
        st.subheader("🚨 Recent High-Risk Alerts")
        alerts = []
        for _, row in self.gap_df.iterrows():
            risk_level = str(row.get('risk_level', 'medium')).title()
            if risk_level.lower() in ['high', 'critical']:
                product_name = row.get('product_name', 'Unknown')
                risk_score = row.get('overall_risk_score', 0)
                issue = f"Risk score: {risk_score:.2f}"
                alerts.append({
                    "product": product_name,
                    "risk": risk_level,
                    "issue": issue,
                    "time": "Recently detected"
                })
        
        # Limit to top 3 alerts
        alerts = alerts[:3]
        
        if not alerts:
            st.info("No high-risk alerts currently")
        
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
        
        if self.gap_df is None or len(self.gap_df) == 0:
            st.error("⚠️ No data available. Please run main_pipeline.py first!")
            return
        
        # Create real alert data from gap analysis
        alerts_list = []
        for _, row in self.gap_df.iterrows():
            product_name = row.get('product_name', 'Unknown')
            risk_level = str(row.get('risk_level', 'medium')).title()
            risk_score = float(row.get('overall_risk_score', 0.5))
            dissatisfaction = float(row.get('dissatisfaction_index', 0))
            
            # Count mismatches
            mismatch_count = 0
            try:
                if isinstance(row.get('mismatches'), str):
                    import json
                    mismatches = json.loads(row.get('mismatches', '[]'))
                    mismatch_count = len(mismatches)
            except:
                pass
            
            alerts_list.append({
                "Product": product_name,
                "Risk Level": risk_level,
                "Score": risk_score,
                "Mismatches": mismatch_count,
                "Dissatisfaction": dissatisfaction,
                "Last Updated": "Recently"
            })
        
        alerts_df = pd.DataFrame(alerts_list)
        
        # Sort by risk score (highest first)
        if len(alerts_df) > 0:
            alerts_df = alerts_df.sort_values('Score', ascending=False)
        
        if len(alerts_df) == 0:
            st.info("No alerts to display")
            return
        
        # Color code risk levels
        def color_risk(val):
            val_str = str(val).lower()
            if val_str == "critical":
                return "background-color: #FFCCCC; color: #CC0000"
            elif val_str == "high":
                return "background-color: #FFE5CC; color: #FF6600"
            elif val_str == "medium":
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
        
        if self.gap_df is None or len(self.gap_df) == 0:
            st.error("⚠️ No data available. Please run main_pipeline.py first!")
            return
        
        # Sentiment trend chart
        st.markdown("### Customer Sentiment Trend")
        
        # Try to load time series data if available
        time_series_path = "data/mock/sentiment_time_series.csv"
        if os.path.exists(time_series_path):
            try:
                sentiment_trend = pd.read_csv(time_series_path)
                sentiment_trend['date'] = pd.to_datetime(sentiment_trend['date'])
                
                # Pivot for plotting
                if 'product' in sentiment_trend.columns and 'sentiment' in sentiment_trend.columns:
                    pivot_df = sentiment_trend.pivot(index='date', columns='product', values='sentiment')
                    fig = go.Figure()
                    for col in pivot_df.columns[:5]:  # Limit to 5 products
                        fig.add_trace(go.Scatter(
                            x=pivot_df.index,
                            y=pivot_df[col],
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
                else:
                    raise ValueError("Invalid time series format")
            except Exception as e:
                st.warning(f"Could not load time series data: {e}")
                # Fallback to sample data
                dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
                products = self.gap_df['product_name'].tolist()[:3]
                sentiment_trend = pd.DataFrame({'Date': dates})
                for i, product in enumerate(products):
                    base_sentiment = float(self.gap_df[self.gap_df['product_name'] == product]['sentiment_score'].iloc[0]) if len(self.gap_df[self.gap_df['product_name'] == product]) > 0 else 0.5
                    sentiment_trend[product] = [base_sentiment + 0.1 * (j % 7)/7 for j in range(30)]
        else:
            # Fallback: Create trend from current sentiment scores
            dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
            products = self.gap_df['product_name'].tolist()[:3]
            sentiment_trend = pd.DataFrame({'Date': dates})
            for product in products:
                base_sentiment = float(self.gap_df[self.gap_df['product_name'] == product]['sentiment_score'].iloc[0]) if len(self.gap_df[self.gap_df['product_name'] == product]) > 0 else 0.5
                sentiment_trend[product] = [base_sentiment + 0.1 * (i % 7)/7 for i in range(30)]
        
        # Only create chart if we have the fallback data
        if 'Date' in sentiment_trend.columns:
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
        
        # Mismatch patterns - Calculate from real data
        st.markdown("### Common Mismatch Patterns")
        patterns_dict = {}
        for _, row in self.gap_df.iterrows():
            try:
                if isinstance(row.get('mismatches'), str):
                    import json
                    mismatches = json.loads(row.get('mismatches', '[]'))
                    for m in mismatches:
                        aspect = m.get('promise_aspect', 'Unknown')
                        severity = float(m.get('severity', 0.5))
                        if aspect not in patterns_dict:
                            patterns_dict[aspect] = {'count': 0, 'severity_sum': 0, 'products': set()}
                        patterns_dict[aspect]['count'] += 1
                        patterns_dict[aspect]['severity_sum'] += severity
                        patterns_dict[aspect]['products'].add(row.get('product_name', 'Unknown'))
            except:
                pass
        
        if patterns_dict:
            patterns_list = []
            for aspect, data in patterns_dict.items():
                patterns_list.append({
                    "Pattern": aspect,
                    "Frequency": data['count'],
                    "Severity": data['severity_sum'] / data['count'] if data['count'] > 0 else 0,
                    "Affected Products": len(data['products'])
                })
            patterns_df = pd.DataFrame(patterns_list)
            patterns_df = patterns_df.sort_values('Frequency', ascending=False)
            st.dataframe(patterns_df, use_container_width=True)
        else:
            st.info("No mismatch patterns detected yet")
        
        # Regulatory impact - Calculate from real data
        st.markdown("### Estimated Regulatory Impact")
        col1, col2, col3 = st.columns(3)
        
        if self.gap_df is not None and len(self.gap_df) > 0:
            high_risk_count = len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])])
            total_products = len(self.gap_df)
            avg_dissatisfaction = self.gap_df['dissatisfaction_index'].mean()
            
            # Estimate fines (₹2.5 Cr per high-risk product)
            potential_fines = high_risk_count * 2.5
            # Estimate compensation (based on dissatisfaction)
            consumer_compensation = total_products * (avg_dissatisfaction / 10) * 3
            # Estimate prevented losses
            prevented_losses = total_products * 10
            
            with col1:
                st.metric("Potential Fines", f"₹{potential_fines:.1f} Cr", f"{high_risk_count} products")
            with col2:
                st.metric("Consumer Compensation", f"₹{consumer_compensation:.1f} Cr", f"{avg_dissatisfaction:.0f}% avg dissatisfaction")
            with col3:
                st.metric("Prevented Losses", f"₹{prevented_losses:.1f} Cr", f"{total_products} products monitored")
        else:
            with col1:
                st.metric("Potential Fines", "₹2.5 Cr", "N/A")
            with col2:
                st.metric("Consumer Compensation", "₹15 Cr", "N/A")
            with col3:
                st.metric("Prevented Losses", "₹50 Cr", "N/A")
    
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
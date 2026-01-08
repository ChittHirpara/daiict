# dashboard.py - Streamlit Dashboard for Live Demo
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import base64
from datetime import datetime
import json

# Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="Veritas Finance - Mis-selling Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME MANAGEMENT ---
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'dark'  # Default to Premium Black

def toggle_theme():
    if st.session_state['theme'] == 'dark':
        st.session_state['theme'] = 'light'
    else:
        st.session_state['theme'] = 'dark'

# --- CSS INJECTION ---
def inject_custom_css():
    theme = st.session_state['theme']
    
    if theme == 'dark':
        # PREMIUM BLACK & GOLD THEME
        bg_color = "#000000"  # True Black
        card_bg = "#111111"   # Very dark grey/black
        text_color = "#FFFFFF"
        accent_color = "#D4AF37" # Gold
        secondary_accent = "#00E5FF" # Cyan/Tech
        border_color = "#333333"
    else:
        # LIGHT / MODERN THEME
        bg_color = "#F8F9FA"
        card_bg = "#FFFFFF"
        text_color = "#1F2937"
        accent_color = "#2563EB" # Blue
        secondary_accent = "#7C3AED" # Purple
        border_color = "#E5E7EB"

    st.markdown(f"""
    <style>
        /* MAIN BACKGROUND */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* HEADERS */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            font-family: 'Inter', sans-serif;
        }}
        
        .main-header {{
            font-size: 2.5rem;
            color: {accent_color}; /* Theme Color */
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 700;
            text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.2);
        }}
        
        /* SIDEBAR */
        [data-testid="stSidebar"] {{
            background-color: {card_bg};
            border-right: 1px solid {border_color};
        }}
        
        /* METRIC CARDS */
        .metric-card {{
            background: {card_bg};
            padding: 20px;
            border-radius: 12px;
            border: 1px solid {border_color};
            color: {text_color};
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            border-color: {accent_color};
        }}
        .metric-card h3 {{
            color: {text_color};
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.8;
            margin-bottom: 5px;
        }}
        .metric-card h2 {{
            color: {accent_color};
            font-size: 2.2rem;
            margin: 0;
            font-weight: bold;
        }}
        
        /* RISK TAGS */
        .risk-critical {{ color: #FF3B30; font-weight: bold; }}
        .risk-high {{ color: #FF9500; font-weight: bold; }}
        .risk-medium {{ color: #FFCC00; font-weight: bold; }}
        .risk-low {{ color: #34C759; font-weight: bold; }}
        
        /* BUTTONS */
        .stButton>button {{
            background-color: {accent_color};
            color: {'black' if theme == 'dark' else 'white'};
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            opacity: 0.9;
            box-shadow: 0 0 15px {accent_color}40;
        }}
        
        /* CHAT INTERFACE */
        .chat-container {{
            border: 1px solid {border_color};
            background-color: {card_bg};
            border-radius: 10px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            margin-bottom: 10px;
        }}
        .user-msg {{
            background-color: {accent_color}20; /* 20% opacity */
            padding: 8px 12px;
            border-radius: 15px 15px 0 15px;
            margin: 5px 0 5px auto;
            max-width: 80%;
            text-align: right;
            border: 1px solid {accent_color};
        }}
        .ai-msg {{
            background-color: {border_color};
            padding: 8px 12px;
            border-radius: 15px 15px 15px 0;
            margin: 5px auto 5px 0;
            max-width: 80%;
            border: 1px solid {border_color};
        }}
    </style>
    """, unsafe_allow_html=True)

class VeritasDashboard:
    def __init__(self):
        inject_custom_css()
        self.load_data()
        
        # Initialize Auth Manager
        try:
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent))
            from backend.auth.auth_manager import AuthManager
            self.auth = AuthManager()
        except ImportError:
            self.auth = None
        
        # Initialize AI Assistant
        try:
            from backend.ai_assistant import VeritasAssistant
            if 'ai_assistant' not in st.session_state:
                st.session_state.ai_assistant = VeritasAssistant()
        except ImportError:
            st.session_state.ai_assistant = None
            
        # Initialize Chat History
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! I am Veritas AI. Ask me anything about risk analysis or regulations."}
            ]
            
        # Session state initialization
        if 'user' not in st.session_state:
            st.session_state['user'] = None
        
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
        # Authentication Gate
        if not st.session_state['user']:
            self.show_login_page()
            return

        # LOGGED IN VIEW
        user = st.session_state['user']
        
        # User & Theme Controls (Top Right)
        col_title, col_controls = st.columns([3, 1])
        with col_title:
             st.markdown(f'<h1 class="main-header">🔍 Veritas Finance AI</h1>', unsafe_allow_html=True)
        with col_controls:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🌓 Theme"):
                    toggle_theme()
                    st.rerun()
            with c2:
                if st.button("🚪 Logout"):
                    st.session_state['user'] = None
                    st.session_state['user_face'] = None  # Clear face on logout
                    st.rerun()

        # Sidebar with AI Assistant
        with st.sidebar:
            if st.session_state.get('user_face') is not None:
                st.image(st.session_state['user_face'], width=100, caption=f"ID Verified: {user}")
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
            
            st.markdown(f"### 👤 {user}")
            st.markdown("---")
            
            # Navigation
            st.markdown("### 🧭 Navigation")
            page = st.radio(
                "Go to",
                ["🏠 Dashboard", "📊 Product Analysis", "⚠️ Risk Alerts", "📈 Insights", "🧪 Live Analysis Lab", "⚙️ Settings"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            
            # AI Assistant Widget
            with st.expander("🤖 Veritas AI Assistant", expanded=False):
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                
                # Show history (last 5 messages)
                for msg in st.session_state.chat_history[-6:]:
                    div_class = "user-msg" if msg['role'] == "user" else "ai-msg"
                    st.markdown(f'<div class="{div_class}">{msg["content"]}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Input
                user_q = st.text_input("Ask about risks...", key="sidebar_chat_input")
                if st.button("Send", key="sidebar_chat_send"):
                    if user_q and st.session_state.ai_assistant:
                        # Add user msg
                        st.session_state.chat_history.append({"role": "user", "content": user_q})
                        
                        # Get AI response
                        with st.spinner("Thinking..."):
                            response = st.session_state.ai_assistant.get_response(user_q)
                        
                        # Add AI msg
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        st.rerun()

        # Main content based on page selection
        if page == "🏠 Dashboard":
            self.show_dashboard()
        elif page == "📊 Product Analysis":
            self.show_product_analysis()
        elif page == "⚠️ Risk Alerts":
            self.show_risk_alerts()
        elif page == "📈 Insights":
            self.show_insights()
        elif page == "🧪 Live Analysis Lab":
            self.show_live_analysis()
        else:
            self.show_settings()

    def show_login_page(self):
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div style="background-color: {'#111' if st.session_state['theme'] == 'dark' else '#fff'}; padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #333;">
                <h1>🔐 Login to Veritas</h1>
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Login", "Sign Up"])
            
            with tab1:
                login_method = st.radio("Method", ["Password", "Face ID"], horizontal=True)
                if login_method == "Password":
                    username = st.text_input("Username", key="login_user")
                    password = st.text_input("Password", type="password", key="login_pass")
                    if st.button("🚀 Login Now", use_container_width=True):
                        success, msg = self.auth.login(username, password)
                        if success:
                            st.session_state['user'] = username
                            st.rerun()
                        else:
                            st.error(msg)
                else: # Face ID
                    st.info("Look at the camera for Face ID")
                    img_file = st.camera_input("Scan Face", key="login_cam")
                    if img_file is not None:
                         # Process image (Copy of previous logic)
                        bytes_data = img_file.getvalue()
                        import cv2
                        import numpy as np
                        nparr = np.frombuffer(bytes_data, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        if self.auth:
                            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            encoding = self.auth.get_face_encoding_from_image(rgb_img)
                            if encoding is not None:
                                success, username = self.auth.login_with_face(encoding)
                                if success:
                                    st.session_state['user'] = username
                                    # Save image for display (convert BGR to RGB)
                                    st.session_state['user_face'] = rgb_img
                                    st.rerun()
                                else:
                                    st.error("Face not recognized")
            
            with tab2:
                new_user = st.text_input("New Username", key="signup_user")
                new_pass = st.text_input("New Password", type="password", key="signup_pass")
                enable_face = st.checkbox("Enable Face ID for Signup")
                face_enc = None
                if enable_face:
                     reg_img = st.camera_input("Capture Face", key="signup_cam")
                     if reg_img:
                         import cv2
                         import numpy as np
                         bytes_data = reg_img.getvalue()
                         nparr = np.frombuffer(bytes_data, np.uint8)
                         img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                         rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                         if self.auth:
                             face_enc = self.auth.get_face_encoding_from_image(rgb_img)
                
                if st.button("Create Account", use_container_width=True):
                    success, msg = self.auth.signup(new_user, new_pass, face_enc)
                    if success: st.success("Account created! Login now.")
                    else: st.error(msg)
    
    def show_dashboard(self):
        """Show main dashboard with real data"""
        if self.gap_df is None or len(self.gap_df) == 0:
            st.error("⚠️ No data available. Please run main_pipeline.py first!")
            return
        
        # Calculate real metrics
        total_products = len(self.gap_df)
        high_risk_products = len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])])
        
        # Count total mismatches
        total_mismatches = 0
        for _, row in self.gap_df.iterrows():
            try:
                if isinstance(row.get('mismatches'), str):
                    mismatches = json.loads(row.get('mismatches', '[]'))
                    total_mismatches += len(mismatches)
            except: pass
        
        avg_dissatisfaction = self.gap_df['dissatisfaction_index'].mean() if 'dissatisfaction_index' in self.gap_df.columns else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Analyzed</h3><h2>{total_products}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>High Risk</h3><h2>{high_risk_products}</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><h3>Violations</h3><h2>{total_mismatches}</h2></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><h3>Dissatisfaction</h3><h2>{avg_dissatisfaction:.0f}%</h2></div>', unsafe_allow_html=True)
        
        st.markdown("### 📊 Live Risk Monitor")
        col1, col2 = st.columns(2)
        with col1:
            if self.gap_df is not None:
                fig = go.Figure(data=[go.Pie(labels=self.gap_df['risk_level'], values=[1]*len(self.gap_df), hole=.4)])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white" if st.session_state['theme']=='dark' else "black"})
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Recent Alerts**")
            for _, row in self.gap_df.head(3).iterrows():
                risk = row['risk_level'].upper()
                name = row['product_name']
                score = row['overall_risk_score']
                risk_color = "#FF3B30" if risk in ['HIGH', 'CRITICAL'] else "#34C759"
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 10px; margin-bottom: 5px; border-left: 4px solid {risk_color}; color: inherit;">
                    <strong>{name}</strong><br>
                    <small>Risk: {risk} | Score: {score:.2f}</small>
                </div>
                """, unsafe_allow_html=True)
    
    def show_product_analysis(self):
        """Show detailed product analysis"""
        st.subheader("Product Analysis")
        
        if self.gap_df is not None and self.promises_df is not None:
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
                    try:
                        features = eval(product_promise.get('key_features', '[]'))
                        for feature in features:
                            st.write(f"- {feature}")
                    except:
                        st.write("No features listed")
                
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


                # Report Export
                st.markdown("---")
                st.markdown("### 📤 Export Report")
                if st.button("Generate HTML Report"):
                    report_html = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; padding: 20px; }}
                            h1 {{ color: #2563EB; }}
                            .risk-high {{ color: red; }}
                            .metric {{ padding: 10px; background: #f0f0f0; margin: 10px 0; border-radius: 5px; }}
                        </style>
                    </head>
                    <body>
                        <h1>Veritas Analysis Report: {selected_product}</h1>
                        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        
                        <div class='metric'>
                            <h3>Overall Risk Score: {product_gap['overall_risk_score']:.2f}</h3>
                            <h3>Risk Level: <span class='risk-{product_gap['risk_level'].lower()}'>{product_gap['risk_level'].upper()}</span></h3>
                        </div>
                        
                        <h2>Promised Returns</h2>
                        <p>{product_promise.get('promised_returns', 'N/A')}</p>
                        
                        <h2>Identified Mismatches</h2>
                        <ul>
                    """
                    try:
                        mismatches = eval(product_gap.get('mismatches', '[]'))
                        for m in mismatches:
                            report_html += f"<li><strong>{m.get('promise_aspect', 'Aspect')}:</strong> {m.get('complaint_topic', 'Issue')}</li>"
                    except:
                        report_html += "<li>No mismatches detailed.</li>"
                    
                    report_html += """
                        </ul>
                        <h2>Recommendations</h2>
                        <ul>
                    """
                    try:
                        recs = eval(product_gap.get('recommendations', '[]'))
                        for r in recs:
                            report_html += f"<li>{r}</li>"
                    except:
                        pass
                        
                    report_html += """
                        </ul>
                        <br>
                        <small>Veritas Finance Mis-selling Detection System</small>
                    </body>
                    </html>
                    """
                    
                    # Create download button
                    b64 = base64.b64encode(report_html.encode()).decode()
                    href = f'<a href="data:file/html;base64,{b64}" download="{selected_product}_report.html" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">📥 Download HTML Report</a>'
                    st.markdown(href, unsafe_allow_html=True)


    def show_live_analysis(self):
        """Show interactive live analysis lab"""
        st.subheader("🧪 Live Analysis Lab")
        st.markdown("Test the AI engines with real-time inputs.")
        
        tab1, tab2 = st.tabs(["📄 Promise Extraction (Expectation)", "💬 Sentiment Analysis (Reality)"])
        
        with tab1:
            st.markdown("### Extract Promises from Marketing Material")
            
            input_method = st.radio("Input Method", ["Paste Text", "Upload PDF"])
            
            text_to_analyze = ""
            
            if input_method == "Paste Text":
                text_to_analyze = st.text_area("Paste marketing brochure text here:", height=200,
                    placeholder="Example: The Delta Super Fund guarantees 15% returns per annum. Zero risk involved...")
            else:
                uploaded_file = st.file_uploader("Upload Product Brochure", type=['pdf'])
                if uploaded_file is not None:
                    try:
                        import PyPDF2
                        reader = PyPDF2.PdfReader(uploaded_file)
                        for page in reader.pages:
                            text_to_analyze += page.extract_text() + "\n"
                        st.success(f"✅ Extracted {len(text_to_analyze)} characters from PDF")
                        with st.expander("View Extracted Text"):
                            st.text(text_to_analyze[:1000] + "...")
                    except Exception as e:
                        st.error(f"Error reading PDF: {e}")
            
            if st.button("🚀 Extract Promises", type="primary"):
                if text_to_analyze:
                    with st.spinner("Analyzing text with NLP Engine..."):
                        # Import backend on demand
                        try:
                            import sys
                            from pathlib import Path
                            sys.path.append(str(Path(__file__).parent))
                            from backend.expectation_engine.promise_extractor import PromiseExtractor, FinancialPromise
                            
                            extractor = PromiseExtractor()
                            # Create a dummy product info dict
                            info = {'product_name': 'Live Analysis Product', 'issuer': 'Unknown'}
                            promise = extractor.extract_from_text(text_to_analyze, info)
                            
                            # Display results
                            col1, col2 = st.columns(2)
                            with col1:
                                st.success("✅ Extraction Complete!")
                                st.metric("Promised Returns", promise.promised_returns if promise.promised_returns else "Not Found")
                                st.metric("Risk Category", promise.risk_category)
                                st.metric("Lock-in Period", promise.lock_in_period if promise.lock_in_period else "Not Found")
                                
                            with col2:
                                st.markdown("**Key Features Detected:**")
                                for feature in promise.key_features:
                                    st.write(f"• {feature}")
                                    
                                st.markdown("**Warnings/Disclaimers:**")
                                for warning in promise.warnings:
                                    st.write(f"⚠️ {warning}")
                                    
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")
                            st.write(e)
                else:
                    st.warning("Please provide some text to analyze.")
                    
        with tab2:
            st.markdown("### Analyze Customer Sentiment")
            review_text = st.text_area("Paste a customer review:", height=150,
                placeholder="Example: I am very angry! They promised 12% but I only got 4%. Hidden fees everywhere...")
            
            if st.button("🔍 Analyze Sentiment", type="primary"):
                if review_text:
                    with st.spinner("Analyzing sentiment..."):
                        try:
                            from backend.reality_engine.sentiment_analyzer import AdvancedSentimentAnalyzer
                            
                            # Initialize (might take a sec to load model)
                            analyzer = AdvancedSentimentAnalyzer()
                            result = analyzer.analyze_sentiment(review_text)
                            
                            st.markdown("### Analysis Result")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                sentiment_label = result['label']
                                color = "green" if sentiment_label == 'POSITIVE' else "red"
                                st.markdown(f"Sentiment: <h2 style='color:{color}'>{sentiment_label}</h2>", unsafe_allow_html=True)
                                st.progress(result['score'])
                                st.caption(f"Confidence: {result['score']:.2f}")
                                
                            with col2:
                                st.markdown("**Detected Complaints/Keywords:**")
                                # Simple keyword check for demo
                                keywords = analyzer.financial_keywords
                                found = []
                                for category, terms in keywords.items():
                                    for term in terms:
                                        if term in review_text.lower():
                                            found.append(f"{category.replace('_', ' ').title()} ({term})")
                                            break
                                
                                if found:
                                    for f in found:
                                        st.error(f"• {f}")
                                else:
                                    st.info("No specific operational complaints detected.")
                                    
                        except Exception as e:
                            st.error(f"Analysis failed: {e}")
                else:
                    st.warning("Please enter a review to analyze.")
    
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

        # Risk Heatmap
        st.markdown("### 🔥 Risk vs. Dissatisfaction Heatmap")
        if self.gap_df is not None and len(self.gap_df) > 0:
            # Create a combined figure
            fig = go.Figure()
            
            # Add Heatmap background
            fig.add_trace(go.Histogram2dContour(
                x=self.gap_df['overall_risk_score'],
                y=self.gap_df['dissatisfaction_index'],
                colorscale='Hot',
                ncontours=20,
                showscale=False,
                hoverinfo='none',
                opacity=0.3
            ))
            
            # Add Scatter points
            fig.add_trace(go.Scatter(
                x=self.gap_df['overall_risk_score'],
                y=self.gap_df['dissatisfaction_index'],
                mode='markers+text',
                text=self.gap_df['product_name'],
                textposition="top center",
                marker=dict(
                    size=12,
                    color=self.gap_df['overall_risk_score'], # Use raw score for color
                    colorscale='RdYlGn_r', # Red high risk
                    showscale=True,
                    colorbar=dict(title="Risk Score"),
                    line=dict(width=1, color='DarkSlateGrey')
                ),

                hovertemplate="<b>%{text}</b><br>Risk: %{x:.2f}<br>Dissatisfaction: %{y:.1f}%<extra></extra>"
            ))
            
            fig.update_layout(
                title="Risk Correlation Analysis",
                xaxis_title="Overall Risk Score (0-1)",
                yaxis_title="Customer Dissatisfaction Index (%)",
                height=500,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "white" if st.session_state['theme']=='dark' else "black"}
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

        st.markdown("---")
        st.markdown("### 🤖 AI Configuration")
        
        # Check current key status
        current_key = st.session_state.get('gemini_api_key', '')
        # Mask key for display
        display_key = current_key[:4] + "*" * (len(current_key)-4) if current_key and len(current_key) > 4 else ""
        
        new_key = st.text_input("Google Gemini API Key", value=display_key, type="password", help="Get your key from Google AI Studio")
        
        if st.button("Update API Key"):
            if new_key and new_key != display_key:
                st.session_state['gemini_api_key'] = new_key
                if st.session_state.ai_assistant:
                    st.session_state.ai_assistant.set_api_key(new_key)
                st.success("✅ API Key updated! The AI Assistant is now powered by Gemini.")
            elif not new_key:
                st.warning("Please enter a valid API Key")


        st.markdown("---")
        st.markdown("### 👥 User Management (Admin)")
        
        if self.auth:
             # Get users
             users = self.auth.get_users()
             
             if not users:
                 st.info("No users found.")
             else:
                 # Header
                 c1, c2, c3 = st.columns([3, 2, 1])
                 c1.markdown("**Username**")
                 c2.markdown("**Auth Methods**")
                 c3.markdown("**Action**")
                 
                 for user, data in users.items():
                     c1, c2, c3 = st.columns([3, 2, 1])
                     with c1:
                         st.write(f"👤 {user}")
                     with c2:
                         methods = ["🔑 Password"]
                         if data.get('has_face_id'):
                             methods.append("📸 Face ID")
                         st.caption(", ".join(methods))
                     with c3:
                         # Prevent deleting self if possible, but skipping complex logic for now
                         if st.button("🗑️", key=f"del_{user}"):
                             if self.auth.delete_user(user):
                                 st.success(f"Deleted {user}")
                                 st.rerun()
                             else:
                                 st.error("Failed to delete")
        else:
            st.error("Auth Manager not initialized")


# Run the dashboard
if __name__ == "__main__":
    dashboard = VeritasDashboard()
    dashboard.run()
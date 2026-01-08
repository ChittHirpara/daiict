import pandas as pd
import json
import re
import random
from typing import Dict, List, Optional
import os

try:
    from backend.gemini_client import GeminiClient
except ImportError:
    # Fallback if run from different context
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from backend.gemini_client import GeminiClient

class VeritasAssistant:
    """
    Veritas AI Assistant - An intelligent chatbot for the Mis-selling Detection System.
    Powered by Google Gemini Pro.
    """
    
    def __init__(self):
        self.load_data()
        self.gemini = GeminiClient()
        self.context = {}
        
    def load_data(self):
        """Load the latest analyzed data"""
        try:
            self.gap_df = pd.read_csv("data/processed/gap_analysis.csv") if os.path.exists("data/processed/gap_analysis.csv") else pd.DataFrame()
            self.promises_df = pd.read_csv("data/processed/extracted_promises.csv") if os.path.exists("data/processed/extracted_promises.csv") else pd.DataFrame()
        except Exception as e:
            print(f"Error loading AI data: {e}")
            self.gap_df = pd.DataFrame()
            self.promises_df = pd.DataFrame()

    def set_api_key(self, key: str):
        """Update the Gemini API Key"""
        self.gemini.update_api_key(key)

    def get_response(self, user_query: str) -> str:
        """
        Process user query and return an AI-generated response.
        """
        # Reload data to ensure freshness
        self.load_data()
        
        # If Gemini is ready, use it
        if self.gemini.is_configured():
            return self._get_gemini_response(user_query)
        
        # Fallback to legacy regex system
        return self._get_legacy_response(user_query)

    def _get_gemini_response(self, query: str) -> str:
        """Use Gemini to generate a response with data context"""
        
        # Construct Data Context
        context_str = "You are Veritas AI, a financial regulatory assistant. You analyze financial products for mis-selling risks.\n"
        context_str += "Here is the summary of the latest analysis:\n\n"
        
        if not self.gap_df.empty:
            stats = {
                "total_products": len(self.gap_df),
                "high_risk_count": len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])]),
                "avg_dissatisfaction": self.gap_df['dissatisfaction_index'].mean() if 'dissatisfaction_index' in self.gap_df.columns else 0
            }
            context_str += f"Statistics: {stats}\n\n"
            
            # Add top 5 risky products details
            risky_products = self.gap_df.sort_values('overall_risk_score', ascending=False).head(5)
            context_str += "Top Risky Products Details:\n"
            for _, row in risky_products.iterrows():
                context_str += f"- Name: {row.get('product_name')}\n"
                context_str += f"  Risk Level: {row.get('risk_level')}\n"
                context_str += f"  Score: {row.get('overall_risk_score')}\n"
                context_str += f"  Issues: {row.get('mismatches')}\n"
        else:
            context_str += "No analysis data available yet. Ask the user to run the pipeline.\n"
            
        context_str += "\nAnswer the user's question based on this data. Be professional, concise, and helpful."
        
        return self.gemini.generate_response(query, context_str)

    def _get_legacy_response(self, query: str) -> str:
        """Legacy Pattern Matching (Fallback)"""
        query = query.lower()
        
        # 1. GREETINGS
        if re.search(r'\b(hi|hello|hey|greetings)\b', query):
            return "Hello! I am the Veritas AI Assistant (Legacy Mode). I can help you analyze financial products. add a Gemini API Key for smarter answers!"

        # 2. OVERALL STATUS / SUMMARY
        if re.search(r'\b(summary|status|overview|how many)\b', query):
            return self._get_overall_summary()

        # 3. HIGH RISK QUERIES
        if re.search(r'\b(risk|risky|danger|alert|violation)\b', query):
            return self._get_risk_analysis()

        # 4. EXPLAIN PRODUCT (Specific Query)
        product_match = self._extract_product_name(query)
        if product_match:
            return self._explain_product(product_match)

        # FALLBACK
        return "I'm in Legacy Mode. Please add a Gemini API Key in the sidebar for full AI capabilities. You can ask me about 'high risk products' or 'summary'."

    def _get_overall_summary(self) -> str:
        if self.gap_df.empty:
            return "I don't have enough data yet. Please run the analysis pipeline first."
        
        total = len(self.gap_df)
        high_risk = len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])])
        avg_dissatisfaction = self.gap_df['dissatisfaction_index'].mean() if 'dissatisfaction_index' in self.gap_df.columns else 0
        
        return f"""**Analysis Summary**:
- I have monitored **{total} products** in total.
- **{high_risk} products** have been flagged as **High/Critical Risk**.
- The average customer dissatisfaction rate is **{avg_dissatisfaction:.1f}%**.

Would you like to see the high-risk products? Type 'show high risk'."""

    def _get_risk_analysis(self) -> str:
        if self.gap_df.empty:
            return "No risk data available yet."
            
        high_risk_df = self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])]
        
        if high_risk_df.empty:
            return "Good news! I haven't detected any critical mis-selling cases in the current batch of data."
            
        response = "**⚠️ Critical Risk Alerts Detected:**\n\n"
        for _, row in high_risk_df.iterrows():
            name = row.get('product_name', 'Unknown')
            score = row.get('overall_risk_score', 0)
            response += f"- **{name}** (Risk Score: {score:.2f}/1.0)\n"
            
        response += "\nI recommend issuing show-cause notices for these products immediately."
        return response

    def _extract_product_name(self, query: str) -> Optional[str]:
        """Try to fuzzy match a product name from the query"""
        if self.gap_df.empty: return None
        
        products = self.gap_df['product_name'].unique()
        for product in products:
            # Simple substring check
            if product.lower() in query:
                return product
            # Check parts of name
            parts = product.split()
            if len(parts) > 1 and f"{parts[0]} {parts[1]}".lower() in query:
                return product
        return None

    def _explain_product(self, product_name: str) -> str:
        row = self.gap_df[self.gap_df['product_name'] == product_name].iloc[0]
        
        risk_level = row.get('risk_level', 'Unknown').upper()
        sentiment = row.get('sentiment_score', 0.5)
        mismatches_text = ""
        
        try:
            mismatches = json.loads(row.get('mismatches', '[]'))
            if mismatches:
                mismatches_text = "\n**Key Violations:**\n"
                for m in mismatches[:3]:
                    mismatches_text += f"- {m.get('promise_aspect')}: {m.get('complaint_topic')}\n"
        except:
            pass
            
        return f"""**Analysis for {product_name}**:

**Risk Level**: {risk_level}
**Customer Sentiment**: {sentiment:.2f} (0=Negative, 1=Positive)

{mismatches_text}
**My Recommendation**: {json.loads(row.get('recommendations', '["Review required"]'))[0]}
"""

if __name__ == "__main__":
    # Test
    bot = VeritasAssistant()
    print(bot.get_response("hello"))
    print(bot.get_response("show me high risk products"))

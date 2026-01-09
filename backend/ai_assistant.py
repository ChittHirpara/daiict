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
        """Use Gemini to generate a response with data context and navigation intent"""
        
        # Construct Data Context
        context_str = "You are Veritas AI, a smart financial regulatory assistant for the Mis-selling Detection System.\n"
        context_str += "You have control over the dashboard navigation. You MUST return your response in a strict JSON format.\n"
        context_str += "Structure: {\"text\": \"Your natural language response here\", \"navigate_to\": \"page_id_or_null\"}\n\n"
        
        context_str += "Available Page IDs for 'navigate_to':\n"
        context_str += "- 'dashboard' (Overview/Home)\n"
        context_str += "- 'products' (Products Monitor/List)\n"
        context_str += "- 'expectation' (Expectation Engine/Upload)\n"
        context_str += "- 'reality' (Reality Engine/Sentiment)\n"
        context_str += "- 'risks' (Risk Flags)\n"
        context_str += "- 'reports' (Reports & Evidence)\n"
        context_str += "- 'settings' (Settings)\n"
        context_str += "- null (If no navigation is needed)\n\n"
        
        context_str += "System Context:\n"
        
        if not self.gap_df.empty:
            stats = {
                "total_products": len(self.gap_df),
                "high_risk_count": len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])]),
                "avg_dissatisfaction": self.gap_df['dissatisfaction_index'].mean() if 'dissatisfaction_index' in self.gap_df.columns else 0
            }
            context_str += f"Current Statistics: {stats}\n\n"
            
            # Add top 5 risky products details
            risky_products = self.gap_df.sort_values('overall_risk_score', ascending=False).head(5)
            context_str += "Top Risky Products Details:\n"
            for _, row in risky_products.iterrows():
                context_str += f"- Name: {row.get('product_name')}\n"
                context_str += f"  Risk Level: {row.get('risk_level')}\n"
                context_str += f"  Score: {row.get('overall_risk_score')}\n"
        else:
            context_str += "No analysis data available yet. Ask the user to run the pipeline.\n"
            
        context_str += "\nInstructions:\n"
        context_str += "1. If the user asks to go to a page, navigate there.\n"
        context_str += "2. If the user asks about data, answer based on the context.\n"
        context_str += "3. Keep answers concise (< 50 words).\n"
        context_str += "4. ALWAYS return valid JSON."

        return self.gemini.generate_response(query, context_str)

    def _get_legacy_response(self, query: str) -> str:
        """Legacy Pattern Matching (Fallback) - Returns JSON format for consistency"""
        query = query.lower()
        response_text = ""
        navigate_to = None
        
        # 1. NAVIGATION
        if "dashboard" in query or "home" in query:
             response_text = "Navigating to Dashboard..."
             navigate_to = "dashboard"
        elif "product" in query and "list" in query:
             response_text = "Opening Products Monitor..."
             navigate_to = "products"
        elif "expectation" in query or "upload" in query:
             response_text = "Opening Expectation Engine..."
             navigate_to = "expectation"
        elif "reality" in query or "sentiment" in query:
             response_text = "Opening Reality Engine..."
             navigate_to = "reality"
        elif "risk" in query and "page" in query:
             response_text = "Opening Risk Flags..."
             navigate_to = "risks"
        
        # 2. GREETINGS
        elif re.search(r'\b(hi|hello|hey|greetings)\b', query):
            response_text = "Hello! I am Veritas AI. I can help you analyze data or navigate the app. Try 'Go to risks' or 'Show summary'."
            
        # 3. OVERALL STATUS
        elif re.search(r'\b(summary|status|overview|how many)\b', query):
            response_text = self._get_overall_summary_text()

        # 4. HIGH RISK QUERIES
        elif re.search(r'\b(risk|risky|danger|alert|violation)\b', query):
            response_text = self._get_risk_analysis_text()

        # FALLBACK
        else:
            response_text = "I'm in Legacy Mode. Please add a Gemini API Key for full AI capabilities."

        return json.dumps({"text": response_text, "navigate_to": navigate_to})

    def _get_overall_summary_text(self) -> str:
        if self.gap_df.empty:
            return "No data analyzed yet."
        
        total = len(self.gap_df)
        high_risk = len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])])
        return f"Monitored: {total} products. High Risk: {high_risk}."

    def _get_risk_analysis_text(self) -> str:
        if self.gap_df.empty: return "No data."
        high_risk_df = self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])]
        if high_risk_df.empty: return "No high risk products detected."
        
        names = ", ".join(high_risk_df['product_name'].head(3).tolist())
        return f"Accessing Risk Data. Found critical risks: {names}..."

    def _extract_product_name(self, query: str) -> Optional[str]:
        """Try to fuzzy match a product name from the query"""
        if self.gap_df.empty: return None
        
        products = self.gap_df['product_name'].unique()
        for product in products:
            if product.lower() in query:
                return product
        return None

if __name__ == "__main__":
    # Test
    bot = VeritasAssistant()
    print(bot.get_response("hello"))
    print(bot.get_response("go to dashboard"))


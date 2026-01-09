import pandas as pd
import json
import re
import random
from typing import Dict, List, Optional
import os


# GeminiClient removed


class VeritasAssistant:
    """
    Veritas AI Assistant - A rule-based chatbot for the Mis-selling Detection System.
    """
    
    def __init__(self):
        self.load_data()
        
    def load_data(self):
        """Load the latest analyzed data"""
        try:
            self.gap_df = pd.read_csv("data/processed/gap_analysis.csv") if os.path.exists("data/processed/gap_analysis.csv") else pd.DataFrame()
            self.promises_df = pd.read_csv("data/processed/extracted_promises.csv") if os.path.exists("data/processed/extracted_promises.csv") else pd.DataFrame()
        except Exception as e:
            print(f"Error loading AI data: {e}")
            self.gap_df = pd.DataFrame()
            self.promises_df = pd.DataFrame()

    def get_response(self, user_query: str) -> str:
        """
        Process user query and return a response.
        """
        # Reload data to ensure freshness
        self.load_data()
        
        return self._get_simple_response(user_query)

    def _get_simple_response(self, query: str) -> str:
        """Simple Pattern Matching - Returns JSON format"""
        query = query.lower()
        response_text = ""
        navigate_to = None
        
        # 1. NAVIGATION
        if "dashboard" in query or "home" in query:
             response_text = "Navigating to Dashboard overview."
             navigate_to = "dashboard"
        elif "product" in query:
             response_text = "Opening Products Monitor..."
             navigate_to = "products"
        elif "expectation" in query or "upload" in query:
             response_text = "Opening Expectation Engine..."
             navigate_to = "expectation"
        elif "reality" in query or "sentiment" in query:
             response_text = "Opening Reality Engine..."
             navigate_to = "reality"
        elif "risk" in query:
             response_text = "Opening Risk Flags..."
             navigate_to = "risks"
        elif "report" in query:
             response_text = "Opening Reports section..."
             navigate_to = "reports"
        elif "setting" in query:
             response_text = "Opening Settings..."
             navigate_to = "settings"
        
        # 2. GREETINGS & BASICS
        elif re.search(r'\b(hi|hello|hey|greetings)\b', query):
            response_text = "Hello! I am Veritas AI. I can help you navigate the system or check basic stats. Try asking 'Show summary' or 'Go to risks'."
        
        elif "thank" in query:
            response_text = "You're welcome!"
        elif "who are you" in query:
            response_text = "I am a simple virtual assistant for the Veritas Finance platform."

        # 3. OVERALL STATUS
        elif re.search(r'\b(summary|status|overview|how many)\b', query):
            response_text = self._get_overall_summary_text()

        # 4. DATA QUERIES
        elif re.search(r'\b(risk|risky|danger|alert|violation)\b', query):
            response_text = self._get_risk_analysis_text()

        # FALLBACK
        else:
            response_text = f"I'm not sure about that. I can help you navigate (e.g., 'Go to dashboard') or show summaries (e.g., 'Show risks'). You said: '{query}'"

        return json.dumps({"text": response_text, "navigate_to": navigate_to})

    def _get_overall_summary_text(self) -> str:
        if self.gap_df.empty:
            return "No data analyzed yet."
        
        total = len(self.gap_df)
        high_risk = len(self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])])
        return f"System is monitoring {total} products. Currently {high_risk} are flagged as High Risk."

    def _get_risk_analysis_text(self) -> str:
        if self.gap_df.empty: return "No data available."
        high_risk_df = self.gap_df[self.gap_df['risk_level'].isin(['high', 'critical'])]
        if high_risk_df.empty: return "No high risk products detected."
        
        count = len(high_risk_df)
        names = ", ".join(high_risk_df['product_name'].head(3).tolist())
        return f"Found {count} critical risks. Top offenders: {names}."

if __name__ == "__main__":
    # Test
    bot = VeritasAssistant()
    print(bot.get_response("hello"))
    print(bot.get_response("go to dashboard"))


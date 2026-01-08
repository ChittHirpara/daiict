
import google.generativeai as genai
import os
from typing import Optional

class GeminiClient:
    """
    Client for interacting with Google's Gemini Pro Model.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.chat_session = None
        
        if self.api_key:
            self._configure_genai()
    
    def _configure_genai(self):
        try:
            genai.configure(api_key=self.api_key)
            # Try using the newer Flash model which is faster and usually standard
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.chat_session = self.model.start_chat(history=[])
            print("Message from GeminiClient: Successfully configured Gemini 1.5 Flash.")
        except Exception as e:
            print(f"Error configuring Gemini: {e}")
            try:
                # Fallback to listing models to help debug
                print("Available models:")
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        print(f"  - {m.name}")
            except:
                pass
            self.model = None

    def update_api_key(self, api_key: str):
        """Update the API key at runtime"""
        self.api_key = api_key
        self._configure_genai()

    def generate_response(self, prompt: str, system_context: str = "") -> str:
        """
        Generate a response from Gemini given a user prompt and system context.
        """
        if not self.model:
            return "Gemini API Key is missing or invalid. Please provide a key in the settings sidebar."
            
        try:
            # Combine context and prompt. 
            # Note: Gemini Pro doesn't have a strict 'system' role yet in all versions, 
            # so we prepend the context to the message or history.
            full_prompt = f"{system_context}\n\nUser Query: {prompt}"
            
            response = self.chat_session.send_message(full_prompt)
            return response.text
        except Exception as e:
            return f"Error getting response from Gemini: {str(e)}"

    def is_configured(self) -> bool:
        return self.model is not None

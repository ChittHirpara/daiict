import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from backend.ai_assistant import VeritasAssistant

def test_legacy_responses():
    bot = VeritasAssistant()
    
    test_cases = [
        ("hi", None),
        ("go to dashboard", "dashboard"),
        ("show me the products list", "products"),
        ("risk page please", "risks"),
        ("random query", None)
    ]
    
    print("🧪 Testing Legacy/Fallback Mode JSON Structure...\n")
    
    all_passed = True
    
    for query, expected_nav in test_cases:
        response = bot.get_response(query)
        print(f"Query: '{query}'")
        try:
            # Handle markdown wrapping if present (logic copied from dashboard.py)
            clean_response = response
            if "```json" in response:
                clean_response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                clean_response = response.split("```")[1].split("```")[0]
                
            data = json.loads(clean_response)
            
            nav = data.get("navigate_to")
            text = data.get("text")
            
            print(f"  ✅ Parsed JSON: text='{text[:30]}...', nav='{nav}'")
            
            if expected_nav and nav != expected_nav:
                print(f"  ❌ Expected nav '{expected_nav}', got '{nav}'")
                all_passed = False
            elif expected_nav is None and nav is not None:
                 print(f"  ❌ Expected nav None, got '{nav}'")
                 all_passed = False
                 
        except json.JSONDecodeError:
            print(f"  ❌ Failed to parse JSON: {response}")
            all_passed = False
        print("-" * 30)

    if all_passed:
        print("\n✅ All legacy tests passed.")
    else:
        print("\n❌ Some tests failed.")

if __name__ == "__main__":
    test_legacy_responses()

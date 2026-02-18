"""
Simple Gemini API test with detailed error output
"""

import os
import traceback
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key: {api_key[:20]}...{api_key[-4:]}")
    
    genai.configure(api_key=api_key)
    
    # Try different model names
    model_names = [
        "gemini-2.0-flash-exp",
        "models/gemini-2.0-flash-exp",
        "gemini-1.5-pro",
        "models/gemini-1.5-pro",
        "gemini-pro",
        "models/gemini-pro"
    ]
    
    for model_name in model_names:
        try:
            print(f"\nTrying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello!'")
            print(f"✓ SUCCESS with {model_name}")
            print(f"  Response: {response.text}")
            break
        except Exception as e:
            print(f"✗ Failed: {str(e)[:100]}")
            
except Exception as e:
    print(f"\nFull error:")
    traceback.print_exc()

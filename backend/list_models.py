"""
List available Gemini models
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

print("Available Gemini models that support generateContent:\n")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  ✓ {model.name}")
        print(f"    Description: {model.display_name}")
        print()

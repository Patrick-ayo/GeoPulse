"""
List available models with new google.genai package
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

print("Available Gemini models:\n")
for model in client.models.list():
    print(f"  ✓ {model.name}")
    if hasattr(model, 'display_name'):
        print(f"    Display: {model.display_name}")
    print()

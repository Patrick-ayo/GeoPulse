"""
Test new google.genai API with models/gemini-2.5-flash
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    from google.genai import types
    
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key: {api_key[:20]}...{api_key[-4:]}")
    
    # Initialize client
    client = genai.Client(api_key=api_key)
    
    # Try to generate content
    print("\nTrying model: models/gemini-2.5-flash")
    response = client.models.generate_content(
        model='models/gemini-2.5-flash',
        contents='Say "Hello, GeoPulse!" in one sentence.'
    )
    
    print(f"✓ SUCCESS!")
    print(f"  Response: {response.text}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

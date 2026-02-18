"""
Diagnostic script to test Gemini API connection
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("="*80)
print("GEMINI API DIAGNOSTIC")
print("="*80)

# Check if API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("\n✗ GOOGLE_API_KEY not found in environment")
    print("  Make sure .env file exists and contains GOOGLE_API_KEY")
    exit(1)

print(f"\n✓ GOOGLE_API_KEY found: {api_key[:20]}...{api_key[-4:]}")

# Try to import google.generativeai
try:
    import google.generativeai as genai
    print(f"✓ google-generativeai imported successfully (version {genai.__version__})")
except ImportError as e:
    print(f"\n✗ Failed to import google-generativeai: {e}")
    print("  Run: pip install google-generativeai")
    exit(1)

# Try to configure the API
try:
    genai.configure(api_key=api_key)
    print("✓ API configured successfully")
except Exception as e:
    print(f"\n✗ Failed to configure API: {e}")
    exit(1)

# Try to create a model
try:
    model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
    print("✓ Model created successfully")
except Exception as e:
    print(f"\n✗ Failed to create model: {e}")
    exit(1)

# Try to generate content
print("\n" + "="*80)
print("TESTING API CALL")
print("="*80)

try:
    response = model.generate_content("Say 'Hello, GeoPulse!' in one sentence.")
    print(f"\n✓ API call successful!")
    print(f"  Response: {response.text}")
    print("\n" + "="*80)
    print("✓ ALL TESTS PASSED - Gemini API is working correctly!")
    print("="*80)
except Exception as e:
    print(f"\n✗ API call failed: {type(e).__name__}")
    print(f"  Error: {str(e)}")
    print("\n" + "="*80)
    print("TROUBLESHOOTING")
    print("="*80)
    print("\n1. Verify your API key is correct:")
    print("   - Go to https://makersuite.google.com/app/apikey")
    print("   - Check if the key is still valid")
    print("   - Create a new key if needed")
    print("\n2. Check if the API key has the correct permissions")
    print("\n3. Ensure you haven't exceeded the free tier limits")
    print("   - Free tier: 60 requests per minute")
    exit(1)

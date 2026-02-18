# Troubleshooting Guide: API Key Issues

## Problem
The test_real_llm.py script is failing with all 8 tests showing errors. The diagnostic shows the Gemini API key is being loaded but API calls are failing.

## Most Likely Causes

### 1. Invalid or Expired API Key
The API key in your `.env` file might be:
- Incorrect (typo when copying)
- Expired or revoked
- Not activated properly

**Solution:**
1. Go to https://makersuite.google.com/app/apikey
2. Check if your existing key is still valid
3. If not, create a NEW API key
4. Copy the ENTIRE key carefully (no extra spaces)
5. Update `.env` file:
   ```
   GOOGLE_API_KEY=your-new-key-here
   ```

### 2. API Key Restrictions
Your API key might have restrictions that prevent it from being used.

**Solution:**
1. Go to https://makersuite.google.com/app/apikey
2. Click on your API key
3. Check "API restrictions" - it should allow "Generative Language API"
4. If restricted, create a new unrestricted key for testing

### 3. Billing or Quota Issues
Even though Gemini has a free tier, there might be quota issues.

**Solution:**
1. Check https://makersuite.google.com/app/apikey for usage limits
2. Ensure you haven't exceeded 60 requests/minute
3. Wait a few minutes and try again

### 4. Network/Firewall Issues
Your network might be blocking Google AI API calls.

**Solution:**
1. Try from a different network
2. Check if your firewall is blocking the requests
3. Try using a VPN if behind a corporate firewall

## Quick Test

Run this diagnostic command:
```bash
python diagnose_api.py
```

This will show you exactly where the problem is.

## Alternative: Use OpenAI Instead

If Gemini continues to fail, you can use OpenAI:

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Add billing information (required for OpenAI)
3. Update `.env`:
   ```
   # Comment out Gemini
   # GOOGLE_API_KEY=...
   
   # Add OpenAI
   OPENAI_API_KEY=your-openai-key-here
   ```
4. Run the test again

**Note:** OpenAI is paid (~$0.002 per analysis, so ~$0.016 for all 8 tests)

## Verify .env File Format

Your `.env` file should look like this (no extra spaces):

```bash
GOOGLE_API_KEY=AIzaSyC7pxRXndPixX7Z8GajwwbjL_Nxt3wu-7s
```

NOT like this:
```bash
GOOGLE_API_KEY = AIzaSyC7pxRXndPixX7Z8GajwwbjL_Nxt3wu-7s  # Extra spaces
 GOOGLE_API_KEY=AIzaSyC7pxRXndPixX7Z8GajwwbjL_Nxt3wu-7s  # Leading space
```

## Next Steps

1. **Get a fresh API key** from Google AI Studio
2. **Update .env** with the new key (no spaces)
3. **Run diagnostic**: `python diagnose_api.py`
4. **If diagnostic passes**, run: `python test_real_llm.py`

## Still Having Issues?

The API key shown in your .env file appears to be properly formatted. The issue is likely:
- The key itself is invalid/expired
- Network/firewall blocking the API
- Google AI Studio account not properly set up

**Recommended Action:** Create a completely new API key from scratch at https://makersuite.google.com/app/apikey

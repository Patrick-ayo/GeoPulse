# Real-time LLM Testing Guide

This guide explains how to test the GeoPulse Intelligence Pipeline with actual LLM API keys to validate prompt effectiveness.

## Prerequisites

You need an API key from one of these providers:
- **Google Gemini** (Recommended) - Free tier available
- **OpenAI** - Paid service

## Step 1: Get an API Key

### Option A: Google Gemini (Recommended)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

**Pricing:** Free tier includes 60 requests per minute

### Option B: OpenAI

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the generated API key

**Pricing:** Pay-as-you-go (approximately $0.002-0.01 per analysis)

## Step 2: Set Environment Variable

### Windows (PowerShell)
```powershell
# For Gemini
$env:GOOGLE_API_KEY="your-api-key-here"

# For OpenAI
$env:OPENAI_API_KEY="your-api-key-here"
```

### Windows (Command Prompt)
```cmd
# For Gemini
set GOOGLE_API_KEY=your-api-key-here

# For OpenAI
set OPENAI_API_KEY=your-api-key-here
```

### Linux/Mac
```bash
# For Gemini
export GOOGLE_API_KEY="your-api-key-here"

# For OpenAI
export OPENAI_API_KEY="your-api-key-here"
```

### Permanent Setup (Recommended)

Create a `.env` file in the `backend/` directory:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your-actual-api-key-here
```

Then install python-dotenv (already in requirements.txt):
```bash
pip install python-dotenv
```

## Step 3: Run the Test Script

```bash
cd backend
python test_real_llm.py
```

## What the Test Does

The script will:

1. **Check API Keys** - Verify which LLM provider is available
2. **Test 8 Headlines** - Covering different market scenarios:
   - Energy/Commodities (OPEC oil cuts)
   - Monetary Policy (Fed rate hikes)
   - Tech/Earnings (Apple sales)
   - Regulation (EU AI rules)
   - Economic Data (China GDP)
   - Corporate/Safety (Tesla recalls)
   - Safe Haven (Gold prices)
   - Tech/M&A (Microsoft-OpenAI)

3. **Validate Outputs** - Ensure all responses match the Event Pydantic model

4. **Analyze Quality** - Generate statistics on:
   - Severity distribution
   - Market pressure types
   - Prediction confidence
   - Logic chain completeness

5. **Save Results** - Export to `test_results/TIMESTAMP_test_results.json`

## Expected Output

```
================================================================================
REAL-TIME LLM TESTING
================================================================================

API KEY STATUS
================================================================================

✓ GOOGLE_API_KEY: Set
✗ OPENAI_API_KEY: Not set

🤖 Active LLM Client: GeminiClient

📋 Testing 8 headlines...

[1/8]
────────────────────────────────────────────────────────────────────────────────
📰 Headline: OPEC announces surprise oil production cut of 2 million barrels per day
📍 Source: Bloomberg
🏷️  Category: Energy/Commodities

✓ Analysis successful
  Event ID: evt_20260215_201500
  Severity: HIGH
  Sentiment: NEGATIVE
  Macro Effect: Supply Shock
  Market Pressure: INFLATIONARY
  Horizon: SHORT_TERM

📊 Logic Chain:
  EVENT    → OPEC production cut announcement
  MACRO    → Supply Shock
  SECTOR   → Energy
  ASSET    → XOM

💼 Affected Assets (2):
  XOM    | BULLISH  | Confidence: 0.85
         Oil producers benefit from higher prices
  USO    | BULLISH  | Confidence: 0.80
         Oil ETF tracks crude prices directly

💡 Why: OPEC production cuts reduce supply, driving oil prices higher
🤖 Model: gemini-1.5-flash

[2/8]
...
```

## Interpreting Results

### Success Metrics
- ✅ **100% validation pass rate** - All outputs match Event model
- ✅ **Complete logic chains** - All 4 steps present (Event → Macro → Sector → Asset)
- ✅ **Reasonable confidence** - Average confidence > 0.6
- ✅ **Diverse predictions** - Mix of BULLISH, BEARISH, NEUTRAL

### Quality Indicators
- **Severity matches impact** - Major events = HIGH, minor = LOW
- **Market pressure is logical** - Rate cuts = RISK_ON, oil shock = INFLATIONARY
- **Asset selection is relevant** - Energy news → energy stocks
- **Reasoning is clear** - "Why" field explains the logic

## Troubleshooting

### "No API keys found"
- Ensure you've set the environment variable correctly
- Check spelling: `GOOGLE_API_KEY` not `GOOGLE_API_KEY_`
- Restart your terminal after setting the variable

### "API key invalid"
- Verify the key is correct (no extra spaces)
- Check if the key has been revoked
- Ensure billing is enabled (for OpenAI)

### "Rate limit exceeded"
- Wait a few minutes and try again
- Gemini free tier: 60 requests/minute
- OpenAI: Depends on your tier

### "Validation failed"
- This indicates the LLM output doesn't match the Event model
- Check the error message for missing/invalid fields
- May need to refine prompts in `prompt_builder.py`

## Next Steps

After successful testing:

1. **Analyze the results JSON** - Review prediction quality
2. **Refine prompts** - If predictions are poor, update `prompt_builder.py`
3. **Test with real news** - Use current headlines from news APIs
4. **Integrate with Correlator** - Validate predictions against real market data

## Cost Estimation

### Gemini (Free Tier)
- **Cost:** $0
- **Limit:** 60 requests/minute
- **Sufficient for:** Development and testing

### OpenAI (GPT-4o-mini)
- **Cost:** ~$0.002 per analysis
- **8 test headlines:** ~$0.016
- **1000 analyses/day:** ~$2/day

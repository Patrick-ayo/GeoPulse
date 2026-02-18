# Quick Start: Real-time LLM Testing

## 🚀 Get Started in 3 Steps

### Step 1: Get a Free API Key (2 minutes)

**Option A: Google Gemini (Recommended - Free)**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

**Option B: OpenAI (Paid)**
1. Visit https://platform.openai.com/api-keys
2. Create account and add payment method
3. Click "Create new secret key"
4. Copy the key

### Step 2: Set the API Key

**Windows PowerShell:**
```powershell
$env:GOOGLE_API_KEY="paste-your-key-here"
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="paste-your-key-here"
```

### Step 3: Run the Test

```bash
cd backend
python test_real_llm.py
```

## 📊 What You'll See

The script tests 8 different news scenarios:
- ✅ Energy/Commodities (OPEC cuts)
- ✅ Monetary Policy (Fed rates)
- ✅ Tech Earnings (Apple sales)
- ✅ Regulation (EU AI rules)
- ✅ Economic Data (China GDP)
- ✅ Corporate Safety (Tesla recalls)
- ✅ Safe Haven (Gold prices)
- ✅ Tech M&A (Microsoft-OpenAI)

For each headline, you'll see:
- 📰 The headline and source
- 📊 Logic Chain (Event → Macro → Sector → Asset)
- 💼 Affected assets with predictions and confidence
- 💡 Reasoning for the prediction

## 📈 Results

Results are automatically saved to:
```
backend/test_results/TIMESTAMP_test_results.json
```

## 🔍 What to Look For

**Good Signs:**
- ✅ All validations pass
- ✅ Logic chains are complete (4 steps)
- ✅ Predictions make sense (oil cuts → energy stocks bullish)
- ✅ Confidence scores are reasonable (0.6-0.9)

**Red Flags:**
- ❌ Validation errors
- ❌ Incomplete logic chains
- ❌ Illogical predictions (oil cuts → tech stocks bullish)
- ❌ Very low/high confidence (< 0.3 or > 0.95)

## 💡 Next Steps

After testing:
1. Review the JSON results
2. If predictions are poor, refine prompts in `app/intelligence/prompt_builder.py`
3. Test with real current news headlines
4. Integrate with the Correlator for validation

## 💰 Cost

- **Gemini:** FREE (60 requests/minute)
- **OpenAI:** ~$0.002 per analysis (~$0.016 for all 8 tests)

## ❓ Troubleshooting

**"No API keys found"**
- Make sure you set the environment variable in the same terminal
- Check for typos: `GOOGLE_API_KEY` (not `GOOGLE_API_KEY_`)

**"API key invalid"**
- Verify the key is correct
- For OpenAI, ensure billing is enabled

See `TESTING_GUIDE.md` for detailed troubleshooting.

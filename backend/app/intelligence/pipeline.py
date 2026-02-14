from datetime import datetime
from typing import Optional, Dict, Any, List

def analyze_text(headline: str, source: str, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Analyze news headline and generate mock predictions.
    In production, this would call an LLM (OpenAI/Gemini).
    """
    headline_lower = headline.lower()
    
    # Simple keyword-based mock analysis logic moved from main.py
    if any(word in headline_lower for word in ["oil", "opec", "saudi", "energy"]):
        macro_effect = "Supply Shock"
        market_pressure = "INFLATIONARY"
        severity = "HIGH"
        affected_assets = [
            {
                "ticker": "XOM",
                "name": "Exxon Mobil",
                "asset_class": "Equity",
                "sector": "Energy",
                "prediction": "BULLISH",
                "confidence": 0.85,
                "reason": "Oil price increases benefit energy producers.",
            }
        ]
        logic_chain = [
            {"type": "event", "text": "Oil news"},
            {"type": "macro", "text": "Supply Shock"},
            {"type": "sector", "text": "Energy"},
            {"type": "asset", "text": "XOM"},
        ]
    elif any(word in headline_lower for word in ["fed", "rate", "interest", "monetary"]):
        macro_effect = "Monetary Policy Shift"
        market_pressure = "RISK_ON" if "cut" in headline_lower else "DEFENSIVE"
        severity = "HIGH"
        affected_assets = [
            {
                "ticker": "SPY",
                "name": "S&P 500 ETF",
                "asset_class": "Equity",
                "sector": "Broad Market",
                "prediction": "BULLISH" if "cut" in headline_lower else "BEARISH",
                "confidence": 0.80,
                "reason": "Rate changes affect equity valuations.",
            }
        ]
        logic_chain = [
            {"type": "event", "text": "Fed announcement"},
            {"type": "macro", "text": macro_effect},
            {"type": "sector", "text": "Financials"},
            {"type": "asset", "text": "SPY"},
        ]
    elif any(word in headline_lower for word in ["ai", "regulation", "tech", "microsoft", "google"]):
        macro_effect = "Regulatory Impact"
        market_pressure = "DEFENSIVE"
        severity = "MEDIUM"
        affected_assets = [
            {
                "ticker": "MSFT",
                "name": "Microsoft",
                "asset_class": "Equity",
                "sector": "Technology",
                "prediction": "BEARISH" if "regulation" in headline_lower else "BULLISH",
                "confidence": 0.70,
                "reason": "Tech sector faces regulatory changes.",
            }
        ]
        logic_chain = [
            {"type": "event", "text": "Tech news"},
            {"type": "macro", "text": macro_effect},
            {"type": "sector", "text": "Technology"},
            {"type": "asset", "text": "MSFT"},
        ]
    else:
        macro_effect = "Market Uncertainty"
        market_pressure = "RISK_OFF"
        severity = "LOW"
        affected_assets = [
            {
                "ticker": "GLD",
                "name": "Gold ETF",
                "asset_class": "Commodity",
                "sector": "Precious Metals",
                "prediction": "BULLISH",
                "confidence": 0.55,
                "reason": "Uncertainty drives safe haven demand.",
            }
        ]
        logic_chain = [
            {"type": "event", "text": "General news"},
            {"type": "macro", "text": macro_effect},
            {"type": "sector", "text": "Safe Haven"},
            {"type": "asset", "text": "GLD"},
        ]

    event_id = f"evt_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    return {
        "event_id": event_id,
        "headline": headline,
        "source": source,
        "timestamp": (timestamp or datetime.utcnow()).isoformat() + "Z",
        "severity": severity,
        "event_sentiment": "NEGATIVE" if "cut" not in headline_lower and "positive" not in headline_lower else "POSITIVE",
        "macro_effect": macro_effect,
        "prediction_horizon": "SHORT_TERM",
        "market_pressure": market_pressure,
        "logic_chain": logic_chain,
        "affected_assets": affected_assets,
        "why": f"Analysis based on {macro_effect.lower()} implications.",
        "meta": {
            "llm_model": "demo-gpt",
            "llm_prompt_version": "v1",
            "confidence_components": {
                "llm_score": 0.75,
                "sentiment_strength": 0.6,
                "historical_similarity": 0.5,
            },
            "confidence_formula": "0.4*llm_score+0.3*sentiment_strength+0.3*historical_similarity",
        },
    }

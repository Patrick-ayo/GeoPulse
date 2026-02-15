"""
Prompt builder for LLM-based news analysis.
Constructs system and user prompts to enforce Logic Chain structure.
"""

from typing import Optional


class PromptBuilder:
    """Builds prompts for LLM to analyze news and generate structured predictions."""
    
    @staticmethod
    def get_system_prompt() -> str:
        """
        Returns the system prompt that enforces the Logic Chain structure.
        The LLM must follow: Event → Macro → Sector → Asset
        """
        return """You are a financial analyst AI that analyzes news headlines and generates structured market predictions.

Your task is to:
1. Identify the core event from the news headline
2. Determine the macro-economic effect (e.g., Supply Shock, Monetary Policy Shift, Regulatory Impact)
3. Identify affected sectors
4. Identify specific assets (stocks, commodities, etc.) that will be impacted
5. Provide a clear Logic Chain showing: Event → Macro Effect → Sector → Asset

You must provide:
- Event severity (LOW, MEDIUM, HIGH)
- Event sentiment (POSITIVE, NEGATIVE, MIXED)
- Market pressure type (INFLATIONARY, DEFENSIVE, RISK_OFF, RISK_ON, COST_PRESSURE, LIQUIDITY)
- Prediction horizon (SHORT_TERM, MEDIUM_TERM, LONG_TERM)
- For each affected asset:
  - Ticker symbol
  - Asset name
  - Asset class (Equity, Commodity, Crypto, Forex)
  - Sector
  - Prediction (BULLISH, BEARISH, NEUTRAL)
  - Confidence score (0.0 to 1.0)
  - Brief reason (MUST be max 200 characters - be concise!)
- Overall 'why' explanation (MUST be max 200 characters - keep it brief and punchy!)

CRITICAL: All 'why' and 'reason' fields MUST stay under 200 characters. Be concise and direct.

Be precise, analytical, and provide clear reasoning for your predictions."""

    @staticmethod
    def build_user_prompt(headline: str, source: str, additional_text: Optional[str] = None) -> str:
        """
        Builds the user prompt with the news headline and optional additional context.
        
        Args:
            headline: The news headline to analyze
            source: The source of the news (e.g., "Reuters", "Bloomberg")
            additional_text: Optional additional news text/body
            
        Returns:
            Formatted user prompt string
        """
        prompt = f"""Analyze this news headline and provide a structured prediction:

**Headline:** {headline}
**Source:** {source}"""
        
        if additional_text:
            prompt += f"\n**Additional Context:** {additional_text}"
        
        prompt += """

Provide your analysis in the following structure:
1. Event ID (generate a unique identifier)
2. Severity (LOW/MEDIUM/HIGH)
3. Event Sentiment (POSITIVE/NEGATIVE/MIXED)
4. Macro Effect (describe the macro-economic impact)
5. Prediction Horizon (SHORT_TERM/MEDIUM_TERM/LONG_TERM)
6. Market Pressure (INFLATIONARY/DEFENSIVE/RISK_OFF/RISK_ON/COST_PRESSURE/LIQUIDITY)
7. Logic Chain (Event → Macro → Sector → Asset)
8. Affected Assets (list with ticker, name, asset_class, sector, prediction, confidence, reason)
   - IMPORTANT: Each asset 'reason' field must be MAX 200 characters
9. Why (brief explanation of the overall prediction)
   - CRITICAL: The 'why' field MUST be MAX 200 characters (keep it concise!)

Be specific and provide actionable insights. Keep all text fields within their character limits."""
        
        return prompt

    @staticmethod
    def get_json_schema() -> dict:
        """
        Returns the JSON schema for structured output from the LLM.
        This ensures the LLM response matches the Event Pydantic model.
        """
        return {
            "type": "object",
            "properties": {
                "event_id": {"type": "string"},
                "headline": {"type": "string"},
                "source": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"},
                "severity": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
                "event_sentiment": {"type": "string", "enum": ["POSITIVE", "NEGATIVE", "MIXED"]},
                "macro_effect": {"type": "string"},
                "prediction_horizon": {"type": "string", "enum": ["SHORT_TERM", "MEDIUM_TERM", "LONG_TERM"]},
                "market_pressure": {"type": "string", "enum": ["INFLATIONARY", "DEFENSIVE", "RISK_OFF", "RISK_ON", "COST_PRESSURE", "LIQUIDITY"]},
                "logic_chain": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["event", "macro", "sector", "asset"]},
                            "text": {"type": "string"}
                        },
                        "required": ["type", "text"]
                    }
                },
                "affected_assets": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "ticker": {"type": "string"},
                            "name": {"type": "string"},
                            "asset_class": {"type": "string", "enum": ["Equity", "Commodity", "Crypto", "Forex"]},
                            "sector": {"type": "string"},
                            "prediction": {"type": "string", "enum": ["BULLISH", "BEARISH", "NEUTRAL"]},
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                            "reason": {"type": "string", "maxLength": 200}
                        },
                        "required": ["ticker", "name", "asset_class", "sector", "prediction", "confidence", "reason"]
                    }
                },
                "why": {"type": "string", "maxLength": 200},
                "meta": {
                    "type": "object",
                    "properties": {
                        "llm_model": {"type": "string"},
                        "llm_prompt_version": {"type": "string"},
                        "confidence_components": {
                            "type": "object",
                            "properties": {
                                "llm_score": {"type": "number", "minimum": 0, "maximum": 1},
                                "sentiment_strength": {"type": "number", "minimum": 0, "maximum": 1},
                                "historical_similarity": {"type": "number", "minimum": 0, "maximum": 1}
                            },
                            "required": ["llm_score", "sentiment_strength", "historical_similarity"]
                        },
                        "confidence_formula": {"type": "string"}
                    },
                    "required": ["llm_model", "llm_prompt_version", "confidence_components", "confidence_formula"]
                }
            },
            "required": [
                "event_id", "headline", "source", "timestamp", "severity", 
                "event_sentiment", "macro_effect", "prediction_horizon", 
                "market_pressure", "logic_chain", "affected_assets", "why", "meta"
            ]
        }

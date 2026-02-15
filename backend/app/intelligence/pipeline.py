"""
Intelligence pipeline for news analysis.
Uses LLM to analyze news and generate structured market predictions.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any

from .llm_client import LLMClient, GeminiClient, OpenAIClient, MockLLMClient
from .prompt_builder import PromptBuilder


# Global LLM client instance (initialized on first use)
_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """
    Get or initialize the LLM client.
    
    Priority:
    1. Gemini (if GOOGLE_API_KEY is set)
    2. OpenAI (if OPENAI_API_KEY is set)
    3. MockLLMClient (fallback for testing)
    
    Returns:
        Initialized LLM client
    """
    global _llm_client
    
    if _llm_client is not None:
        return _llm_client
    
    # Try Gemini first
    if os.getenv("GOOGLE_API_KEY"):
        try:
            _llm_client = GeminiClient()
            print("✓ Using Gemini LLM client")
            return _llm_client
        except Exception as e:
            print(f"⚠ Failed to initialize Gemini client: {e}")
    
    # Try OpenAI second
    if os.getenv("OPENAI_API_KEY"):
        try:
            _llm_client = OpenAIClient()
            print("✓ Using OpenAI LLM client")
            return _llm_client
        except Exception as e:
            print(f"⚠ Failed to initialize OpenAI client: {e}")
    
    # Fallback to mock
    print("⚠ No API keys found. Using MockLLMClient for testing.")
    _llm_client = MockLLMClient()
    return _llm_client


def analyze_text(
    headline: str, 
    source: str, 
    timestamp: Optional[datetime] = None,
    additional_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze news headline using LLM and generate structured predictions.
    
    Args:
        headline: News headline to analyze
        source: Source of the news (e.g., "Reuters", "Bloomberg")
        timestamp: Optional timestamp of the news event
        additional_text: Optional additional news text/body
        
    Returns:
        Dictionary matching the Event model structure
    """
    # Get LLM client
    llm_client = get_llm_client()
    
    # Build prompts
    prompt_builder = PromptBuilder()
    system_prompt = prompt_builder.get_system_prompt()
    user_prompt = prompt_builder.build_user_prompt(headline, source, additional_text)
    json_schema = prompt_builder.get_json_schema()
    
    # Generate event analysis
    try:
        result = llm_client.generate_event(system_prompt, user_prompt, json_schema)
        
        # Ensure headline and source are set correctly
        result["headline"] = headline
        result["source"] = source
        
        # Ensure timestamp is set
        if timestamp:
            result["timestamp"] = timestamp.isoformat() + "Z"
        elif "timestamp" not in result:
            result["timestamp"] = datetime.utcnow().isoformat() + "Z"
        
        return result
        
    except Exception as e:
        # Fallback to error response if LLM fails
        print(f"⚠ LLM analysis failed: {e}")
        return {
            "event_id": f"evt_error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "headline": headline,
            "source": source,
            "timestamp": (timestamp or datetime.utcnow()).isoformat() + "Z",
            "severity": "LOW",
            "event_sentiment": "MIXED",
            "macro_effect": "Analysis Error",
            "prediction_horizon": "SHORT_TERM",
            "market_pressure": "RISK_OFF",
            "logic_chain": [
                {"type": "event", "text": "Error in analysis"},
                {"type": "macro", "text": "Unable to determine"},
                {"type": "sector", "text": "N/A"},
                {"type": "asset", "text": "N/A"}
            ],
            "affected_assets": [],
            "why": (f"LLM analysis failed: {str(e)}")[:200],
            "meta": {
                "llm_model": "error",
                "llm_prompt_version": "v1",
                "confidence_components": {
                    "llm_score": 0.0,
                    "sentiment_strength": 0.0,
                    "historical_similarity": 0.0
                },
                "confidence_formula": "0.4*llm_score+0.3*sentiment_strength+0.3*historical_similarity"
            }
        }

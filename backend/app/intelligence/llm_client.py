"""
LLM client for news analysis.
Supports multiple LLM providers (Gemini, OpenAI, etc.)
"""

import os
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate_event(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate event analysis from LLM.
        
        Args:
            system_prompt: System instructions for the LLM
            user_prompt: User query with news headline
            json_schema: Optional JSON schema for structured output
            
        Returns:
            Dictionary matching the Event model structure
        """
        pass


class GeminiClient(LLMClient):
    """Google Gemini LLM client with structured output support (using new google.genai package)."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "models/gemini-2.5-flash"):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
            model_name: Gemini model to use
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. Set it as an environment variable or pass it to the constructor."
            )
        
        try:
            from google import genai
            from google.genai import types
            self.genai = genai
            self.types = types
            
            # Initialize client with API key
            self.client = genai.Client(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "google-genai package not installed. "
                "Install it with: pip install google-genai"
            )
    
    def generate_event(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate event analysis using Gemini.
        
        Args:
            system_prompt: System instructions
            user_prompt: User query with news headline
            json_schema: JSON schema for structured output
            
        Returns:
            Dictionary matching Event model structure
        """
        # Combine system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # Add JSON schema instruction if provided
        if json_schema:
            full_prompt += f"\n\nRespond with valid JSON matching this schema:\n{json.dumps(json_schema, indent=2)}"
        
        try:
            # Retry logic for rate limiting
            max_retries = 3
            retry_delay = 2  # Start with 2 seconds
            
            for attempt in range(max_retries):
                try:
                    # Generate content using new API
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=full_prompt,
                        config=self.types.GenerateContentConfig(
                            temperature=0.7,
                            response_mime_type="application/json" if json_schema else "text/plain"
                        )
                    )
                    break  # Success, exit retry loop
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
                        # Rate limit error
                        if attempt < max_retries - 1:
                            print(f"⚠ Rate limit hit, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})...")
                            time.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                        else:
                            raise RuntimeError(f"Rate limit exceeded after {max_retries} attempts: {e}")
                    else:
                        raise  # Re-raise non-rate-limit errors immediately
            
            # Parse JSON response
            result = json.loads(response.text)
            
            # Truncate 'why' field if it exceeds 200 characters
            if "why" in result and len(result["why"]) > 200:
                result["why"] = result["why"][:197] + "..."
            
            # Truncate asset 'reason' fields if they exceed 200 characters
            if "affected_assets" in result:
                for asset in result["affected_assets"]:
                    if "reason" in asset and len(asset["reason"]) > 200:
                        asset["reason"] = asset["reason"][:197] + "..."
            
            # Ensure timestamp is present
            if "timestamp" not in result:
                result["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            # Add meta information if not present
            if "meta" not in result:
                result["meta"] = {
                    "llm_model": self.model_name,
                    "llm_prompt_version": "v1",
                    "confidence_components": {
                        "llm_score": 0.75,
                        "sentiment_strength": 0.6,
                        "historical_similarity": 0.5
                    },
                    "confidence_formula": "0.4*llm_score+0.3*sentiment_strength+0.3*historical_similarity"
                }
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Error generating event with Gemini: {e}")


class OpenAIClient(LLMClient):
    """OpenAI LLM client (GPT-4, etc.) with structured output support."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4o-mini"):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model_name: OpenAI model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model_name
        
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Set it as an environment variable or pass it to the constructor."
            )
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "openai package not installed. "
                "Install it with: pip install openai"
            )
    
    def generate_event(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate event analysis using OpenAI.
        
        Args:
            system_prompt: System instructions
            user_prompt: User query with news headline
            json_schema: JSON schema for structured output
            
        Returns:
            Dictionary matching Event model structure
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Add JSON schema instruction if provided
        if json_schema:
            messages[1]["content"] += f"\n\nRespond with valid JSON matching this schema:\n{json.dumps(json_schema, indent=2)}"
        
        try:
            # Generate content
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                response_format={"type": "json_object"} if json_schema else {"type": "text"}
            )
            
            # Parse JSON response
            result = json.loads(response.choices[0].message.content)
            
            # Ensure timestamp is present
            if "timestamp" not in result:
                result["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            # Add meta information if not present
            if "meta" not in result:
                result["meta"] = {
                    "llm_model": self.model_name,
                    "llm_prompt_version": "v1",
                    "confidence_components": {
                        "llm_score": 0.75,
                        "sentiment_strength": 0.6,
                        "historical_similarity": 0.5
                    },
                    "confidence_formula": "0.4*llm_score+0.3*sentiment_strength+0.3*historical_similarity"
                }
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Error generating event with OpenAI: {e}")


class MockLLMClient(LLMClient):
    """Mock LLM client for testing without API calls."""
    
    def __init__(self):
        """Initialize mock client."""
        pass
    
    def generate_event(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate mock event analysis.
        
        Returns:
            Mock dictionary matching Event model structure
        """
        return {
            "event_id": f"evt_mock_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "headline": "Mock headline from user prompt",
            "source": "Mock Source",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": "MEDIUM",
            "event_sentiment": "POSITIVE",
            "macro_effect": "Mock Macro Effect",
            "prediction_horizon": "SHORT_TERM",
            "market_pressure": "RISK_ON",
            "logic_chain": [
                {"type": "event", "text": "Mock event"},
                {"type": "macro", "text": "Mock macro effect"},
                {"type": "sector", "text": "Technology"},
                {"type": "asset", "text": "AAPL"}
            ],
            "affected_assets": [
                {
                    "ticker": "AAPL",
                    "name": "Apple Inc.",
                    "asset_class": "Equity",
                    "sector": "Technology",
                    "prediction": "BULLISH",
                    "confidence": 0.75,
                    "reason": "Mock reasoning for prediction"
                }
            ],
            "why": "Mock explanation of the overall prediction",
            "meta": {
                "llm_model": "mock-gpt",
                "llm_prompt_version": "v1",
                "confidence_components": {
                    "llm_score": 0.75,
                    "sentiment_strength": 0.6,
                    "historical_similarity": 0.5
                },
                "confidence_formula": "0.4*llm_score+0.3*sentiment_strength+0.3*historical_similarity"
            }
        }

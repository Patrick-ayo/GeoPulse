"""
Real-time LLM Testing Script
Tests the Intelligence Pipeline with actual API keys (Gemini or OpenAI).
Validates prompt effectiveness and analyzes output quality.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.intelligence.pipeline import analyze_text, get_llm_client
from app.storage.models import Event
from pydantic import ValidationError


# Test headlines covering different market scenarios
TEST_HEADLINES = [
    {
        "headline": "OPEC announces surprise oil production cut of 2 million barrels per day",
        "source": "Bloomberg",
        "category": "Energy/Commodities"
    },
    {
        "headline": "Federal Reserve raises interest rates by 75 basis points, signals more hikes ahead",
        "source": "Reuters",
        "category": "Monetary Policy"
    },
    {
        "headline": "Apple announces record-breaking iPhone sales, stock surges 8%",
        "source": "CNBC",
        "category": "Tech/Earnings"
    },
    {
        "headline": "EU proposes strict AI regulations targeting big tech companies",
        "source": "Financial Times",
        "category": "Regulation"
    },
    {
        "headline": "China's GDP growth slows to 3.2%, missing expectations",
        "source": "Wall Street Journal",
        "category": "Economic Data"
    },
    {
        "headline": "Tesla recalls 2 million vehicles over autopilot safety concerns",
        "source": "Reuters",
        "category": "Corporate/Safety"
    },
    {
        "headline": "Gold prices hit record high as investors seek safe haven amid banking crisis",
        "source": "Bloomberg",
        "category": "Safe Haven/Crisis"
    },
    {
        "headline": "Microsoft announces $10 billion investment in OpenAI",
        "source": "TechCrunch",
        "category": "Tech/M&A"
    }
]


def check_api_keys():
    """Check which API keys are available."""
    print("\n" + "="*80)
    print("API KEY STATUS")
    print("="*80)
    
    has_google = bool(os.getenv("GOOGLE_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    
    print(f"\n{'✓' if has_google else '✗'} GOOGLE_API_KEY: {'Set' if has_google else 'Not set'}")
    print(f"{'✓' if has_openai else '✗'} OPENAI_API_KEY: {'Set' if has_openai else 'Not set'}")
    
    if not has_google and not has_openai:
        print("\n⚠ WARNING: No API keys found!")
        print("\nTo test with real LLMs, set one of the following:")
        print("\n  For Gemini (recommended):")
        print("    export GOOGLE_API_KEY='your-api-key-here'")
        print("\n  For OpenAI:")
        print("    export OPENAI_API_KEY='your-api-key-here'")
        print("\nGet API keys from:")
        print("  - Gemini: https://makersuite.google.com/app/apikey")
        print("  - OpenAI: https://platform.openai.com/api-keys")
        return False
    
    return True


def test_single_headline(headline_data: Dict[str, str], show_details: bool = True) -> Dict[str, Any]:
    """Test analysis of a single headline."""
    headline = headline_data["headline"]
    source = headline_data["source"]
    category = headline_data["category"]
    
    if show_details:
        print(f"\n{'─'*80}")
        print(f"📰 Headline: {headline}")
        print(f"📍 Source: {source}")
        print(f"🏷️  Category: {category}")
    
    try:
        # Analyze with LLM
        result = analyze_text(headline, source)
        
        # Validate against Pydantic model
        event = Event(**result)
        
        # Check for fallback error event
        if event.meta.llm_model == "error" or event.macro_effect == "Analysis Error":
            print(f"\n✗ Analysis failed (Fallback Error):")
            print(f"  Reason: {event.why}")
            return {
                "success": False,
                "headline": headline,
                "category": category,
                "event": result,
                "error": event.why,
                "validation": "fallback_error"
            }

        if show_details:
            print(f"\n✓ Analysis successful")
            print(f"  Event ID: {event.event_id}")
            print(f"  Severity: {event.severity}")
            print(f"  Sentiment: {event.event_sentiment}")
            print(f"  Macro Effect: {event.macro_effect}")
            print(f"  Market Pressure: {event.market_pressure}")
            print(f"  Horizon: {event.prediction_horizon}")
            
            # Logic Chain
            print(f"\n📊 Logic Chain:")
            for node in event.logic_chain:
                print(f"  {node.type.upper():8s} → {node.text}")
            
            # Affected Assets
            print(f"\n💼 Affected Assets ({len(event.affected_assets)}):")
            for asset in event.affected_assets:
                print(f"  {asset.ticker:6s} | {asset.prediction:8s} | Confidence: {asset.confidence:.2f}")
                print(f"         {asset.reason}")
            
            print(f"\n💡 Why: {event.why}")
            print(f"🤖 Model: {event.meta.llm_model}")
        
        return {
            "success": True,
            "headline": headline,
            "category": category,
            "event": result,
            "validation": "passed"
        }
        
    except ValidationError as e:
        print(f"\n✗ Validation failed:")
        print(f"  {e}")
        return {
            "success": False,
            "headline": headline,
            "category": category,
            "error": str(e),
            "validation": "failed"
        }
    except Exception as e:
        print(f"\n✗ Analysis failed:")
        print(f"  {e}")
        return {
            "success": False,
            "headline": headline,
            "category": category,
            "error": str(e),
            "validation": "error"
        }


def analyze_results(results: List[Dict[str, Any]]):
    """Analyze and summarize test results."""
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total headlines tested: {total}")
    print(f"  Successful analyses: {successful} ({successful/total*100:.1f}%)")
    print(f"  Failed analyses: {failed} ({failed/total*100:.1f}%)")
    
    if successful > 0:
        # Analyze successful results
        events = [r["event"] for r in results if r["success"]]
        
        # Severity distribution
        severities = {}
        for event in events:
            sev = event.get("severity", "UNKNOWN")
            severities[sev] = severities.get(sev, 0) + 1
        
        print(f"\n📈 Severity Distribution:")
        for sev, count in sorted(severities.items()):
            print(f"  {sev:8s}: {count} ({count/successful*100:.1f}%)")
        
        # Market pressure distribution
        pressures = {}
        for event in events:
            press = event.get("market_pressure", "UNKNOWN")
            pressures[press] = pressures.get(press, 0) + 1
        
        print(f"\n📉 Market Pressure Distribution:")
        for press, count in sorted(pressures.items()):
            print(f"  {press:15s}: {count} ({count/successful*100:.1f}%)")
        
        # Average confidence
        all_confidences = []
        for event in events:
            for asset in event.get("affected_assets", []):
                all_confidences.append(asset.get("confidence", 0))
        
        if all_confidences:
            avg_conf = sum(all_confidences) / len(all_confidences)
            print(f"\n🎯 Average Prediction Confidence: {avg_conf:.2f}")
        
        # Logic chain completeness
        complete_chains = sum(1 for e in events if len(e.get("logic_chain", [])) >= 4)
        print(f"\n🔗 Complete Logic Chains: {complete_chains}/{successful} ({complete_chains/successful*100:.1f}%)")


def save_results(results: List[Dict[str, Any]], filename: str = "test_results.json"):
    """Save test results to JSON file."""
    output_dir = os.path.join(os.path.dirname(__file__), "test_results")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"{timestamp}_{filename}")
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: {filepath}")
    return filepath


def main():
    """Run real-time LLM testing."""
    print("\n" + "="*80)
    print("REAL-TIME LLM TESTING")
    print("="*80)
    
    # Check API keys
    if not check_api_keys():
        print("\n⚠ Cannot proceed without API keys. Exiting.")
        sys.exit(1)
    
    # Show active client
    client = get_llm_client()
    client_type = type(client).__name__
    print(f"\n🤖 Active LLM Client: {client_type}")
    
    if client_type == "MockLLMClient":
        print("\n⚠ WARNING: Using MockLLMClient. Set API keys for real testing.")
        response = input("\nContinue with mock client? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Run tests
    print(f"\n📋 Testing {len(TEST_HEADLINES)} headlines...")
    
    results = []
    for i, headline_data in enumerate(TEST_HEADLINES, 1):
        print(f"\n[{i}/{len(TEST_HEADLINES)}]")
        result = test_single_headline(headline_data, show_details=True)
        results.append(result)
        
        # Add delay between requests to avoid rate limiting (60 req/min)
        if i < len(TEST_HEADLINES):
            print(f"\n⏳ Waiting 3s before next test...")
            time.sleep(3)
    
    # Analyze results
    analyze_results(results)
    
    # Save results
    save_results(results)
    
    # Final summary
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)
    
    successful = sum(1 for r in results if r["success"])
    if successful == len(results):
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠ {len(results) - successful} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

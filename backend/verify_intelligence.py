"""
Verification script for the Intelligence Pipeline.
Tests the pipeline with mock and real LLM clients.
"""

import sys
import os
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.intelligence.pipeline import analyze_text
from app.storage.models import Event
from pydantic import ValidationError


def test_pipeline_with_mock():
    """Test the pipeline using MockLLMClient (no API key required)."""
    print("\n" + "="*80)
    print("TEST 1: Pipeline with MockLLMClient")
    print("="*80)
    
    # Ensure no API keys are set for this test
    original_google_key = os.environ.get("GOOGLE_API_KEY")
    original_openai_key = os.environ.get("OPENAI_API_KEY")
    
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    # Reset the global client to force re-initialization
    import app.intelligence.pipeline as pipeline_module
    pipeline_module._llm_client = None
    
    try:
        # Test with a sample headline
        headline = "Fed announces interest rate cut to stimulate economy"
        source = "Reuters"
        
        print(f"\n📰 Analyzing: '{headline}'")
        print(f"📍 Source: {source}")
        
        # Call the pipeline
        result = analyze_text(headline, source)
        
        print(f"\n✓ Pipeline returned result")
        print(f"  Event ID: {result.get('event_id')}")
        print(f"  Severity: {result.get('severity')}")
        print(f"  Macro Effect: {result.get('macro_effect')}")
        print(f"  Market Pressure: {result.get('market_pressure')}")
        print(f"  Affected Assets: {len(result.get('affected_assets', []))} assets")
        
        # Validate against Pydantic model
        try:
            event = Event(**result)
            print(f"\n✓ Result successfully validated against Event model")
            print(f"  Event sentiment: {event.event_sentiment}")
            print(f"  Prediction horizon: {event.prediction_horizon}")
            print(f"  Logic chain steps: {len(event.logic_chain)}")
            
            # Print logic chain
            print(f"\n📊 Logic Chain:")
            for node in event.logic_chain:
                print(f"  {node.type.upper()}: {node.text}")
            
            # Print affected assets
            print(f"\n💼 Affected Assets:")
            for asset in event.affected_assets:
                print(f"  {asset.ticker} ({asset.name})")
                print(f"    Prediction: {asset.prediction} | Confidence: {asset.confidence:.2f}")
                print(f"    Reason: {asset.reason}")
            
            return True
            
        except ValidationError as e:
            print(f"\n✗ Validation failed against Event model:")
            print(e)
            return False
            
    finally:
        # Restore original API keys
        if original_google_key:
            os.environ["GOOGLE_API_KEY"] = original_google_key
        if original_openai_key:
            os.environ["OPENAI_API_KEY"] = original_openai_key
        
        # Reset the global client
        pipeline_module._llm_client = None


def test_pipeline_with_real_llm():
    """Test the pipeline with a real LLM (requires API key)."""
    print("\n" + "="*80)
    print("TEST 2: Pipeline with Real LLM")
    print("="*80)
    
    # Check if API keys are available
    has_google_key = bool(os.getenv("GOOGLE_API_KEY"))
    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    
    if not has_google_key and not has_openai_key:
        print("\n⚠ Skipping real LLM test: No API keys found")
        print("  Set GOOGLE_API_KEY or OPENAI_API_KEY to test with real LLM")
        return None
    
    # Reset the global client to force re-initialization
    import app.intelligence.pipeline as pipeline_module
    pipeline_module._llm_client = None
    
    try:
        # Test with multiple headlines
        test_cases = [
            ("OPEC announces surprise oil production cut", "Bloomberg"),
            ("Tech giants face new AI regulation in Europe", "Financial Times"),
            ("Federal Reserve signals potential rate hike", "Wall Street Journal"),
        ]
        
        for headline, source in test_cases:
            print(f"\n📰 Analyzing: '{headline}'")
            print(f"📍 Source: {source}")
            
            # Call the pipeline
            result = analyze_text(headline, source)
            
            print(f"\n✓ Pipeline returned result")
            print(f"  Event ID: {result.get('event_id')}")
            print(f"  Severity: {result.get('severity')}")
            print(f"  Macro Effect: {result.get('macro_effect')}")
            
            # Validate against Pydantic model
            try:
                event = Event(**result)
                print(f"✓ Result validated against Event model")
                
                # Print logic chain
                print(f"\n📊 Logic Chain:")
                for node in event.logic_chain:
                    print(f"  {node.type.upper()}: {node.text}")
                
                # Print top affected asset
                if event.affected_assets:
                    top_asset = event.affected_assets[0]
                    print(f"\n💼 Top Affected Asset:")
                    print(f"  {top_asset.ticker} ({top_asset.name})")
                    print(f"  Prediction: {top_asset.prediction} | Confidence: {top_asset.confidence:.2f}")
                
            except ValidationError as e:
                print(f"\n✗ Validation failed:")
                print(e)
                return False
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during real LLM test: {e}")
        return False


def main():
    """Run all verification tests."""
    print("\n" + "="*80)
    print("INTELLIGENCE PIPELINE VERIFICATION")
    print("="*80)
    
    # Test 1: Mock client
    mock_success = test_pipeline_with_mock()
    
    # Test 2: Real LLM (if API keys available)
    real_success = test_pipeline_with_real_llm()
    
    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    print(f"Mock Client Test: {'✓ PASSED' if mock_success else '✗ FAILED'}")
    if real_success is not None:
        print(f"Real LLM Test: {'✓ PASSED' if real_success else '✗ FAILED'}")
    else:
        print(f"Real LLM Test: ⊘ SKIPPED (no API keys)")
    
    print("\n" + "="*80)
    
    # Exit with appropriate code
    if not mock_success or (real_success is not None and not real_success):
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()

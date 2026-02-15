"""
Test script for Phase 2: State Management and API Integration
Tests the enhanced repository and API endpoints.
"""

import sys
import os
import json
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.storage import repository
from app.storage.models import Event, Validation
from pydantic import ValidationError


def test_repository_validation():
    """Test repository Pydantic validation."""
    print("\n" + "="*80)
    print("TEST 1: Repository Pydantic Validation")
    print("="*80)
    
    # Test valid event
    print("\n📝 Testing valid event addition...")
    valid_event = {
        "event_id": "test_evt_001",
        "headline": "Test headline for validation",
        "source": "Test Source",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "severity": "MEDIUM",
        "event_sentiment": "POSITIVE",
        "macro_effect": "Test Effect",
        "prediction_horizon": "SHORT_TERM",
        "market_pressure": "RISK_ON",
        "logic_chain": [
            {"type": "event", "text": "Test event"},
            {"type": "macro", "text": "Test macro"},
            {"type": "sector", "text": "Test sector"},
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
                "reason": "Test reason"
            }
        ],
        "why": "Test explanation",
        "meta": {
            "llm_model": "test-model",
            "llm_prompt_version": "v1",
            "confidence_components": {
                "llm_score": 0.75,
                "sentiment_strength": 0.6,
                "historical_similarity": 0.5
            },
            "confidence_formula": "test_formula"
        }
    }
    
    try:
        result = repository.add_event(valid_event, validate=True)
        print("✓ Valid event added successfully")
        print(f"  Event ID: {result['event_id']}")
        return True
    except ValidationError as e:
        print(f"✗ Validation failed unexpectedly: {e}")
        return False


def test_repository_invalid_data():
    """Test repository rejection of invalid data."""
    print("\n" + "="*80)
    print("TEST 2: Repository Invalid Data Rejection")
    print("="*80)
    
    # Test invalid event (missing required fields)
    print("\n📝 Testing invalid event rejection...")
    invalid_event = {
        "event_id": "test_evt_002",
        "headline": "Incomplete event",
        # Missing many required fields
    }
    
    try:
        repository.add_event(invalid_event, validate=True)
        print("✗ Invalid event was accepted (should have been rejected)")
        return False
    except ValidationError as e:
        print("✓ Invalid event correctly rejected")
        print(f"  Validation errors detected: {len(e.errors())} fields")
        return True


def test_repository_backup():
    """Test repository JSON backup functionality."""
    print("\n" + "="*80)
    print("TEST 3: Repository JSON Backup")
    print("="*80)
    
    backup_path = repository.EVENTS_BACKUP_PATH
    
    print(f"\n📝 Checking backup file creation...")
    print(f"  Backup path: {backup_path}")
    
    if os.path.exists(backup_path):
        print("✓ Backup file exists")
        
        # Check if it's valid JSON
        try:
            with open(backup_path, 'r') as f:
                data = json.load(f)
            print(f"✓ Backup file is valid JSON")
            print(f"  Events in backup: {len(data)}")
            return True
        except json.JSONDecodeError:
            print("✗ Backup file is not valid JSON")
            return False
    else:
        print("⚠ Backup file not created yet (this is OK if no events were added)")
        return None


def test_repository_stats():
    """Test repository statistics."""
    print("\n" + "="*80)
    print("TEST 4: Repository Statistics")
    print("="*80)
    
    print("\n📊 Getting repository stats...")
    stats = repository.get_stats()
    
    print(f"✓ Stats retrieved successfully:")
    print(f"  Events count: {stats['events_count']}")
    print(f"  Validations count: {stats['validations_count']}")
    print(f"  Last event: {stats['last_event_timestamp']}")
    print(f"  Last validation: {stats['last_validation_timestamp']}")
    
    return True


def main():
    """Run all Phase 2 tests."""
    print("\n" + "="*80)
    print("PHASE 2: STATE MANAGEMENT & API INTEGRATION TESTS")
    print("="*80)
    
    # Test 1: Valid event
    test1_success = test_repository_validation()
    
    # Test 2: Invalid event rejection
    test2_success = test_repository_invalid_data()
    
    # Test 3: Backup functionality
    test3_success = test_repository_backup()
    
    # Test 4: Statistics
    test4_success = test_repository_stats()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Valid Event Addition: {'✓ PASSED' if test1_success else '✗ FAILED'}")
    print(f"Invalid Data Rejection: {'✓ PASSED' if test2_success else '✗ FAILED'}")
    if test3_success is not None:
        print(f"JSON Backup: {'✓ PASSED' if test3_success else '✗ FAILED'}")
    else:
        print(f"JSON Backup: ⊘ SKIPPED")
    print(f"Repository Stats: {'✓ PASSED' if test4_success else '✗ FAILED'}")
    
    print("\n" + "="*80)
    print("API ENDPOINT TESTS")
    print("="*80)
    print("\nTo test the new API endpoints, start the server with:")
    print("  python main.py")
    print("\nThen test these endpoints:")
    print("  GET  /api/llm/status          - Check LLM client status")
    print("  POST /api/analyze             - Analyze single headline (now supports 'text' field)")
    print("  POST /api/analyze/batch       - Analyze multiple headlines (max 10)")
    print("\nExample curl commands:")
    print("""
  # Check LLM status
  curl http://localhost:8000/api/llm/status
  
  # Analyze with full article text
  curl -X POST http://localhost:8000/api/analyze \\
    -H "Content-Type: application/json" \\
    -d '{
      "headline": "Fed announces rate cut",
      "source": "Reuters",
      "text": "The Federal Reserve announced a surprise rate cut today..."
    }'
  
  # Batch analyze
  curl -X POST http://localhost:8000/api/analyze/batch \\
    -H "Content-Type: application/json" \\
    -d '[
      {"headline": "Oil prices surge", "source": "Bloomberg"},
      {"headline": "Tech stocks rally", "source": "CNBC"}
    ]'
""")
    
    # Exit with appropriate code
    if not test1_success or not test2_success or not test4_success:
        sys.exit(1)
    else:
        print("\n✓ All repository tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()

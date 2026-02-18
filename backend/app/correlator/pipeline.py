import random
from datetime import datetime
from typing import Dict, Any

def validate_prediction(event: Dict[str, Any], horizon: str) -> Dict[str, Any]:
    """
    Simulate market movement and validate prediction.
    Only handles market data (prices, returns).
    """
    if not event.get("affected_assets"):
        raise ValueError("No assets to validate")
        
    asset = event["affected_assets"][0]
    predicted_direction = asset.get("prediction", "NEUTRAL")
    predicted_confidence = asset.get("confidence", 0.5)
    predicted_ticker = asset.get("ticker", "SPY")
    
    # Simulate price movement logic moved from main.py
    mock_price_at_event = 100.0
    # 70% chance to match prediction (for demo purposes)
    direction_matches = random.random() < 0.70
    
    if predicted_direction == "BULLISH":
        change = random.uniform(0.5, 3.0) if direction_matches else random.uniform(-3.0, -0.5)
    elif predicted_direction == "BEARISH":
        change = random.uniform(-3.0, -0.5) if direction_matches else random.uniform(0.5, 3.0)
    else:
        change = random.uniform(-1.0, 1.0)
    
    mock_price_at_validation = mock_price_at_event * (1 + change / 100)
    
    # Determine if prediction was correct
    thresholds = {"1h": 0.5, "6h": 1.5, "24h": 3.0}
    threshold = thresholds.get(horizon, 1.0)
    
    if predicted_direction == "BULLISH" and change > threshold:
        status = "CORRECT"
    elif predicted_direction == "BEARISH" and change < -threshold:
        status = "CORRECT"
    elif abs(change) < threshold:
        status = "PENDING"
    else:
        status = "INCORRECT"
        
    return {
        "event_id": event.get("event_id"),
        "headline": event.get("headline", ""),
        "predicted_direction": predicted_direction,
        "predicted_ticker": predicted_ticker,
        "predicted_confidence": predicted_confidence,
        "horizon": horizon,
        "price_at_event": mock_price_at_event,
        "price_at_validation": round(mock_price_at_validation, 2),
        "actual_change_percent": round(change, 2),
        "status": status,
        "validated_at": datetime.utcnow().isoformat() + "Z",
    }

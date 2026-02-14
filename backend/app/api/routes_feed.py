from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
import random
from typing import Optional

from app.storage.models import (
    EventsResponse,
    ValidationResponse,
    AnalyzeRequest,
)
from app.storage import repository
from app.intelligence.pipeline import analyze_text
from app.correlator.pipeline import validate_prediction

router = APIRouter()

@router.get("/")
async def root():
    return {
        "message": "GeoPulse AI API",
        "version": "1.0.0",
        "status": "running",
    }


@router.get("/api/events", response_model=EventsResponse)
async def get_events(limit: int = Query(10, ge=1, le=50)):
    """Get latest events sorted by timestamp (newest first)."""
    sorted_events = sorted(
        repository.events_store,
        key=lambda x: x.get("timestamp", ""),
        reverse=True,
    )[:limit]
    return {"status": "success", "data": sorted_events}


@router.get("/api/events/{event_id}")
async def get_event(event_id: str):
    """Get a specific event by ID."""
    event = next((e for e in repository.events_store if e.get("event_id") == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Include validation info if available
    validation = next(
        (v for v in repository.validations_store if v.get("event_id") == event_id),
        None,
    )
    
    return {
        "status": "success",
        "data": event,
        "validation": validation,
    }


@router.get("/api/validations", response_model=ValidationResponse)
async def get_validations(limit: int = Query(20, ge=1, le=100)):
    """Get validation results."""
    sorted_validations = sorted(
        repository.validations_store,
        key=lambda x: x.get("validated_at", ""),
        reverse=True,
    )[:limit]
    return {"status": "success", "data": sorted_validations}


@router.get("/api/validate/{event_id}")
async def validate_event(
    event_id: str,
    horizon: str = Query("1h", regex="^(1h|6h|24h)$"),
):
    """Run or get validation for a specific event and horizon."""
    event = repository.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check existing validation
    existing = repository.get_validation_by_event_id_and_horizon(event_id, horizon)
    
    if existing:
        return {"status": "success", "data": existing}
    
    # Generate mock validation using Correlator
    try:
        validation = validate_prediction(event, horizon)
        repository.add_validation(validation)
        return {"status": "success", "data": validation}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/price")
async def get_price(
    ticker: str = Query(..., min_length=1, max_length=10),
    range: str = Query("1d", regex="^(1h|1d|1w|1m)$"),
):
    """Get price data for a ticker (mock data for demo)."""
    # Generate mock price data
    now = datetime.utcnow()
    
    range_hours = {
        "1h": 1,
        "1d": 24,
        "1w": 168,
        "1m": 720,
    }
    hours = range_hours.get(range, 24)
    
    base_price = 100.0
    # Add some variety based on ticker
    ticker_seed = sum(ord(c) for c in ticker)
    random.seed(ticker_seed)
    base_price = 50 + random.random() * 200
    
    prices = []
    for i in range(hours):
        time = now - timedelta(hours=hours - i)
        # Generate somewhat realistic price movement
        noise = random.gauss(0, 0.5)
        trend = 0.01 * (i / hours)  # Slight upward trend
        price = base_price * (1 + trend + noise / 100)
        prices.append({
            "time": time.isoformat() + "Z",
            "price": round(price, 2),
        })
    
    random.seed()  # Reset seed
    
    return {
        "ticker": ticker,
        "prices": prices,
    }


@router.post("/api/analyze")
async def analyze_news(request: AnalyzeRequest):
    """
    Analyze news and generate predictions.
    """
    # Use Intelligence Layer
    event = analyze_text(
        request.headline, 
        request.source, 
        request.timestamp
    )
    
    # Add to store
    repository.add_event(event)
    
    return {"status": "success", "data": event}


@router.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "events_count": len(repository.events_store),
        "validations_count": len(repository.validations_store),
    }

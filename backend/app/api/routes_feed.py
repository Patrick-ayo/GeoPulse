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
    Supports full article analysis via the 'text' field.
    """
    try:
        # Use Intelligence Layer with optional additional_text
        event = analyze_text(
            headline=request.headline, 
            source=request.source, 
            timestamp=request.timestamp,
            additional_text=request.text  # Pass full article text if provided
        )
        
        # Add to store with validation
        repository.add_event(event, validate=True)
        
        return {"status": "success", "data": event}
        
    except Exception as e:
        # Handle LLM failures gracefully
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/api/analyze/batch")
async def analyze_news_batch(requests: list[AnalyzeRequest]):
    """
    Analyze multiple news headlines in batch.
    Maximum 10 headlines per request.
    """
    if len(requests) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 headlines per batch request"
        )
    
    results = []
    errors = []
    
    for idx, request in enumerate(requests):
        try:
            # Use Intelligence Layer
            event = analyze_text(
                headline=request.headline,
                source=request.source,
                timestamp=request.timestamp,
                additional_text=request.text
            )
            
            # Add to store with validation
            repository.add_event(event, validate=True)
            results.append(event)
            
        except Exception as e:
            errors.append({
                "index": idx,
                "headline": request.headline,
                "error": str(e)
            })
    
    return {
        "status": "success" if not errors else "partial",
        "data": results,
        "errors": errors if errors else None,
        "summary": {
            "total": len(requests),
            "successful": len(results),
            "failed": len(errors)
        }
    }


@router.get("/api/llm/status")
async def get_llm_status():
    """
    Get the current LLM client status.
    Shows which LLM provider is active and available.
    """
    from app.intelligence.pipeline import get_llm_client
    
    llm_client = get_llm_client()
    client_type = type(llm_client).__name__
    
    # Check API key availability
    import os
    has_google_key = bool(os.getenv("GOOGLE_API_KEY"))
    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    
    return {
        "status": "success",
        "data": {
            "active_client": client_type,
            "is_mock": client_type == "MockLLMClient",
            "available_providers": {
                "gemini": has_google_key,
                "openai": has_openai_key,
                "mock": True
            },
            "recommendation": "Set GOOGLE_API_KEY or OPENAI_API_KEY for real LLM analysis" if client_type == "MockLLMClient" else None
        }
    }


@router.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "events_count": len(repository.events_store),
        "validations_count": len(repository.validations_store),
    }

import json
import os
from typing import List, Optional
from datetime import datetime
from pydantic import ValidationError

from app.storage.models import Event, Validation

# Load mock data
# Assuming mock_data is 2 levels up from backend/app/storage/repository.py -> backend/app/storage -> backend/app -> backend -> mock_data
# Actually, the original file was in backend/main.py, and mock_data was in ../mock_data relative to backend.
# So from backend/app/storage/repository.py, it is ../../../mock_data
MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "mock_data", "mock_data.json")
MOCK_VALIDATIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "mock_data", "mock_validations.json")

# Optional persistence paths
PERSISTENCE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")
EVENTS_BACKUP_PATH = os.path.join(PERSISTENCE_DIR, "events_backup.json")
VALIDATIONS_BACKUP_PATH = os.path.join(PERSISTENCE_DIR, "validations_backup.json")


def load_mock_events():
    """Load mock events from JSON file."""
    try:
        with open(MOCK_DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def load_mock_validations():
    """Load mock validations from JSON file."""
    try:
        with open(MOCK_VALIDATIONS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_events_backup():
    """Save events to backup JSON file."""
    try:
        os.makedirs(PERSISTENCE_DIR, exist_ok=True)
        with open(EVENTS_BACKUP_PATH, "w") as f:
            json.dump(events_store, f, indent=2)
    except Exception as e:
        print(f"⚠ Failed to save events backup: {e}")


def save_validations_backup():
    """Save validations to backup JSON file."""
    try:
        os.makedirs(PERSISTENCE_DIR, exist_ok=True)
        with open(VALIDATIONS_BACKUP_PATH, "w") as f:
            json.dump(validations_store, f, indent=2)
    except Exception as e:
        print(f"⚠ Failed to save validations backup: {e}")


def validate_event_data(event_data: dict) -> Event:
    """
    Validate event data against Event Pydantic model.
    
    Args:
        event_data: Dictionary containing event data
        
    Returns:
        Validated Event model instance
        
    Raises:
        ValidationError: If data doesn't match Event model schema
    """
    return Event(**event_data)


def validate_validation_data(validation_data: dict) -> Validation:
    """
    Validate validation data against Validation Pydantic model.
    
    Args:
        validation_data: Dictionary containing validation data
        
    Returns:
        Validated Validation model instance
        
    Raises:
        ValidationError: If data doesn't match Validation model schema
    """
    return Validation(**validation_data)


# In-memory storage (would be MongoDB in production)
events_store = load_mock_events()
validations_store = load_mock_validations()


def get_events() -> List[dict]:
    """Get all events."""
    return events_store


def get_event_by_id(event_id: str) -> Optional[dict]:
    """Get a specific event by ID."""
    return next((e for e in events_store if e.get("event_id") == event_id), None)


def add_event(event: dict, validate: bool = True) -> dict:
    """
    Add an event to the store.
    
    Args:
        event: Event data dictionary
        validate: Whether to validate against Pydantic model (default: True)
        
    Returns:
        The added event data
        
    Raises:
        ValidationError: If validation is enabled and data is invalid
    """
    if validate:
        # Validate against Pydantic model
        validated_event = validate_event_data(event)
        # Convert back to dict for storage
        event = validated_event.model_dump(mode='json')
    
    events_store.insert(0, event)
    
    # Optional: Save backup
    save_events_backup()
    
    return event


def get_validations() -> List[dict]:
    """Get all validations."""
    return validations_store


def get_validation_by_event_id(event_id: str) -> Optional[dict]:
    """Get validation by event ID."""
    return next(
        (v for v in validations_store if v.get("event_id") == event_id),
        None,
    )


def get_validation_by_event_id_and_horizon(event_id: str, horizon: str) -> Optional[dict]:
    """Get validation by event ID and horizon."""
    return next(
        (v for v in validations_store 
         if v.get("event_id") == event_id and v.get("horizon") == horizon),
        None,
    )


def add_validation(validation: dict, validate: bool = True) -> dict:
    """
    Add a validation to the store.
    
    Args:
        validation: Validation data dictionary
        validate: Whether to validate against Pydantic model (default: True)
        
    Returns:
        The added validation data
        
    Raises:
        ValidationError: If validation is enabled and data is invalid
    """
    if validate:
        # Validate against Pydantic model
        validated_validation = validate_validation_data(validation)
        # Convert back to dict for storage
        validation = validated_validation.model_dump(mode='json')
    
    validations_store.append(validation)
    
    # Optional: Save backup
    save_validations_backup()
    
    return validation


def get_stats() -> dict:
    """Get repository statistics."""
    return {
        "events_count": len(events_store),
        "validations_count": len(validations_store),
        "last_event_timestamp": events_store[0].get("timestamp") if events_store else None,
        "last_validation_timestamp": validations_store[-1].get("validated_at") if validations_store else None,
    }

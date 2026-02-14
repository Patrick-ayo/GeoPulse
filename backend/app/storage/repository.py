import json
import os
from typing import List, Optional

from app.storage.models import Event, Validation

# Load mock data
# Assuming mock_data is 2 levels up from backend/app/storage/repository.py -> backend/app/storage -> backend/app -> backend -> mock_data
# Actually, the original file was in backend/main.py, and mock_data was in ../mock_data relative to backend.
# So from backend/app/storage/repository.py, it is ../../../mock_data
MOCK_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "mock_data", "mock_data.json")
MOCK_VALIDATIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "mock_data", "mock_validations.json")


def load_mock_events():
    try:
        with open(MOCK_DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def load_mock_validations():
    try:
        with open(MOCK_VALIDATIONS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# In-memory storage (would be MongoDB in production)
events_store = load_mock_events()
validations_store = load_mock_validations()

def get_events() -> List[dict]:
    return events_store

def get_event_by_id(event_id: str) -> Optional[dict]:
    return next((e for e in events_store if e.get("event_id") == event_id), None)

def add_event(event: dict):
    events_store.insert(0, event)

def get_validations() -> List[dict]:
    return validations_store

def get_validation_by_event_id(event_id: str) -> Optional[dict]:
    return next(
        (v for v in validations_store if v.get("event_id") == event_id),
        None,
    )

def get_validation_by_event_id_and_horizon(event_id: str, horizon: str) -> Optional[dict]:
    return next(
        (v for v in validations_store 
         if v.get("event_id") == event_id and v.get("horizon") == horizon),
        None,
    )

def add_validation(validation: dict):
    validations_store.append(validation)

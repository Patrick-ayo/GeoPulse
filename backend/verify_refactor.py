from fastapi.testclient import TestClient
import sys
import os

# Add the current directory to sys.path to import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

def test_analyze_and_validate():
    print("Testing /api/analyze...")
    response = client.post("/api/analyze", json={
        "headline": "Fed signals potential rate hike",
        "source": "reuters"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    event_id = data["data"]["event_id"]
    print(f"Analysis success. Event ID: {event_id}")
    assert "Monetary Policy" in data["data"]["macro_effect"]

    print(f"Testing /api/validate/{event_id}...")
    response = client.get(f"/api/validate/{event_id}?horizon=1h")
    assert response.status_code == 200
    val_data = response.json()
    assert val_data["status"] == "success"
    assert val_data["data"]["event_id"] == event_id
    print("Validation success.")

    print("Testing /api/events...")
    response = client.get("/api/events")
    assert response.status_code == 200
    events = response.json()["data"]
    assert any(e["event_id"] == event_id for e in events)
    print("Events retrieval success.")

    print("Testing health check...")
    response = client.get("/api/health")
    assert response.status_code == 200
    health = response.json()
    assert health["status"] == "healthy"
    print(f"Health check success. Events count: {health['events_count']}")

if __name__ == "__main__":
    try:
        test_analyze_and_validate()
        print("\nALL TESTS PASSED!")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

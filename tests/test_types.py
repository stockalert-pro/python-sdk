"""Test type definitions."""
from datetime import datetime

from stockalert.types import Alert, WebhookPayload


def test_alert_initialization():
    """Test Alert class initialization."""
    data = {
        "id": "test-123",
        "symbol": "AAPL",
        "condition": "price_above",
        "threshold": 150.0,
        "notification": "email",
        "status": "active",
        "created_at": "2024-01-01T00:00:00Z",
        "triggered_at": "2024-01-01T01:00:00Z",
    }

    alert = Alert(data)
    assert alert.id == "test-123"
    assert alert.symbol == "AAPL"
    assert alert.condition == "price_above"
    assert alert.threshold == 150.0
    assert alert.notification == "email"
    assert alert.status == "active"
    assert isinstance(alert.created_at, datetime)
    assert isinstance(alert.updated_at, datetime)
    assert isinstance(alert.triggered_at, datetime)


def test_webhook_payload_initialization():
    """Test WebhookPayload class initialization."""
    data = {
        "id": "evt_123",
        "event": "alert.triggered",
        "timestamp": "2024-01-01T00:00:00Z",
        "data": {
            "alert": {
                "id": "test-123",
                "symbol": "AAPL",
                "condition": "price_above",
                "threshold": 150.0,
                "status": "triggered",
            },
            "stock": {
                "symbol": "AAPL",
                "price": 155.0,
            },
        }
    }

    payload = WebhookPayload(data)
    assert payload.event == "alert.triggered"
    assert isinstance(payload.timestamp, datetime)
    assert payload.id == "evt_123"
    assert payload.data["alert"]["id"] == "test-123"
    assert payload.data["stock"]["price"] == 155.0

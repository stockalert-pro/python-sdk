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
        "updated_at": "2024-01-01T00:00:00Z",
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


def test_webhook_payload_initialization():
    """Test WebhookPayload class initialization."""
    data = {
        "event": "alert.triggered",
        "timestamp": "2024-01-01T00:00:00Z",
        "data": {
            "alert_id": "test-123",
            "symbol": "AAPL",
            "condition": "price_above",
            "threshold": 150.0,
            "current_value": 155.0,
        }
    }

    payload = WebhookPayload(data)
    assert payload.event == "alert.triggered"
    assert isinstance(payload.timestamp, datetime)
    assert payload.data["alert_id"] == "test-123"

"""Test type definitions."""
from datetime import datetime

from stockalert.types import Alert, PaginatedResponse, UserSubscription, WebhookPayload


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


def test_user_subscription_initialization():
    """Test UserSubscription class initialization."""
    data = {
        "id": "sub_123",
        "account_type": "premium",
        "status": "active",
        "is_early_bird": False,
        "is_early_bird_eligible": True,
        "is_premium": True,
        "cancel_at_period_end": False,
        "quotas": {"sms": 50},
        "usage": {"count": 12},
        "current_period": {
            "start": "2026-03-01T00:00:00Z",
            "end": "2026-04-01T00:00:00Z",
        },
        "alerts": {
            "counts": {"total": 7, "by_status": {"active": 7}},
            "quota": {"limit": None, "remaining": None, "unlimited": True},
        },
        "watchlist_items_count": 9,
        "watchlist_quota": 100,
    }

    subscription = UserSubscription(data)
    assert subscription.id == "sub_123"
    assert subscription.account_type == "premium"
    assert isinstance(subscription.current_period["start"], datetime)
    assert subscription.alerts["counts"]["total"] == 7


def test_paginated_response_preserves_dict_style_access():
    """Test PaginatedResponse compatibility helpers."""
    alert = Alert({
        "id": "test-123",
        "symbol": "AAPL",
        "condition": "price_above",
        "threshold": 150.0,
        "notification": "email",
        "status": "active",
        "created_at": "2024-01-01T00:00:00Z",
    })

    response = PaginatedResponse(
        [alert],
        {
            "pagination": {"page": 1, "limit": 50, "total": 1, "total_pages": 1},
            "rate_limit": {"limit": 30, "remaining": 29, "reset": 1736180400000},
        },
    )

    assert "data" in response
    assert response["data"][0]["id"] == "test-123"
    assert response.get("meta", {})["pagination"]["page"] == 1
    assert response.to_dict()["meta"]["rate_limit"]["remaining"] == 29

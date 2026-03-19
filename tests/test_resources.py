"""Tests for typed resource wrappers."""
from unittest.mock import AsyncMock, patch

import pytest

from stockalert import AsyncStockAlert, StockAlert
from stockalert.types import Alert, PaginatedResponse, UserSubscription


def make_alert_payload(alert_id: str = "alert_123") -> dict:
    return {
        "id": alert_id,
        "symbol": "AAPL",
        "condition": "price_above",
        "threshold": 150.0,
        "notification": "email",
        "status": "active",
        "created_at": "2026-03-19T12:00:00Z",
        "updated_at": "2026-03-19T12:00:00Z",
    }


def make_paginated_payload() -> dict:
    return {
        "data": [make_alert_payload()],
        "meta": {
            "pagination": {"page": 1, "limit": 50, "total": 1, "total_pages": 1},
            "rate_limit": {"limit": 30, "remaining": 29, "reset": 1736180400000},
        },
    }


def make_subscription_payload() -> dict:
    return {
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
            "counts": {
                "total": 7,
                "by_status": {"active": 7, "paused": 0, "triggered": 0, "inactive": 0},
            },
            "quota": {"limit": None, "remaining": None, "unlimited": True},
        },
        "watchlist_items_count": 9,
        "watchlist_quota": 100,
    }


def test_sync_client_initializes_user_resource():
    """Test that the sync client exposes the user resource."""
    client = StockAlert(api_key="sk_test_valid_key")
    assert client.user is not None


def test_alerts_list_returns_paginated_response():
    """Test that alerts.list returns typed paginated results."""
    client = StockAlert(api_key="sk_test_valid_key")

    with patch.object(client.alerts, "_request", return_value=make_paginated_payload()):
        response = client.alerts.list(limit=1)

    assert isinstance(response, PaginatedResponse)
    assert isinstance(response.data[0], Alert)
    assert response.page == 1
    assert response.rate_limit["remaining"] == 29
    assert response["data"][0]["id"] == "alert_123"


def test_user_get_subscription_returns_typed_object():
    """Test that user.get_subscription returns a typed subscription object."""
    client = StockAlert(api_key="sk_test_valid_key")

    with patch.object(client.user, "_request", return_value=make_subscription_payload()):
        subscription = client.user.get_subscription()

    assert isinstance(subscription, UserSubscription)
    assert subscription.account_type == "premium"
    assert subscription.alerts["quota"]["unlimited"] is True
    assert subscription.current_period["start"] is not None


@pytest.mark.asyncio
async def test_async_client_exposes_user_resource_and_typed_list_results():
    """Test async resource parity for user and paginated alert responses."""
    pytest.importorskip("httpx")

    async with AsyncStockAlert(api_key="sk_test_valid_key") as client:
        assert client.user is not None

        with patch.object(client, "_request", new=AsyncMock(return_value=make_paginated_payload())):
            response = await client.alerts.list(limit=1)

        assert isinstance(response, PaginatedResponse)
        assert isinstance(response.data[0], Alert)


@pytest.mark.asyncio
async def test_async_user_get_subscription_returns_typed_object():
    """Test async user subscription lookups."""
    pytest.importorskip("httpx")

    async with AsyncStockAlert(api_key="sk_test_valid_key") as client:
        with patch.object(client, "_request", new=AsyncMock(return_value=make_subscription_payload())):
            subscription = await client.user.get_subscription()

    assert isinstance(subscription, UserSubscription)
    assert subscription.watchlist_quota == 100

"""Test validation logic."""
import pytest

from stockalert.client import StockAlert
from stockalert.exceptions import ValidationError
from stockalert.resources.alerts import AlertsResource


class MockClient:
    """Mock client for testing."""
    def _request(self, *args, **kwargs):
        return {"data": {"id": "test"}}


def test_alert_validation():
    """Test alert validation."""
    resource = AlertsResource(MockClient())

    # Test missing symbol
    with pytest.raises(ValidationError, match="Symbol is required"):
        resource._validate_create_request({"condition": "price_above"})

    # Test invalid symbol
    with pytest.raises(ValidationError, match="Symbol must be 1-5 uppercase letters"):
        resource._validate_create_request({"symbol": "TOOLONG", "condition": "price_above"})

    # Test missing condition
    with pytest.raises(ValidationError, match="Condition is required"):
        resource._validate_create_request({"symbol": "AAPL"})

    # Test invalid notification channel
    with pytest.raises(ValidationError, match="Notification must be one of"):
        resource._validate_create_request({
            "symbol": "AAPL",
            "condition": "price_above",
            "notification": "whatsapp"  # Not allowed!
        })

    # Test condition requiring threshold
    with pytest.raises(ValidationError, match="requires a threshold value"):
        resource._validate_create_request({
            "symbol": "AAPL",
            "condition": "price_above"
        })

    # Test condition not allowing threshold
    with pytest.raises(ValidationError, match="does not use a threshold value"):
        resource._validate_create_request({
            "symbol": "AAPL",
            "condition": "earnings_announcement",
            "threshold": 100
        })


def test_client_validation():
    """Test client validation."""
    # Test missing API key
    with pytest.raises(ValidationError, match="API key is required"):
        StockAlert(api_key="")

    # Test invalid API key format
    with pytest.raises(ValidationError, match="Invalid API key format"):
        StockAlert(api_key="invalid_key")

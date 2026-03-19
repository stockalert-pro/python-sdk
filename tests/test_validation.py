"""Test validation logic."""
import pytest

from stockalert.client import StockAlert
from stockalert.exceptions import ValidationError
from stockalert.resources.alerts import AlertsResource


def make_resource() -> AlertsResource:
    return AlertsResource(
        {
            "api_key": "sk_test_valid_key",
            "base_url": "https://stockalert.pro/api/v1",
            "timeout": 30,
            "max_retries": 3,
        }
    )


def test_alert_validation_base_fields():
    """Test core alert validation."""
    resource = make_resource()

    with pytest.raises(ValidationError, match="Symbol is required"):
        resource._validate_create_request({"condition": "price_above"})

    with pytest.raises(ValidationError, match="Symbol must be 1-10 chars"):
        resource._validate_create_request({"symbol": "TOOLONGSYMBOL", "condition": "price_above"})

    with pytest.raises(ValidationError, match="Condition is required"):
        resource._validate_create_request({"symbol": "AAPL"})

    with pytest.raises(ValidationError, match="Notification must be one of"):
        resource._validate_create_request(
            {
                "symbol": "AAPL",
                "condition": "price_above",
                "threshold": 100,
                "notification": "whatsapp",
            }
        )


def test_alert_validation_current_threshold_contract():
    """Test threshold rules for current public alert types."""
    resource = make_resource()

    with pytest.raises(ValidationError, match="price_above requires a threshold value"):
        resource._validate_create_request({"symbol": "AAPL", "condition": "price_above"})

    resource._validate_create_request({"symbol": "AAPL", "condition": "new_high"})

    with pytest.raises(ValidationError, match="daily_reminder does not use a threshold value"):
        resource._validate_create_request(
            {"symbol": "AAPL", "condition": "daily_reminder", "threshold": 1}
        )

    with pytest.raises(ValidationError, match="earnings_announcement requires a threshold value"):
        resource._validate_create_request({"symbol": "AAPL", "condition": "earnings_announcement"})

    with pytest.raises(
        ValidationError,
        match="ma_touch_above requires a positive moving average period as threshold",
    ):
        resource._validate_create_request(
            {"symbol": "AAPL", "condition": "ma_touch_above", "threshold": 12.5}
        )


def test_alert_validation_current_parameters():
    """Test parameter validation for reminder-like and insider alerts."""
    resource = make_resource()

    with pytest.raises(ValidationError, match="Reminder alerts require reminder_date and reminder_time"):
        resource._validate_create_request(
            {"symbol": "AAPL", "condition": "reminder", "threshold": 30}
        )

    resource._validate_create_request(
        {
            "symbol": "AAPL",
            "condition": "daily_reminder",
            "parameters": {"deliveryTime": "after_market_close"},
        }
    )

    with pytest.raises(ValidationError, match="Dividend payment alerts require a positive shares parameter"):
        resource._validate_create_request({"symbol": "KO", "condition": "dividend_payment"})

    resource._validate_create_request(
        {
            "symbol": "KO",
            "condition": "dividend_payment",
            "parameters": {"shares": 25},
        }
    )

    with pytest.raises(ValidationError, match="insider_transactions direction must be buy, sell or both"):
        resource._validate_create_request(
            {
                "symbol": "MSFT",
                "condition": "insider_transactions",
                "threshold": 100000,
                "parameters": {"direction": "invalid"},
            }
        )

    resource._validate_create_request(
        {
            "symbol": "MSFT",
            "condition": "insider_transactions",
            "threshold": 100000,
            "parameters": {
                "direction": "both",
                "minExecutives": 2,
                "windowDays": 14,
                "openMarketOnly": True,
            },
        }
    )


def test_client_validation():
    """Test client validation."""
    with pytest.raises(ValidationError, match="API key is required"):
        StockAlert(api_key="")

    with pytest.raises(ValidationError, match="Invalid API key format"):
        StockAlert(api_key="invalid_key")

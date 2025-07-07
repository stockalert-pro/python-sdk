"""Test client initialization."""
import pytest
from stockalert import StockAlert
from stockalert.exceptions import ValidationError


def test_client_requires_api_key():
    """Test that client requires an API key."""
    with pytest.raises(ValidationError, match="API key is required"):
        StockAlert(api_key="")


def test_client_validates_api_key_format():
    """Test that client validates API key format."""
    with pytest.raises(ValidationError, match="Invalid API key format"):
        StockAlert(api_key="invalid")
    
    with pytest.raises(ValidationError, match="Invalid API key format"):
        StockAlert(api_key="sk_123")  # Too short


def test_client_accepts_valid_api_key():
    """Test that client accepts valid API key."""
    client = StockAlert(api_key="sk_test_valid_key")
    assert client.api_key == "sk_test_valid_key"
    assert client.base_url == "https://stockalert.pro/api/public/v1"
    assert client.timeout == 30
    assert client.max_retries == 3

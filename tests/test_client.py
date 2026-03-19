"""Test client initialization."""
import pytest

from stockalert import StockAlert, _build_missing_async_client
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
    assert client.base_url == "https://stockalert.pro/api/v1"
    assert client.timeout == 30
    assert client.max_retries == 3
    assert client.user is not None


def test_missing_async_client_raises_helpful_import_error():
    """Test that missing async dependencies raise a clear error when instantiated."""
    AsyncStockAlert = _build_missing_async_client(
        ImportError("The async client requires httpx. Install it with: pip install stockalert[async]")
    )

    with pytest.raises(ImportError, match="requires httpx"):
        AsyncStockAlert(api_key="sk_test_valid_key")

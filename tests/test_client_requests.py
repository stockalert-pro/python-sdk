"""Test client HTTP request handling."""
from unittest.mock import Mock, patch

import pytest
import requests

from stockalert import NetworkError, RateLimitError, StockAlert


class TestClientRequests:
    """Test HTTP request handling."""

    def test_successful_request(self):
        """Test successful API request."""
        client = StockAlert(api_key="sk_test_key")

        mock_response = Mock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": {"id": "123"}}

        with patch.object(client.session, "request", return_value=mock_response):
            result = client._request("GET", "/test")
            assert result == {"id": "123"}

    def test_rate_limit_error(self):
        """Test rate limit handling."""
        client = StockAlert(api_key="sk_test_key")

        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_response.json.return_value = {"error": "Rate limit exceeded"}

        with patch.object(client.session, "request", return_value=mock_response):
            with pytest.raises(RateLimitError) as exc_info:
                client._request("GET", "/test")

            assert exc_info.value.retry_after == 60

    def test_network_error(self):
        """Test network error handling."""
        client = StockAlert(api_key="sk_test_key")

        with patch.object(client.session, "request", side_effect=requests.exceptions.Timeout()):
            with pytest.raises(NetworkError) as exc_info:
                client._request("GET", "/test")

            assert "timeout" in str(exc_info.value).lower()

    def test_retry_logic(self):
        """Test retry logic with exponential backoff."""
        client = StockAlert(api_key="sk_test_key", max_retries=2)

        # First two calls fail, third succeeds
        mock_response_fail = Mock()
        mock_response_fail.ok = False
        mock_response_fail.status_code = 500
        mock_response_fail.json.return_value = {"error": "Server error"}

        mock_response_success = Mock()
        mock_response_success.ok = True
        mock_response_success.json.return_value = {"success": True, "data": {}}

        with patch.object(
            client.session,
            "request",
            side_effect=[
                requests.exceptions.ConnectionError("Connection failed"),
                requests.exceptions.ConnectionError("Connection failed"),
                mock_response_success
            ]
        ):
            with patch("time.sleep"):  # Don't actually sleep in tests
                result = client._request("GET", "/test")
                assert result == {}

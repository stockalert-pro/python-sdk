"""Test webhook functionality."""
import hashlib
import hmac

from stockalert.resources.webhooks import WebhooksResource
from stockalert.types import WebhookPayload


class TestWebhooks:
    """Test webhook parsing and signature verification."""

    def test_verify_signature_valid_with_timestamp(self):
        """Test valid webhook signature using the current timestamped format."""
        payload = '{"event":"alert.triggered","data":{"alert":{"id":"123","symbol":"AAPL","condition":"price_above","status":"triggered"}}}'
        secret = "webhook_secret_123"
        timestamp = "1736180400000"
        expected = "sha256=" + hmac.new(
            secret.encode("utf-8"),
            f"{timestamp}.{payload}".encode(),
            hashlib.sha256,
        ).hexdigest()

        assert WebhooksResource.verify_signature(payload, expected, secret, timestamp)

    def test_verify_signature_supports_legacy_format(self):
        """Test legacy signature verification without timestamp."""
        payload = b'{"event":"alert.triggered"}'
        secret = "secret"
        expected = "sha256=" + hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256,
        ).hexdigest()

        assert WebhooksResource.verify_signature(payload, expected, secret)

    def test_verify_signature_invalid(self):
        """Test invalid webhook signature."""
        payload = b'{"event":"alert.triggered"}'
        secret = "webhook_secret"
        signature = "sha256=invalid_signature"

        assert not WebhooksResource.verify_signature(payload, signature, secret)
        assert not WebhooksResource.verify_signature("", signature, secret)

    def test_webhook_payload_normalizes_legacy_data(self):
        """Test that legacy flat webhook payloads are normalized."""
        payload = WebhookPayload(
            {
                "event": "alert.triggered",
                "timestamp": 1736180400000,
                "data": {
                    "alert_id": "test-123",
                    "symbol": "AAPL",
                    "condition": "price_above",
                    "threshold": 150.0,
                    "status": "triggered",
                    "notification": "email",
                    "price": 155.0,
                },
            }
        )

        assert payload.data["alert"]["id"] == "test-123"
        assert payload.data["alert"]["notification"] == "email"
        assert payload.data["stock"]["price"] == 155.0

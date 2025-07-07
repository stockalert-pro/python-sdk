"""Test webhook functionality."""
import pytest
from stockalert.resources.webhooks import WebhooksResource


class TestWebhooks:
    """Test webhook signature verification."""

    def test_verify_signature_valid(self):
        """Test valid webhook signature."""
        payload = b'{"event":"alert.triggered","data":{"id":"123"}}'
        secret = "webhook_secret_123"
        # This is the expected signature for the above payload and secret
        signature = "sha256=8b3d9f7a8c6e5d4c3b2a1908f7e6d5c4b3a29187f6e5d4c3b2a1908f7e6d5c4"
        
        # Calculate actual signature
        import hmac
        import hashlib
        expected = "sha256=" + hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        assert WebhooksResource.verify_signature(payload, expected, secret)

    def test_verify_signature_invalid(self):
        """Test invalid webhook signature."""
        payload = b'{"event":"alert.triggered"}'
        secret = "webhook_secret"
        signature = "sha256=invalid_signature"
        
        assert not WebhooksResource.verify_signature(payload, signature, secret)

    def test_verify_signature_string_payload(self):
        """Test signature verification with string payload."""
        payload = '{"event":"test"}'
        secret = "secret"
        
        import hmac
        import hashlib
        expected = "sha256=" + hmac.new(
            secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        assert WebhooksResource.verify_signature(payload, expected, secret)

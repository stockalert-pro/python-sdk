"""Webhooks resource for StockAlert SDK."""
import hashlib
import hmac
from typing import List, Optional, Union

from ..types import ApiResponse
from .base import BaseResource


class WebhooksResource(BaseResource):
    """Manage webhooks"""

    def list(self) -> ApiResponse:
        """
        List all webhooks

        Returns:
            List of webhooks
        """
        return self._request("GET", "/webhooks")

    def get(self, webhook_id: str) -> ApiResponse:
        """
        Get webhook by ID

        Args:
            webhook_id: Webhook ID

        Returns:
            Webhook details
        """
        return self._request("GET", f"/webhooks/{webhook_id}")

    def create(self, url: str, events: Optional[List[str]] = None) -> ApiResponse:
        """
        Create a new webhook

        Args:
            url: Webhook endpoint URL (HTTPS required)
            events: List of events to subscribe to (default: ["alert.triggered"])

        Returns:
            Created webhook (includes secret, returned only once)
        """
        if events is None:
            events = ["alert.triggered"]

        data = {
            "url": url,
            "events": events
        }

        return self._request("POST", "/webhooks", json_data=data)

    def delete(self, webhook_id: str) -> ApiResponse:
        """
        Delete a webhook

        Args:
            webhook_id: Webhook ID

        Returns:
            Success message
        """
        return self._request("DELETE", f"/webhooks/{webhook_id}")

    def test(self, url: str, secret: str) -> ApiResponse:
        """
        Test a webhook by sending a test payload

        Args:
            url: Webhook URL to test
            secret: Webhook secret for signature

        Returns:
            Test result including destination response
        """
        data = {
            "url": url,
            "secret": secret
        }
        return self._request("POST", "/webhooks/test", json_data=data)

    @staticmethod
    def verify_signature(
        payload: Union[str, bytes],
        signature: str,
        secret: str,
        timestamp: Optional[Union[str, int]] = None,
    ) -> bool:
        """
        Verify webhook signature

        Args:
            payload: Raw webhook payload (JSON string or bytes)
            signature: Signature from X-StockAlert-Signature header
            secret: Your webhook secret

        Returns:
            True if signature is valid

        Example:
            >>> payload = request.body
            >>> signature = request.headers.get("X-StockAlert-Signature")
            >>> if WebhooksResource.verify_signature(payload, signature, secret):
            ...     # Process webhook
        """
        if not payload or not signature or not secret:
            return False

        payload_bytes = payload.encode("utf-8") if isinstance(payload, str) else payload
        payload_text = payload if isinstance(payload, str) else payload.decode("utf-8")

        signing_payload = payload_bytes
        if timestamp not in (None, ""):
            signing_payload = f"{timestamp}.{payload_text}".encode()

        expected_signature = hmac.new(secret.encode("utf-8"), signing_payload, hashlib.sha256).hexdigest()

        # Support both formats: "sha256=..." and raw hex
        if signature.startswith("sha256="):
            signature = signature[7:]  # Remove "sha256=" prefix

        return hmac.compare_digest(signature, expected_signature)

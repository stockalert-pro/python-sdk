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

    def create(self, url: str, events: Optional[List[str]] = None) -> ApiResponse:
        """
        Create a new webhook

        Args:
            url: Webhook endpoint URL
            events: List of events to subscribe to (default: ["alert.triggered"])

        Returns:
            Created webhook
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

    def test(self, webhook_id: str) -> ApiResponse:
        """
        Test a webhook by sending a test payload

        Args:
            webhook_id: Webhook ID

        Returns:
            Test result
        """
        return self._request("POST", f"/webhooks/{webhook_id}/test")

    @staticmethod
    def verify_signature(
        payload: Union[str, bytes],
        signature: str,
        secret: str
    ) -> bool:
        """
        Verify webhook signature

        Args:
            payload: Raw webhook payload
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
        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        expected_signature = hmac.new(
            secret.encode("utf-8"),
            payload,
            hashlib.sha256
        ).hexdigest()

        return signature == f"sha256={expected_signature}"

"""Async user resource for StockAlert SDK."""
from typing import Any, Dict

from ..types import UserSubscription


class AsyncUserResource:
    """Async user resource."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self._config = config
        self.client: Any = None  # Set by AsyncStockAlert

    async def get_subscription(self) -> UserSubscription:
        """Get subscription, quotas, and usage for the authenticated user."""
        response = await self.client._request("GET", "/user/subscription")
        return UserSubscription(response)

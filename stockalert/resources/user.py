"""User resource for StockAlert SDK."""

from ..types import UserSubscription
from .base import BaseResource


class UserResource(BaseResource):
    """User resource."""

    def get_subscription(self) -> UserSubscription:
        """Get subscription, quotas, and usage for the authenticated user."""
        response = self._request("GET", "/user/subscription")
        return UserSubscription(response)

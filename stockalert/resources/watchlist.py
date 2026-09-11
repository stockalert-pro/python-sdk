"""Watchlist resource for StockAlert SDK."""
from typing import Any, Dict, List, Optional, cast

from .base import BaseResource
from .watchlist_base import WatchlistResourceBase


class WatchlistResource(WatchlistResourceBase, BaseResource):
    """Watchlist resource."""

    def list(self) -> List[Dict[str, Any]]:
        """List watchlist items."""
        return cast(List[Dict[str, Any]], self._request("GET", "/watchlist"))

    def create(
        self,
        stock_symbol: str,
        intention: str,
        stock_name: Optional[str] = None,
        target_price: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a stock to the watchlist."""
        return self._request(
            "POST",
            "/watchlist",
            json_data=self._create_payload(
                stock_symbol, intention, stock_name, target_price, notes
            ),
        )

    def update(
        self,
        item_id: str,
        target_price: Optional[float] = None,
        notes: Optional[str] = None,
        is_active: Optional[bool] = None,
        auto_alerts_enabled: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a watchlist item."""
        payload = self._update_payload(
            item_id, target_price, notes, is_active, auto_alerts_enabled
        )
        return self._request("PATCH", f"/watchlist/{item_id}", json_data=payload)

    def delete(self, item_id: str) -> Dict[str, Any]:
        """Remove a watchlist item."""
        self._require_item_id(item_id)
        return self._request("DELETE", f"/watchlist/{item_id}")

    def swap_intention(
        self,
        item_id: str,
        new_intention: str,
        stock_symbol: str,
    ) -> Dict[str, Any]:
        """Swap buy/sell intention and reorder the watchlist."""
        return self._request(
            "PUT",
            "/watchlist/order",
            json_data=self._swap_payload(item_id, new_intention, stock_symbol),
        )

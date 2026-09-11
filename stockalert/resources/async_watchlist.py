"""Async watchlist resource for StockAlert SDK."""
from typing import Any, Dict, List, Optional

from ..exceptions import ValidationError


class AsyncWatchlistResource:
    """Async watchlist resource."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self._config = config
        self.client: Any = None

    async def list(self) -> List[Dict[str, Any]]:
        """List watchlist items."""
        return await self.client._request("GET", "/watchlist")

    async def create(
        self,
        stock_symbol: str,
        intention: str,
        stock_name: Optional[str] = None,
        target_price: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a stock to the watchlist."""
        if not stock_symbol or not str(stock_symbol).strip():
            raise ValidationError("stock_symbol is required")
        if intention not in ("buy", "sell"):
            raise ValidationError("intention must be either buy or sell")

        payload: Dict[str, Any] = {
            "stock_symbol": str(stock_symbol).strip().upper(),
            "intention": intention,
        }
        if stock_name is not None:
            payload["stock_name"] = stock_name
        if target_price is not None:
            payload["target_price"] = target_price
        if notes is not None:
            payload["notes"] = notes

        return await self.client._request("POST", "/watchlist", json=payload)

    async def update(
        self,
        item_id: str,
        target_price: Optional[float] = None,
        notes: Optional[str] = None,
        is_active: Optional[bool] = None,
        auto_alerts_enabled: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update a watchlist item."""
        if not item_id:
            raise ValidationError("Watchlist item ID is required")

        payload: Dict[str, Any] = {}
        if target_price is not None:
            payload["target_price"] = target_price
        if notes is not None:
            payload["notes"] = notes
        if is_active is not None:
            payload["is_active"] = is_active
        if auto_alerts_enabled is not None:
            payload["auto_alerts_enabled"] = auto_alerts_enabled

        if not payload:
            raise ValidationError("Provide at least one field to update")

        return await self.client._request("PATCH", f"/watchlist/{item_id}", json=payload)

    async def delete(self, item_id: str) -> Dict[str, Any]:
        """Remove a watchlist item."""
        if not item_id:
            raise ValidationError("Watchlist item ID is required")
        return await self.client._request("DELETE", f"/watchlist/{item_id}")

    async def swap_intention(
        self,
        item_id: str,
        new_intention: str,
        stock_symbol: str,
    ) -> Dict[str, Any]:
        """Swap buy/sell intention and reorder the watchlist."""
        if not item_id:
            raise ValidationError("item_id is required")
        if not stock_symbol or not str(stock_symbol).strip():
            raise ValidationError("stock_symbol is required")
        if new_intention not in ("buy", "sell"):
            raise ValidationError("new_intention must be either buy or sell")

        return await self.client._request(
            "PUT",
            "/watchlist/order",
            json={
                "item_id": item_id,
                "new_intention": new_intention,
                "stock_symbol": str(stock_symbol).strip().upper(),
            },
        )

"""Shared watchlist validation and payloads."""
from typing import Any, Dict, Optional

from ..exceptions import ValidationError


class WatchlistResourceBase:
    """Shared watchlist payload helpers."""

    @staticmethod
    def _normalize_symbol(stock_symbol: str, field: str = "stock_symbol") -> str:
        if not stock_symbol or not str(stock_symbol).strip():
            raise ValidationError(f"{field} is required")
        return str(stock_symbol).strip().upper()

    @staticmethod
    def _require_intention(intention: str, field: str = "intention") -> str:
        if intention not in ("buy", "sell"):
            raise ValidationError(f"{field} must be either buy or sell")
        return intention

    @staticmethod
    def _require_item_id(item_id: str, label: str = "Watchlist item ID") -> str:
        if not item_id:
            raise ValidationError(f"{label} is required")
        return item_id

    def _create_payload(
        self,
        stock_symbol: str,
        intention: str,
        stock_name: Optional[str] = None,
        target_price: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "stock_symbol": self._normalize_symbol(stock_symbol),
            "intention": self._require_intention(intention),
        }
        if stock_name is not None:
            payload["stock_name"] = stock_name
        if target_price is not None:
            payload["target_price"] = target_price
        if notes is not None:
            payload["notes"] = notes
        return payload

    def _update_payload(
        self,
        item_id: str,
        target_price: Optional[float] = None,
        notes: Optional[str] = None,
        is_active: Optional[bool] = None,
        auto_alerts_enabled: Optional[bool] = None,
    ) -> Dict[str, Any]:
        self._require_item_id(item_id)
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
        return payload

    def _swap_payload(
        self,
        item_id: str,
        new_intention: str,
        stock_symbol: str,
    ) -> Dict[str, Any]:
        self._require_item_id(item_id, "item_id")
        return {
            "item_id": item_id,
            "new_intention": self._require_intention(new_intention, "new_intention"),
            "stock_symbol": self._normalize_symbol(stock_symbol),
        }

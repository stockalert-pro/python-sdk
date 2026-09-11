"""Stocks resource for StockAlert SDK."""
from typing import Any, Dict, List, Optional

from ..exceptions import ValidationError
from .base import BaseResource


class StocksResource(BaseResource):
    """Stocks resource."""

    def retrieve(self, symbol: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get a stock by symbol."""
        if not symbol or not str(symbol).strip():
            raise ValidationError("Stock symbol is required")

        params = {"fields": ",".join(fields)} if fields else None
        return self._request(
            "GET",
            f"/stocks/{str(symbol).strip().upper()}",
            params=params,
        )

"""Async stocks resource for StockAlert SDK."""
from typing import Any, Dict, List, Optional

from ..exceptions import ValidationError


class AsyncStocksResource:
    """Async stocks resource."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self._config = config
        self.client: Any = None

    async def retrieve(self, symbol: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get a stock by symbol."""
        if not symbol or not str(symbol).strip():
            raise ValidationError("Stock symbol is required")

        params = {"fields": ",".join(fields)} if fields else None
        return await self.client._request(
            "GET",
            f"/stocks/{str(symbol).strip().upper()}",
            params=params,
        )

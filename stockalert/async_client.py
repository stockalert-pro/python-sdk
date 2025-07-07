"""
Async client for StockAlert.pro API

Requires httpx to be installed:
    pip install stockalert[async]
"""

try:
    import httpx
except ImportError:
    raise ImportError(
        "The async client requires httpx. "
        "Install it with: pip install stockalert[async]"
    )

from typing import Optional
from .resources.async_alerts import AsyncAlertsResource
from .resources.async_webhooks import AsyncWebhooksResource
from .resources.async_api_keys import AsyncApiKeysResource
from .exceptions import AuthenticationError

DEFAULT_BASE_URL = "https://stockalert.pro/api/public/v1"
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_MAX_RETRIES = 3


class AsyncStockAlert:
    """
    Async StockAlert.pro API Client
    
    Example:
        >>> async with AsyncStockAlert(api_key="sk_your_api_key") as client:
        ...     alerts = await client.alerts.list()
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ):
        if not api_key:
            raise AuthenticationError("API key is required")
        
        self._config = {
            "api_key": api_key,
            "base_url": base_url.rstrip("/"),
            "timeout": timeout,
            "max_retries": max_retries,
        }
        
        self._client = None
        
        # Initialize resources
        self.alerts = AsyncAlertsResource(self._config, self)
        self.webhooks = AsyncWebhooksResource(self._config, self)
        self.api_keys = AsyncApiKeysResource(self._config, self)
    
    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            headers={
                "X-API-Key": self._config["api_key"],
                "Content-Type": "application/json",
                "User-Agent": "stockalert-python-async/1.0.0",
            },
            timeout=self._config["timeout"],
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    @property
    def client(self) -> httpx.AsyncClient:
        if not self._client:
            raise RuntimeError(
                "AsyncStockAlert must be used as a context manager. "
                "Use: async with AsyncStockAlert(...) as client:"
            )
        return self._client
"""Async client for StockAlert SDK."""
from typing import Any, Optional

# Import httpx at runtime to make it optional
try:
    import httpx
except ImportError as e:
    raise ImportError(
        "The async client requires httpx. "
        "Install it with: pip install stockalert[async]"
    ) from e

from .exceptions import AuthenticationError
from .resources.async_alerts import AsyncAlertsResource
from .resources.async_api_keys import AsyncApiKeysResource
from .resources.async_webhooks import AsyncWebhooksResource

DEFAULT_BASE_URL = "https://stockalert.pro/api/public/v1"
DEFAULT_TIMEOUT = 30


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
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 3,
    ):
        if not api_key:
            raise AuthenticationError("API key is required")

        self._config = {
            "api_key": api_key,
            "base_url": base_url or DEFAULT_BASE_URL,
            "timeout": timeout or DEFAULT_TIMEOUT,
            "max_retries": max_retries,
        }

        self._client: Optional[httpx.AsyncClient] = None

        # Initialize resources
        self.alerts = AsyncAlertsResource(self._config)
        self.webhooks = AsyncWebhooksResource(self._config)
        self.api_keys = AsyncApiKeysResource(self._config)

    async def __aenter__(self) -> "AsyncStockAlert":
        self._client = httpx.AsyncClient(
            base_url=self._config["base_url"],
            timeout=self._config["timeout"],
            headers={
                "Authorization": f"Bearer {self._config['api_key']}",
                "User-Agent": "stockalert-python/1.0.0",
                "Content-Type": "application/json",
            },
        )

        # Set client reference for resources
        self.alerts.client = self
        self.webhooks.client = self
        self.api_keys.client = self

        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        if not self._client:
            raise RuntimeError(
                "Client not initialized. "
                "Use: async with AsyncStockAlert(...) as client:"
            )
        return self._client

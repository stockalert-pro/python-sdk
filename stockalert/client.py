from typing import Optional
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
from .resources.api_keys import ApiKeysResource
from .exceptions import AuthenticationError

DEFAULT_BASE_URL = "https://stockalert.pro/api/public/v1"
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_MAX_RETRIES = 3


class StockAlert:
    """
    StockAlert.pro API Client
    
    Example:
        >>> client = StockAlert(api_key="sk_your_api_key")
        >>> alerts = client.alerts.list()
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
        
        # Initialize resources
        self.alerts = AlertsResource(self._config)
        self.webhooks = WebhooksResource(self._config)
        self.api_keys = ApiKeysResource(self._config)
    
    def set_api_key(self, api_key: str) -> None:
        """Update the API key at runtime"""
        self._config["api_key"] = api_key
    
    @property
    def api_key(self) -> str:
        """Get the current API key (masked)"""
        key = self._config["api_key"]
        if len(key) > 8:
            return f"{key[:4]}...{key[-4:]}"
        return "***"
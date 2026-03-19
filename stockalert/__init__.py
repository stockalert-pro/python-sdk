"""StockAlert Python SDK."""
from typing import Any

from .__version__ import __version__
from .client import StockAlert
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .types import (
    Alert,
    AlertCondition,
    AlertStatus,
    NotificationChannel,
    WebhookPayload,
)


def _build_missing_async_client(import_error: ImportError) -> type[Any]:
    class MissingAsyncStockAlert:
        def __init__(self, *_args, **_kwargs):
            raise ImportError(str(import_error)) from import_error

    MissingAsyncStockAlert.__name__ = "AsyncStockAlert"
    return MissingAsyncStockAlert


AsyncStockAlert: type[Any]

try:
    from .async_client import AsyncStockAlert as ImportedAsyncStockAlert
except ImportError as exc:
    if "requires httpx" not in str(exc):
        raise
    AsyncStockAlert = _build_missing_async_client(exc)
else:
    AsyncStockAlert = ImportedAsyncStockAlert

__all__ = [
    "StockAlert",
    "AsyncStockAlert",
    "StockAlertError",
    "APIError",
    "RateLimitError",
    "AuthenticationError",
    "ValidationError",
    "NetworkError",
    "Alert",
    "AlertCondition",
    "NotificationChannel",
    "AlertStatus",
    "WebhookPayload",
    "__version__",
]

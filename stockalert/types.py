"""Type definitions for StockAlert SDK."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

AlertCondition = Literal[
    "price_above",
    "price_below",
    "price_change_up",
    "price_change_down",
    "new_high",
    "new_low",
    "reminder",
    "daily_reminder",
    "ma_crossover_golden",
    "ma_crossover_death",
    "ma_touch_above",
    "ma_touch_below",
    "volume_change",
    "rsi_limit",
    "pe_ratio_below",
    "pe_ratio_above",
    "forward_pe_below",
    "forward_pe_above",
    "earnings_announcement",
    "dividend_ex_date",
    "dividend_payment",
    "insider_transactions",
]

NotificationChannel = Literal["email", "sms"]
AlertStatus = Literal["active", "paused", "triggered", "inactive"]


def _parse_datetime(value: Any) -> Optional[datetime]:
    if value in (None, ""):
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value) / 1000, tz=timezone.utc)

    if isinstance(value, str):
        trimmed = value.strip()
        if not trimmed:
            return None
        if trimmed.isdigit():
            return datetime.fromtimestamp(int(trimmed) / 1000, tz=timezone.utc)
        return datetime.fromisoformat(trimmed.replace("Z", "+00:00"))

    raise TypeError(f"Unsupported datetime value: {value!r}")


class Alert:
    """Alert object."""

    def __init__(self, data: Dict[str, Any]):
        self.id: str = data["id"]
        self.symbol: str = data["symbol"]
        self.condition: AlertCondition = data["condition"]
        self.threshold: Optional[float] = data.get("threshold")
        self.notification: NotificationChannel = data["notification"]
        self.status: AlertStatus = data["status"]
        self.created_at: datetime = _parse_datetime(data["created_at"])  # type: ignore[assignment]

        triggered_at = data.get("triggered_at") or data.get("updated_at")
        self.triggered_at: Optional[datetime] = _parse_datetime(triggered_at)

        # Backward-compatible aliases used by older consumers.
        self.updated_at: datetime = self.triggered_at or self.created_at
        self.last_triggered: Optional[datetime] = self.triggered_at

        self.initial_price: Optional[float] = data.get("initial_price")
        self.parameters: Optional[Dict[str, Any]] = data.get("parameters")
        self.user_id: Optional[str] = data.get("user_id")
        self.email: Optional[str] = data.get("email")
        self.verified: Optional[bool] = data.get("verified")
        self.verification_token: Optional[str] = data.get("verification_token")
        self.last_evaluated_at: Optional[datetime] = _parse_datetime(data.get("last_evaluated_at"))
        self.last_metric_value: Optional[float] = data.get("last_metric_value")
        self.stock: Optional[Dict[str, Any]] = data.get("stock")

        self._raw_data = data

    def __repr__(self) -> str:
        return f"<Alert {self.id}: {self.symbol} {self.condition}>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self._raw_data


class PaginatedResponse:
    """Paginated response for v1 API."""

    def __init__(self, data: List[Dict[str, Any]], meta: Dict[str, Any]):
        self.data = data
        self.meta = meta

        pagination = meta.get("pagination", {})
        self.page = pagination.get("page", 1)
        self.limit = pagination.get("limit", 50)
        self.total = pagination.get("total", 0)
        self.total_pages = pagination.get("total_pages", pagination.get("totalPages", 0))

        self.offset = (self.page - 1) * self.limit
        self.has_more = self.page < self.total_pages

        self.rate_limit = meta.get("rate_limit", meta.get("rateLimit", {}))


class WebhookPayload:
    """Normalized webhook payload."""

    def __init__(self, data: Dict[str, Any]):
        self.id: Optional[str] = data.get("id")
        self.event: str = data["event"]
        self.timestamp: datetime = _parse_datetime(data["timestamp"])  # type: ignore[assignment]
        self.data: Dict[str, Any] = self._normalize_data(data["data"])
        self._raw_data = {
            "id": self.id,
            "event": self.event,
            "timestamp": data["timestamp"],
            "data": self.data,
        }

    def _normalize_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if "alert" in payload:
            return payload

        alert = {
            "id": payload["alert_id"],
            "symbol": payload["symbol"],
            "condition": payload["condition"],
            "status": payload["status"],
        }

        if "threshold" in payload:
            alert["threshold"] = payload.get("threshold")
        if "notification" in payload:
            alert["notification"] = payload.get("notification")
        if "triggered_at" in payload:
            alert["triggered_at"] = payload.get("triggered_at")
        if "triggered_value" in payload:
            alert["triggered_value"] = payload.get("triggered_value")

        normalized: Dict[str, Any] = {"alert": alert}
        if "price" in payload:
            normalized["stock"] = {
                "symbol": payload["symbol"],
                "price": payload.get("price"),
            }

        return normalized

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self._raw_data


ApiResponse = Dict[str, Any]

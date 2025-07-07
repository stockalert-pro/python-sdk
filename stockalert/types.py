from typing import TypedDict, Literal, Optional, List, Dict, Any, Union
from datetime import datetime

AlertStatus = Literal["active", "paused", "triggered"]
NotificationChannel = Literal["email", "sms"]

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
]


class StockInfo(TypedDict):
    name: str
    last_price: float


class Alert(TypedDict):
    id: str
    symbol: str
    condition: AlertCondition
    threshold: Optional[float]
    notification: NotificationChannel
    status: AlertStatus
    created_at: str
    initial_price: float
    parameters: Optional[Dict[str, Any]]
    stocks: Optional[StockInfo]


class CreateAlertRequest(TypedDict, total=False):
    symbol: str  # required
    condition: AlertCondition  # required
    threshold: Optional[float]
    notification: NotificationChannel
    parameters: Optional[Dict[str, Any]]


class UpdateAlertRequest(TypedDict):
    status: Literal["active", "paused"]


class ListAlertsParams(TypedDict, total=False):
    page: int
    limit: int
    status: AlertStatus
    condition: AlertCondition
    search: str
    sortField: str
    sortDirection: Literal["asc", "desc"]


class Pagination(TypedDict):
    page: int
    limit: int
    total: int
    totalPages: int


class PaginatedResponse(TypedDict):
    success: bool
    data: List[Alert]
    pagination: Pagination


class ApiResponse(TypedDict):
    success: bool
    data: Any


class ApiError(TypedDict):
    success: Literal[False]
    error: str


class Webhook(TypedDict):
    id: str
    url: str
    events: List[str]
    secret: str
    is_active: bool
    created_at: str
    last_triggered_at: Optional[str]
    failure_count: int


class CreateWebhookRequest(TypedDict):
    url: str
    events: List[str]


class WebhookEventData(TypedDict):
    alert_id: str
    symbol: str
    condition: str
    threshold: float
    current_value: float
    triggered_at: str
    reason: str
    parameters: Optional[Dict[str, Any]]


class WebhookPayload(TypedDict):
    event: str
    timestamp: str
    data: WebhookEventData
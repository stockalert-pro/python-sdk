"""Alerts resource for StockAlert SDK."""
from typing import Optional, Dict, Any, List, AsyncGenerator, Generator
from ..types import Alert, AlertCondition, NotificationChannel, AlertStatus, PaginatedResponse
from ..exceptions import ValidationError

class AlertsResource:
    """Alerts resource."""
    
    def __init__(self, client):
        self.client = client
    
    def _validate_create_request(self, data: Dict[str, Any]) -> None:
        """Validate create alert request."""
        # Required fields
        if not data.get("symbol"):
            raise ValidationError("Symbol is required")
        
        if not data.get("condition"):
            raise ValidationError("Condition is required")
        
        # Validate symbol format
        symbol = str(data["symbol"]).strip().upper()
        if not symbol or not symbol.isalpha() or len(symbol) > 5:
            raise ValidationError("Symbol must be 1-5 uppercase letters")
        
        # Normalize symbol
        data["symbol"] = symbol
        
        # Validate notification channel
        if "notification" in data:
            valid_channels = ["email", "sms"]  # NO WhatsApp!
            if data["notification"] not in valid_channels:
                raise ValidationError(f"Notification must be one of: {', '.join(valid_channels)}")
        
        # Validate condition-specific requirements
        self._validate_condition_requirements(data)
    
    def _validate_condition_requirements(self, data: Dict[str, Any]) -> None:
        """Validate condition-specific requirements."""
        condition = data["condition"]
        threshold = data.get("threshold")
        
        # Conditions that require threshold
        requires_threshold = [
            "price_above", "price_below", "price_change_up", "price_change_down",
            "new_high", "new_low", "ma_touch_above", "ma_touch_below",
            "volume_change", "rsi_limit", "pe_ratio_below", "pe_ratio_above",
            "forward_pe_below", "forward_pe_above"
        ]
        
        # Conditions that don't use threshold
        no_threshold = [
            "ma_crossover_golden", "ma_crossover_death", "reminder", "daily_reminder",
            "earnings_announcement", "dividend_ex_date", "dividend_payment"
        ]
        
        if condition in requires_threshold and threshold is None:
            raise ValidationError(f"{condition} requires a threshold value")
        
        if condition in no_threshold and threshold is not None:
            raise ValidationError(f"{condition} does not use a threshold value")
        
        # Specific validations
        if condition in ["ma_touch_above", "ma_touch_below"]:
            if not data.get("parameters", {}).get("ma_period"):
                raise ValidationError(f"{condition} requires ma_period parameter (50 or 200)")
        
        if condition == "rsi_limit" and threshold is not None:
            if not 0 <= threshold <= 100:
                raise ValidationError("RSI threshold must be between 0 and 100")
        
        if condition == "reminder":
            params = data.get("parameters", {})
            if not params.get("reminder_date") or not params.get("reminder_time"):
                raise ValidationError("Reminder alerts require reminder_date and reminder_time")
        
        if condition == "daily_reminder":
            if not data.get("parameters", {}).get("reminder_time"):
                raise ValidationError("Daily reminder alerts require reminder_time")
    
    def list(self, **params) -> PaginatedResponse:
        """List alerts with optional filtering."""
        # Validate params
        if "symbol" in params:
            params["symbol"] = str(params["symbol"]).upper()
        
        response = self.client._request("GET", "/alerts", params=params)
        alerts = [Alert(item) for item in response["data"]]
        return PaginatedResponse(alerts, response["meta"])
    
    def create(self, **data) -> Alert:
        """Create a new alert."""
        # Set default notification to email
        if "notification" not in data:
            data["notification"] = "email"
        
        self._validate_create_request(data)
        response = self.client._request("POST", "/alerts", json=data)
        return Alert(response)
    
    def get(self, alert_id: str) -> Alert:
        """Get alert by ID."""
        if not alert_id:
            raise ValidationError("Alert ID is required")
        
        response = self.client._request("GET", f"/alerts/{alert_id}")
        return Alert(response)
    
    def update(self, alert_id: str, status: AlertStatus) -> Alert:
        """Update alert status."""
        if not alert_id:
            raise ValidationError("Alert ID is required")
        
        if status not in ["active", "paused"]:
            raise ValidationError('Status must be either "active" or "paused"')
        
        response = self.client._request("PUT", f"/alerts/{alert_id}", json={"status": status})
        return Alert(response)
    
    def delete(self, alert_id: str) -> Dict[str, Any]:
        """Delete an alert."""
        if not alert_id:
            raise ValidationError("Alert ID is required")
        
        return self.client._request("DELETE", f"/alerts/{alert_id}")
    
    def iterate(self, **params) -> Generator[Alert, None, None]:
        """Iterate through all alerts with automatic pagination."""
        offset = 0
        limit = min(params.get("limit", 100), 100)
        
        # Remove pagination params from base params
        base_params = {k: v for k, v in params.items() if k not in ["limit", "offset"]}
        
        while True:
            page = self.list(**base_params, limit=limit, offset=offset)
            
            for alert in page.data:
                yield alert
            
            if len(page.data) < limit or not page.has_more:
                break
            
            offset += len(page.data)

class AsyncAlertsResource(AlertsResource):
    """Async alerts resource."""
    
    async def list(self, **params) -> PaginatedResponse:
        """List alerts with optional filtering."""
        if "symbol" in params:
            params["symbol"] = str(params["symbol"]).upper()
        
        response = await self.client._request("GET", "/alerts", params=params)
        alerts = [Alert(item) for item in response["data"]]
        return PaginatedResponse(alerts, response["meta"])
    
    async def create(self, **data) -> Alert:
        """Create a new alert."""
        if "notification" not in data:
            data["notification"] = "email"
        
        self._validate_create_request(data)
        response = await self.client._request("POST", "/alerts", json=data)
        return Alert(response)
    
    async def get(self, alert_id: str) -> Alert:
        """Get alert by ID."""
        if not alert_id:
            raise ValidationError("Alert ID is required")
        
        response = await self.client._request("GET", f"/alerts/{alert_id}")
        return Alert(response)
    
    async def update(self, alert_id: str, status: AlertStatus) -> Alert:
        """Update alert status."""
        if not alert_id:
            raise ValidationError("Alert ID is required")
        
        if status not in ["active", "paused"]:
            raise ValidationError('Status must be either "active" or "paused"')
        
        response = await self.client._request("PUT", f"/alerts/{alert_id}", json={"status": status})
        return Alert(response)
    
    async def delete(self, alert_id: str) -> Dict[str, Any]:
        """Delete an alert."""
        if not alert_id:
            raise ValidationError("Alert ID is required")
        
        return await self.client._request("DELETE", f"/alerts/{alert_id}")
    
    async def iterate(self, **params) -> AsyncGenerator[Alert, None]:
        """Iterate through all alerts with automatic pagination."""
        offset = 0
        limit = min(params.get("limit", 100), 100)
        
        base_params = {k: v for k, v in params.items() if k not in ["limit", "offset"]}
        
        while True:
            page = await self.list(**base_params, limit=limit, offset=offset)
            
            for alert in page.data:
                yield alert
            
            if len(page.data) < limit or not page.has_more:
                break
            
            offset += len(page.data)

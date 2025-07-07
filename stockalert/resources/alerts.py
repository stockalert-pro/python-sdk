from typing import Dict, Any, Optional, Iterator
from .base import BaseResource
from ..types import (
    Alert,
    CreateAlertRequest,
    UpdateAlertRequest,
    ListAlertsParams,
    PaginatedResponse,
    ApiResponse,
)


class AlertsResource(BaseResource):
    """Manage stock alerts"""
    
    def list(self, **params: Any) -> PaginatedResponse:
        """
        List all alerts
        
        Args:
            page: Page number (default: 1)
            limit: Items per page (default: 10, max: 100)
            status: Filter by status (active, paused, triggered)
            condition: Filter by alert type
            search: Search by symbol
            sortField: Field to sort by
            sortDirection: Sort direction (asc, desc)
        
        Returns:
            Paginated list of alerts
        """
        return self._request("GET", "/alerts", params=params)
    
    def create(
        self,
        symbol: str,
        condition: str,
        threshold: Optional[float] = None,
        notification: str = "email",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> ApiResponse:
        """
        Create a new alert
        
        Args:
            symbol: Stock ticker symbol
            condition: Alert condition (e.g., price_above, price_below)
            threshold: Target value for the alert
            notification: Notification channel (email, sms)
            parameters: Additional alert-specific parameters
        
        Returns:
            Created alert
        """
        data = {
            "symbol": symbol,
            "condition": condition,
            "notification": notification,
        }
        
        if threshold is not None:
            data["threshold"] = threshold
        
        if parameters:
            data["parameters"] = parameters
        
        return self._request("POST", "/alerts", json_data=data)
    
    def get(self, alert_id: str) -> ApiResponse:
        """
        Get a specific alert
        
        Args:
            alert_id: Alert ID
        
        Returns:
            Alert details
        """
        return self._request("GET", f"/alerts/{alert_id}")
    
    def update(self, alert_id: str, status: str) -> ApiResponse:
        """
        Update an alert's status
        
        Args:
            alert_id: Alert ID
            status: New status (active, paused)
        
        Returns:
            Updated alert
        """
        data = {"status": status}
        return self._request("PUT", f"/alerts/{alert_id}", json_data=data)
    
    def delete(self, alert_id: str) -> ApiResponse:
        """
        Delete an alert
        
        Args:
            alert_id: Alert ID
        
        Returns:
            Success message
        """
        return self._request("DELETE", f"/alerts/{alert_id}")
    
    def pause(self, alert_id: str) -> ApiResponse:
        """Pause an alert"""
        return self.update(alert_id, "paused")
    
    def activate(self, alert_id: str) -> ApiResponse:
        """Activate an alert"""
        return self.update(alert_id, "active")
    
    def list_all(self, **params: Any) -> Iterator[Alert]:
        """
        List all alerts with automatic pagination
        
        Yields:
            Alert objects
        """
        page = 1
        while True:
            response = self.list(page=page, **params)
            
            for alert in response["data"]:
                yield alert
            
            if page >= response["pagination"]["totalPages"]:
                break
            
            page += 1
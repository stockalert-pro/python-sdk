"""Test alert type definitions."""
import pytest
from datetime import datetime
from stockalert.types import Alert, PaginatedResponse


class TestAlertTypes:
    """Test alert type classes."""

    def test_paginated_response(self):
        """Test paginated response creation."""
        data = [{"id": "1"}, {"id": "2"}]
        meta = {
            "total": 50,
            "limit": 10,
            "offset": 0,
            "has_more": True
        }
        
        response = PaginatedResponse(data, meta)
        
        assert response.data == data
        assert response.total == 50
        assert response.limit == 10
        assert response.offset == 0
        assert response.has_more is True

    def test_alert_datetime_parsing(self):
        """Test alert datetime parsing."""
        alert_data = {
            "id": "test-123",
            "symbol": "AAPL",
            "condition": "price_above",
            "threshold": 150.0,
            "notification": "email",
            "status": "active",
            "created_at": "2024-01-07T12:00:00Z",
            "updated_at": "2024-01-07T12:00:00Z",
        }
        
        alert = Alert(alert_data)
        
        assert isinstance(alert.created_at, datetime)
        assert isinstance(alert.updated_at, datetime)
        assert alert.created_at.year == 2024
        assert alert.created_at.month == 1
        assert alert.created_at.day == 7

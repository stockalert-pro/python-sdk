class StockAlertError(Exception):
    """Base exception for StockAlert SDK"""
    
    def __init__(self, message: str, status_code: int = None, code: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code


class AuthenticationError(StockAlertError):
    """Invalid API key or authentication failure"""
    
    def __init__(self, message: str = "Invalid API key"):
        super().__init__(message, 401, "authentication_error")


class RateLimitError(StockAlertError):
    """Rate limit exceeded"""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        limit: int = None,
        remaining: int = None,
        reset: int = None
    ):
        super().__init__(message, 429, "rate_limit_error")
        self.limit = limit
        self.remaining = remaining
        self.reset = reset


class ValidationError(StockAlertError):
    """Invalid request data"""
    
    def __init__(self, message: str, errors: dict = None):
        super().__init__(message, 400, "validation_error")
        self.errors = errors or {}


class NotFoundError(StockAlertError):
    """Resource not found"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404, "not_found")


class NetworkError(StockAlertError):
    """Network request failed"""
    
    def __init__(self, message: str = "Network request failed", original_error: Exception = None):
        super().__init__(message, None, "network_error")
        self.original_error = original_error
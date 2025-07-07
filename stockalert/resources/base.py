import time
import json
from typing import Dict, Any, Optional, Union
from urllib.parse import urlencode
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..exceptions import (
    StockAlertError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    NetworkError,
)


class BaseResource:
    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=self._config["max_retries"],
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            "X-API-Key": self._config["api_key"],
            "Content-Type": "application/json",
            "User-Agent": "stockalert-python/1.0.0",
        })
        
        return session
    
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        url = f"{self._config['base_url']}{path}"
        
        # Clean up params
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self._config["timeout"],
                **kwargs
            )
            
            # Handle rate limit headers
            rate_limit_info = {
                "limit": int(response.headers.get("X-RateLimit-Limit", 0)),
                "remaining": int(response.headers.get("X-RateLimit-Remaining", 0)),
                "reset": int(response.headers.get("X-RateLimit-Reset", 0)),
            }
            
            # Check for errors
            if not response.ok:
                self._handle_error(response, rate_limit_info)
            
            return response.json()
            
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError("Connection failed")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {str(e)}")
    
    def _handle_error(self, response: requests.Response, rate_limit_info: Dict[str, int]):
        try:
            error_data = response.json()
            error_message = error_data.get("error", response.reason)
        except:
            error_message = response.reason or f"HTTP {response.status_code}"
        
        if response.status_code == 401:
            raise AuthenticationError(error_message)
        elif response.status_code == 404:
            raise NotFoundError(error_message)
        elif response.status_code == 429:
            raise RateLimitError(
                error_message,
                limit=rate_limit_info["limit"],
                remaining=rate_limit_info["remaining"],
                reset=rate_limit_info["reset"]
            )
        elif response.status_code == 400:
            errors = error_data.get("errors") if "error_data" in locals() else None
            raise ValidationError(error_message, errors=errors)
        else:
            raise StockAlertError(error_message, status_code=response.status_code)
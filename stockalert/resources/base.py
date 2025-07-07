"""Base resource class for StockAlert SDK."""
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)


class BaseResource:
    """Base class for all API resources."""

    def __init__(self, config: Dict[str, Any]):
        self._config = config
        self._session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()

        # Configure retries
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            "X-API-Key": self._config['api_key'],
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
        **kwargs: Any
    ) -> Dict[str, Any]:
        # Ensure proper URL construction
        base_url = str(self._config['base_url']).rstrip("/")
        path = path.lstrip("/")
        url = f"{base_url}/{path}"

        # Clean up params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self._config.get("timeout", 30),
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

            return response.json()  # type: ignore[no-any-return]

        except requests.exceptions.Timeout as e:
            raise NetworkError("Request timed out") from e
        except requests.exceptions.ConnectionError as e:
            raise NetworkError("Connection failed") from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {str(e)}") from e

    def _handle_error(self, response: requests.Response, rate_limit_info: Dict[str, int]) -> None:
        try:
            error_data = response.json()
            error_message = error_data.get("error", response.reason)
        except Exception:
            error_message = response.reason or f"HTTP {response.status_code}"
            error_data = {}

        if response.status_code == 401:
            raise AuthenticationError(error_message)
        elif response.status_code == 404:
            raise NotFoundError(error_message)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                error_message,
                retry_after=int(retry_after) if retry_after else None
            )
        elif response.status_code == 422:
            # Include validation errors in the message if available
            validation_errors = error_data.get("errors", [])
            if validation_errors:
                error_message = f"{error_message}: {', '.join(validation_errors)}"
            raise ValidationError(error_message)
        else:
            raise StockAlertError(error_message)

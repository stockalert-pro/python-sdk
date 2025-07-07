"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
import time
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
from typing import Optional, Dict, Any
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
import requests
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
from urllib.parse import urljoin
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
from .exceptions import (
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
    StockAlertError,
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
    APIError,
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
    RateLimitError,
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
    AuthenticationError,
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
    ValidationError,
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
    NetworkError
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
)
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
from .resources.alerts import AlertsResource
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
from .resources.webhooks import WebhooksResource
"""StockAlert Python SDK Client."""
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .__version__ import __version__
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    StockAlertError,
    ValidationError,
)
from .resources.alerts import AlertsResource
from .resources.webhooks import WebhooksResource
from .__version__ import __version__

class StockAlert:
    """StockAlert API client."""
    
    DEFAULT_BASE_URL = "https://stockalert.pro/api/public/v1"
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        debug: bool = False
    ):
        """Initialize StockAlert client."""
        if not api_key:
            raise ValidationError("API key is required")
        
        if not api_key.startswith("sk_") or len(api_key) < 10:
            raise ValidationError("Invalid API key format")
        
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.max_retries = max_retries or self.DEFAULT_MAX_RETRIES
        self.debug = debug
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "User-Agent": f"stockalert-python/{__version__}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        # Initialize resources
        self.alerts = AlertsResource(self)
        self.webhooks = WebhooksResource(self)
        
        # Rate limit tracking
        self._rate_limit_reset: Dict[str, float] = {}
    
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retries."""
        url = urljoin(self.base_url, path)
        timeout = timeout or self.timeout
        
        # Check rate limit
        if url in self._rate_limit_reset:
            wait_time = self._rate_limit_reset[url] - time.time()
            if wait_time > 0:
                raise RateLimitError(
                    f"Rate limit in effect. Please wait {int(wait_time)} seconds.",
                    retry_after=int(wait_time)
                )
        
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if self.debug and attempt > 0:
                    print(f"[StockAlert SDK] Retry attempt {attempt}/{self.max_retries}")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    timeout=timeout
                )
                
                # Handle rate limits
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    self._rate_limit_reset[url] = time.time() + retry_after
                    
                    data = response.json()
                    raise RateLimitError(
                        data.get("error", "Rate limit exceeded"),
                        retry_after=retry_after
                    )
                
                # Parse response
                try:
                    data = response.json()
                except ValueError:
                    raise APIError(f"Invalid JSON response: {response.text}", response.status_code)
                
                # Handle errors
                if response.status_code == 401:
                    raise AuthenticationError(data.get("error", "Authentication failed"))
                
                if not response.ok:
                    raise APIError(
                        data.get("error", f"HTTP {response.status_code} error"),
                        response.status_code,
                        data
                    )
                
                if not data.get("success", True):
                    raise APIError(
                        data.get("error", "Request failed"),
                        response.status_code,
                        data
                    )
                
                # Return data directly for single objects, or full response for lists
                if "data" in data and "meta" not in data:
                    return data["data"]
                return data
                
            except requests.exceptions.Timeout:
                last_error = NetworkError("Request timeout")
            except requests.exceptions.ConnectionError:
                last_error = NetworkError("Connection failed")
            except (RateLimitError, AuthenticationError):
                raise  # Don't retry these
            except APIError as e:
                if 400 <= e.status_code < 500 and e.status_code != 429:
                    raise  # Don't retry client errors
                last_error = e
            
            # Retry with exponential backoff
            if attempt < self.max_retries:
                delay = min(2 ** attempt, 10)
                if isinstance(last_error, RateLimitError) and last_error.retry_after:
                    delay = last_error.retry_after
                
                time.sleep(delay)
        
        raise last_error or StockAlertError("Request failed after retries")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

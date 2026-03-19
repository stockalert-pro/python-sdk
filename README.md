# StockAlert.pro Python SDK

Official Python SDK for the StockAlert.pro API.

## Installation

```bash
pip install stockalert
```

Install the optional async dependencies when you want to use `AsyncStockAlert`:

```bash
pip install "stockalert[async]"
```

## Quick Start

```python
from stockalert import StockAlert

# Initialize the client
client = StockAlert(api_key="sk_your_api_key")

# List all alerts
alerts = client.alerts.list()
print(f"Found {len(alerts.data)} alerts")

# Inspect subscription, quotas and usage
subscription = client.user.get_subscription()
print(subscription.account_type, subscription.alerts["quota"]["remaining"])

# Create a new alert
alert = client.alerts.create(
    symbol="AAPL",
    condition="price_above",
    threshold=200,
    notification="email"
)

# Pause alert
client.alerts.pause(alert.id)

# Delete alert
client.alerts.delete(alert.id)
```

## Features

- 🐍 Python 3.8+ support
- 🔄 Automatic retries with exponential backoff
- 🛡️ Type hints for better IDE support
- 📦 Minimal dependencies
- 🧪 Comprehensive test suite
- 📚 Detailed documentation

## Async Support

The SDK also supports async operations:

```python
import asyncio
from stockalert import AsyncStockAlert

async def main():
    async with AsyncStockAlert(api_key="sk_your_api_key") as client:
        alerts = await client.alerts.list()
        print(f"Found {len(alerts.data)} alerts")

asyncio.run(main())
```

## Documentation

Full documentation is available at [https://stockalert.pro/api/docs](https://stockalert.pro/api/docs)

## License

MIT
## 🎯 More Examples

### Pagination
```python
# Iterate through all alerts efficiently
for alert in client.alerts.iterate():
    print(f"{alert.symbol}: {alert.condition}")
```

### Error Handling
```python
from stockalert import StockAlert, APIError, RateLimitError

try:
    alert = client.alerts.create(
        symbol="AAPL",
        condition="price_above",
        threshold=200
    )
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except APIError as e:
    print(f"API error: {e.message} (status: {e.status_code})")
```

### Environment Variables
```python
import os
from stockalert import StockAlert

# API key from environment variable
client = StockAlert(api_key=os.environ["STOCKALERT_API_KEY"])
```

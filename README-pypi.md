# StockAlert.pro Python SDK

Official SDK for the StockAlert.pro API.

## Installation

```bash
pip install stockalert
```

## Quick Start

```python
from stockalert import StockAlert

client = StockAlert(api_key="sk_your_api_key")

# Create alert
alert = client.alerts.create(
    symbol="AAPL",
    condition="price_above",
    threshold=200
)

# Read subscription details
subscription = client.user.get_subscription()
print(alert.id, subscription.account_type)
```

## Documentation

Full documentation: [https://stockalert.pro/api/docs](https://stockalert.pro/api/docs)

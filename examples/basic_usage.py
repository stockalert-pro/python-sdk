#!/usr/bin/env python3
"""
Basic usage example for StockAlert.pro Python SDK
"""

import os

from stockalert import StockAlert


def main():
    # Initialize the client
    client = StockAlert(
        api_key=os.environ.get("STOCKALERT_API_KEY", "sk_your_api_key")
    )

    try:
        # List all active alerts
        print("📋 Listing active alerts...")
        response = client.alerts.list(status="active")
        print(f"Found {len(response.data)} active alerts")

        for alert in response.data:
            print(f"  - {alert.symbol}: {alert.condition} at ${alert.threshold}")

        # Inspect plan and quotas
        subscription = client.user.get_subscription()
        print(f"\n💳 Account: {subscription.account_type} ({subscription.status})")

        # Create a new alert
        print("\n🚨 Creating new alert...")
        new_alert = client.alerts.create(
            symbol="AAPL",
            condition="price_above",
            threshold=200,
            notification="email"
        )
        alert_id = new_alert.id
        print(f"Created alert {alert_id} for {new_alert.symbol}")

        # Get alert details
        print("\n📖 Getting alert details...")
        alert_details = client.alerts.get(alert_id)
        print(f"Alert status: {alert_details.status}")

        # Pause the alert
        print("\n⏸️  Pausing alert...")
        client.alerts.pause(alert_id)
        print("Alert paused")

        # Reactivate the alert
        print("\n▶️  Reactivating alert...")
        client.alerts.activate(alert_id)
        print("Alert reactivated")

        # Delete the alert
        print("\n🗑️  Deleting alert...")
        client.alerts.delete(alert_id)
        print("Alert deleted")

        # Iterate through all alerts (with automatic pagination)
        print("\n📚 Iterating through all alerts...")
        count = 0
        for alert in client.alerts.iterate():
            count += 1
            if count > 5:  # Limit output
                print("  ...")
                break
            print(f"  - {alert.symbol}: {alert.condition}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

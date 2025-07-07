#!/usr/bin/env python3
"""
Example webhook handler for StockAlert.pro
"""

import json
import os

from flask import Flask, abort, request

from stockalert import WebhooksResource

app = Flask(__name__)

# Your webhook secret from StockAlert.pro
WEBHOOK_SECRET = os.environ.get("STOCKALERT_WEBHOOK_SECRET", "your_webhook_secret")


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    # Get the raw body for signature verification
    raw_body = request.get_data()

    # Get signature from headers
    signature = request.headers.get("X-StockAlert-Signature")
    if not signature:
        abort(401, "Missing signature")

    # Verify signature
    if not WebhooksResource.verify_signature(raw_body, signature, WEBHOOK_SECRET):
        abort(401, "Invalid signature")

    # Parse the payload
    try:
        payload = request.json
    except json.JSONDecodeError:
        abort(400, "Invalid JSON")

    # Handle different event types
    event_type = payload.get("event")

    if event_type == "alert.triggered":
        handle_alert_triggered(payload["data"])
    else:
        print(f"Unknown event type: {event_type}")

    # Always return 200 OK
    return "", 200


def handle_alert_triggered(data):
    """Handle alert triggered event"""
    print("🚨 Alert Triggered!")
    print(f"Symbol: {data['symbol']}")
    print(f"Condition: {data['condition']} at ${data['threshold']}")
    print(f"Current: ${data['current_value']}")
    print(f"Reason: {data['reason']}")

    # Your custom logic here
    # e.g., send notification, execute trade, update database, etc.


if __name__ == "__main__":
    # For development only
    # In production, use a proper WSGI server like Gunicorn
    app.run(host="0.0.0.0", port=3000, debug=True)

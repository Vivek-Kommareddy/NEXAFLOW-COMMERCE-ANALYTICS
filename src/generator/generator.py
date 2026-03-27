"""
NexaFlow Order Event Generator
--------------------------------
Simulates 200 realistic e-commerce orders against the API Gateway endpoint.
Every 25th order is injected as a high-value anomaly (amount > $1500).

Usage:
    pip install requests
    python3 generator.py
"""

import random
import requests
import time
from datetime import datetime, timezone

# ── Configuration ─────────────────────────────────────────────────────────────
API_URL = "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/orders"

CATEGORIES = ["electronics", "fashion", "home", "books", "beauty"]
PAYMENTS = ["card", "wallet", "upi", "gift_card"]
REGIONS = ["us-east-1", "us-west-2", "eu-west-1"]

TOTAL_ORDERS = 200
DELAY_SECONDS = 0.2


def generate_order(i: int) -> dict:
    """Generate a single order event. Injects anomalies every 25 orders."""
    amount = round(random.uniform(10, 500), 2)
    if i % 25 == 0:
        amount = round(random.uniform(1500, 3500), 2)  # high-value anomaly

    return {
        "order_id": f"ORD-{1000 + i}",
        "customer_id": f"CUST-{random.randint(100, 999)}",
        "product_id": f"PROD-{random.randint(1, 50)}",
        "category": random.choice(CATEGORIES),
        "amount": amount,
        "payment_method": random.choice(PAYMENTS),
        "event_time": datetime.now(timezone.utc).isoformat(),
        "region": random.choice(REGIONS),
    }


def main():
    print(f"Sending {TOTAL_ORDERS} orders to {API_URL}\n")

    success = 0
    failed = 0

    for i in range(TOTAL_ORDERS):
        payload = generate_order(i)
        anomaly_flag = " [ANOMALY]" if i % 25 == 0 else ""

        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            status = "OK" if response.status_code == 200 else f"ERR {response.status_code}"
            print(f"[{i+1:03d}] {status} | amount=${payload['amount']:>8.2f}{anomaly_flag}")

            if response.status_code == 200:
                success += 1
            else:
                failed += 1
                print(f"       Response: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"[{i+1:03d}] FAILED — {e}")
            failed += 1

        time.sleep(DELAY_SECONDS)

    print(f"\nDone. {success} succeeded, {failed} failed.")
    print("Wait ~60 seconds for Firehose to flush records to S3.")


if __name__ == "__main__":
    main()

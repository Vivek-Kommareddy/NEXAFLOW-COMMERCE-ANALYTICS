import boto3
import json
import os
from datetime import datetime, timezone

s3 = boto3.client("s3")

BUCKET = os.environ["SOURCE_BUCKET"]
SOURCE_PREFIX = os.environ["SOURCE_PREFIX"]
ALERT_PREFIX = os.environ["ALERT_PREFIX"]


def lambda_handler(event, context):
    """
    Scheduled anomaly detector — runs every 30 minutes via EventBridge Scheduler.
    Scans processed Parquet partitions in S3 and writes alert records.
    Alerts are queryable in Athena after the alerts Glue crawler runs.
    """
    objects = s3.list_objects_v2(Bucket=BUCKET, Prefix=SOURCE_PREFIX)
    alerts = []

    for item in objects.get("Contents", []):
        key = item["Key"]
        if not key.endswith(".parquet"):
            continue

        alerts.append({
            "alert_type": "PIPELINE_HEALTH_CHECK",
            "source_key": key,
            "detected_at": datetime.now(timezone.utc).isoformat()
        })

    if alerts:
        alert_key = (
            f"{ALERT_PREFIX}alerts_"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
        )
        body = "\n".join(json.dumps(a) for a in alerts)
        s3.put_object(Bucket=BUCKET, Key=alert_key, Body=body.encode("utf-8"))

    return {"alerts_written": len(alerts)}

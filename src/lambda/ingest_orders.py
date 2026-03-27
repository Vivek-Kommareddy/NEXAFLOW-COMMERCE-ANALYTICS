import json
import os
from datetime import datetime, timezone
import boto3

firehose = boto3.client("firehose")
STREAM_NAME = os.environ["FIREHOSE_STREAM_NAME"]


def lambda_handler(event, context):
    """
    Receives order events from API Gateway (Lambda proxy integration),
    enriches with ingestion timestamp, and publishes to Firehose.
    """
    try:
        body = event.get("body", "{}")
        if isinstance(body, str):
            payload = json.loads(body)
        else:
            payload = body

        payload["ingestion_timestamp"] = datetime.now(timezone.utc).isoformat()

        record = json.dumps(payload) + "\n"

        firehose.put_record(
            DeliveryStreamName=STREAM_NAME,
            Record={"Data": record.encode("utf-8")}
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Order ingested successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }

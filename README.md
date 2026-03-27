# ⚡ NexaFlow — Real-Time E-Commerce Analytics & Anomaly Detection Platform

> **End-to-end serverless data engineering pipeline on AWS** — from raw API events to interactive BI dashboards, with automated anomaly monitoring.

[![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-ETL-E25A1C?style=flat-square&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 🏗️ Architecture Overview

```
                        ┌─────────────────────────────────────────────────────────┐
                        │                  AWS Cloud (us-east-1)                   │
                        │                                                           │
  ┌──────────┐  POST    │  ┌─────────────┐   ┌──────────┐   ┌──────────────────┐  │
  │  Client  │─────────▶│  │ API Gateway │──▶│  Lambda  │──▶│  Data Firehose   │  │
  │ /orders  │          │  │  HTTP API   │   │  Ingest  │   │  (Buffer + Batch) │  │
  └──────────┘          │  └─────────────┘   └──────────┘   └────────┬─────────┘  │
                        │                                             │             │
                        │          ┌──────────────────────────────────▼──────────┐ │
                        │          │              Amazon S3 (Data Lake)           │ │
                        │          │  raw/orders/  │  processed/orders/  │alerts/ │ │
                        │          └───────┬────────────────┬───────────────┬────┘ │
                        │                  │                │               │       │
                        │           ┌──────▼──────┐  ┌─────▼─────┐        │       │
                        │           │ Glue Crawler│  │ Glue ETL  │        │       │
                        │           │  (Schema)   │  │  (Spark)  │        │       │
                        │           └──────┬──────┘  └─────┬─────┘        │       │
                        │                  │                │               │       │
                        │           ┌──────▼────────────────▼─────┐        │       │
                        │           │       AWS Glue Data Catalog  │        │       │
                        │           └──────────────┬──────────────┘        │       │
                        │                          │                        │       │
                        │                   ┌──────▼──────┐         ┌──────▼────┐  │
                        │                   │   Athena    │         │  Lambda   │  │
                        │                   │  (SQL on S3)│         │ Anomaly   │  │
                        │                   └──────┬──────┘         └─────▲─────┘  │
                        │                          │                       │        │
                        │                   ┌──────▼──────┐    ┌──────────┴──────┐ │
                        │                   │ QuickSight  │    │ EventBridge     │ │
                        │                   │  Dashboards │    │   Scheduler     │ │
                        │                   └─────────────┘    └─────────────────┘ │
                        └─────────────────────────────────────────────────────────┘
```

---

## 🎯 What This Platform Does

NexaFlow ingests real-time e-commerce order events, transforms them through a multi-stage serverless pipeline, and surfaces business intelligence and anomaly alerts — all without managing any servers.

| Stage | Service | Role |
|-------|---------|------|
| **Ingestion** | API Gateway + Lambda | Receives HTTP POST orders, validates, publishes to stream |
| **Streaming** | Amazon Data Firehose | Buffers and delivers records to S3 raw zone |
| **Storage** | Amazon S3 | Tiered data lake: raw → processed → alerts |
| **Cataloging** | AWS Glue Crawlers | Auto-discovers schema, populates Data Catalog |
| **Transformation** | AWS Glue ETL (Spark) | JSON → Parquet, partitioned by date, enriched |
| **Analytics** | Amazon Athena | Serverless SQL queries over S3-backed tables |
| **Visualization** | Amazon QuickSight | Interactive BI dashboards from Athena datasets |
| **Monitoring** | Lambda + EventBridge | Scheduled anomaly detection, alert files to S3 |

---

## 📁 Repository Structure

```
nexaflow-commerce-analytics/
│
├── src/
│   ├── lambda/
│   │   ├── ingest_orders.py          # API Gateway → Firehose Lambda
│   │   └── detect_anomalies.py       # Scheduled anomaly detection Lambda
│   ├── glue/
│   │   └── glue_etl_orders.py        # PySpark ETL: JSON → Parquet
│   └── generator/
│       └── generator.py              # Local order event simulator
│
├── infrastructure/
│   └── iam-policies/
│       ├── lambda-ingest-inline.json         # Firehose PutRecord permissions
│       ├── firehose-delivery-inline.json     # S3 delivery permissions
│       ├── glue-service-inline.json          # S3 read/write for Glue
│       └── scheduler-invoke-inline.json      # Lambda invoke permissions
│
├── docs/
│   └── execution-guide.docx          # Screenshot-annotated execution walkthrough
│
├── scripts/
│   └── athena_queries.sql            # All demo Athena queries
│
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- AWS account with admin access
- Python 3.x + `pip install requests`
- AWS CLI configured (optional, console-based setup)

### 1. Clone the repo

```bash
git clone https://github.com/vivek-kommareddy/nexaflow-commerce-analytics.git
cd nexaflow-commerce-analytics
```

### 2. Follow the setup phases

The platform is built entirely in the AWS Console. Full step-by-step instructions are in [`docs/execution-guide.docx`](docs/execution-guide.docx).

**High-level build order:**

```
Phase 1  →  Create S3 bucket + folder structure
Phase 2  →  Create 4 IAM roles (Lambda, Firehose, Glue, Scheduler)
Phase 3  →  Create Firehose delivery stream
Phase 4  →  Deploy ingest Lambda (src/lambda/ingest_orders.py)
Phase 5  →  Create API Gateway HTTP API with Lambda integration
Phase 6  →  Test with a single curl command
Phase 7  →  Run the order generator (src/generator/generator.py)
Phase 8  →  Create Glue database + raw crawler
Phase 9  →  Upload and run Glue ETL job (src/glue/glue_etl_orders.py)
Phase 10 →  Create processed-data crawler
Phase 11 →  Configure Athena + run demo queries
Phase 12 →  Deploy anomaly Lambda + EventBridge Scheduler
Phase 13 →  Connect QuickSight to Athena
```

### 3. Send a test event

```bash
curl -X POST "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD-1001",
    "customer_id": "CUST-501",
    "product_id": "PROD-19",
    "category": "electronics",
    "amount": 249.99,
    "payment_method": "card",
    "event_time": "2026-03-26T14:30:00Z",
    "region": "us-east-1"
  }'
```

### 4. Generate bulk test data

```bash
# Edit API_URL in the script first
python3 src/generator/generator.py
# Sends 200 orders with realistic distributions + injected high-value anomalies
```

---

## 📊 Athena Demo Queries

All queries are in [`scripts/athena_queries.sql`](scripts/athena_queries.sql).

```sql
-- Daily revenue trend
SELECT event_date, SUM(amount) AS daily_revenue
FROM commerce_analytics.processed_orders
GROUP BY event_date ORDER BY event_date;

-- Category performance
SELECT category, COUNT(*) AS total_orders, SUM(amount) AS revenue
FROM commerce_analytics.processed_orders
GROUP BY category ORDER BY revenue DESC;

-- High-value order detection
SELECT event_date, COUNT(*) AS high_value_orders
FROM commerce_analytics.processed_orders
WHERE is_high_value = 1
GROUP BY event_date ORDER BY event_date;

-- Hourly order volume patterns
SELECT event_hour, AVG(amount) AS avg_order_value
FROM commerce_analytics.processed_orders
GROUP BY event_hour ORDER BY event_hour;
```

---

## 🧱 Infrastructure & IAM

All IAM policies are documented in [`infrastructure/iam-policies/`](infrastructure/iam-policies/).

| Role | Purpose | Key Permissions |
|------|---------|----------------|
| `role-commerce-lambda-ingest` | Ingest Lambda execution | `firehose:PutRecord`, CloudWatch Logs |
| `role-commerce-firehose-delivery` | Firehose → S3 | `s3:PutObject` on bucket |
| `role-commerce-glue-service` | Glue crawlers + ETL | S3 read/write, Data Catalog access |
| `role-commerce-scheduler-invoke-lambda` | EventBridge → Lambda | `lambda:InvokeFunction` |

---

## 🔍 Data Flow Detail

```
Order Event (JSON)
    │
    ▼
API Gateway HTTP POST /orders
    │
    ▼
Lambda: ingest_orders.py
  - Parses request body
  - Adds ingestion_timestamp
  - Calls firehose.put_record()
    │
    ▼
Amazon Data Firehose (buffered, ~60s)
  - Batches records
  - Delivers to S3 with newline delimiters
    │
    ▼
S3: raw/orders/YYYY/MM/DD/HH/*.json.gz
    │
    ▼
Glue Crawler: crawler_raw_orders
  - Infers schema
  - Creates table in commerce_analytics DB
    │
    ▼
Glue ETL Job: job_process_orders (PySpark)
  - Reads raw JSON
  - Drops nulls on order_id, customer_id, amount
  - Parses timestamps → event_date, event_hour
  - Flags is_high_value (amount >= $1000)
  - Writes Parquet, partitioned by event_date
    │
    ▼
S3: processed/orders/event_date=YYYY-MM-DD/*.parquet
    │
    ▼
Glue Crawler: crawler_processed_orders
  - Registers Parquet schema + partitions
    │
    ▼
Athena → QuickSight
```

---

## 🚨 Anomaly Detection

The `detect_anomalies` Lambda runs every 30 minutes via EventBridge Scheduler.

It scans processed order partitions and writes structured alert records to `s3://bucket/alerts/`.

Alerts are queryable via Athena after the alerts crawler runs:

```sql
SELECT * FROM commerce_analytics.alerts LIMIT 20;
```

**Designed to extend:** The anomaly logic can be upgraded to use statistical thresholds (Z-score, IQR) on the processed Parquet data as a next iteration.

---

## 💼 Skills Demonstrated

| Domain | Skills |
|--------|--------|
| **Cloud Architecture** | Serverless event-driven design, IAM least-privilege, multi-tier S3 data lake |
| **Data Engineering** | Streaming ingestion (Firehose), ETL with PySpark (Glue), schema management (Data Catalog) |
| **Analytics** | Partitioned Parquet, Athena query optimization, columnar storage |
| **BI & Reporting** | QuickSight dataset creation, Athena-backed dashboards |
| **DevOps** | Scheduled jobs (EventBridge), Lambda deployment, CloudWatch logging |

---

## 🧹 Cleanup (Avoid Ongoing Costs)

After demo — delete or disable:

1. **Firehose stream** — per GB charges
2. **Glue ETL jobs** — per DPU-hour when running
3. **QuickSight** — monthly subscription if not needed
4. **EventBridge schedule** — disable to stop Lambda invocations
5. **S3 data** — delete test files to avoid storage costs

Athena, IAM roles, Lambda functions, and Glue crawlers have no idle cost.

---

## 📄 License

MIT — free to use, fork, and build on.

---

*Built on AWS | Serverless | Event-Driven | Real-Time Analytics*

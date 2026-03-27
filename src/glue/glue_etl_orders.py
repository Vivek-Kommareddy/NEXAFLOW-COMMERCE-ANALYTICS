import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_timestamp, to_date, hour, when, lit

args = getResolvedOptions(sys.argv, ["JOB_NAME", "SOURCE_PATH", "TARGET_PATH"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

source_path = args["SOURCE_PATH"]
target_path = args["TARGET_PATH"]

# ── Read raw JSON from S3 ────────────────────────────────────────────────────
df = spark.read.json(source_path)

# ── Transform and enrich ─────────────────────────────────────────────────────
clean_df = (
    df
    .filter(col("order_id").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("amount").isNotNull())
    .withColumn("event_ts", to_timestamp(col("event_time")))
    .withColumn("event_date", to_date(col("event_ts")))
    .withColumn("event_hour", hour(col("event_ts")))
    .withColumn("is_high_value", when(col("amount") >= 1000, lit(1)).otherwise(lit(0)))
)

# ── Write Parquet, partitioned by date ───────────────────────────────────────
(
    clean_df
    .write
    .mode("overwrite")
    .partitionBy("event_date")
    .parquet(target_path)
)

job.commit()

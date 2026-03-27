-- ============================================================
-- NexaFlow Analytics — Athena Demo Queries
-- Database: commerce_analytics
-- ============================================================

-- 1. PREVIEW PROCESSED DATA
-- ─────────────────────────────────────────────────────────────
SELECT *
FROM commerce_analytics.processed_orders
LIMIT 10;


-- 2. DAILY REVENUE TREND
-- ─────────────────────────────────────────────────────────────
SELECT
    event_date,
    SUM(amount)   AS daily_revenue,
    COUNT(*)      AS total_orders
FROM commerce_analytics.processed_orders
GROUP BY event_date
ORDER BY event_date;


-- 3. CATEGORY PERFORMANCE
-- ─────────────────────────────────────────────────────────────
SELECT
    category,
    COUNT(*)        AS total_orders,
    SUM(amount)     AS total_revenue,
    AVG(amount)     AS avg_order_value
FROM commerce_analytics.processed_orders
GROUP BY category
ORDER BY total_revenue DESC;


-- 4. HIGH-VALUE ORDER DETECTION
-- ─────────────────────────────────────────────────────────────
SELECT
    event_date,
    COUNT(*)    AS high_value_orders,
    SUM(amount) AS high_value_revenue
FROM commerce_analytics.processed_orders
WHERE is_high_value = 1
GROUP BY event_date
ORDER BY event_date;


-- 5. HOURLY ORDER VOLUME PATTERN
-- ─────────────────────────────────────────────────────────────
SELECT
    event_hour,
    COUNT(*)    AS total_orders,
    AVG(amount) AS avg_order_value
FROM commerce_analytics.processed_orders
GROUP BY event_hour
ORDER BY event_hour;


-- 6. PAYMENT METHOD BREAKDOWN
-- ─────────────────────────────────────────────────────────────
SELECT
    payment_method,
    COUNT(*)    AS orders,
    SUM(amount) AS revenue,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct_of_orders
FROM commerce_analytics.processed_orders
GROUP BY payment_method
ORDER BY orders DESC;


-- 7. REGION ANALYSIS
-- ─────────────────────────────────────────────────────────────
SELECT
    region,
    COUNT(*)    AS total_orders,
    SUM(amount) AS total_revenue
FROM commerce_analytics.processed_orders
GROUP BY region
ORDER BY total_revenue DESC;


-- 8. TOP PRODUCTS BY REVENUE
-- ─────────────────────────────────────────────────────────────
SELECT
    product_id,
    COUNT(*)    AS orders,
    SUM(amount) AS revenue
FROM commerce_analytics.processed_orders
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;


-- 9. PIPELINE ALERTS
-- ─────────────────────────────────────────────────────────────
SELECT *
FROM commerce_analytics.alerts
ORDER BY detected_at DESC
LIMIT 20;

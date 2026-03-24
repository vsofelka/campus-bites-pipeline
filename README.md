# Campus Bites Pipeline

Local PostgreSQL database for analyzing campus food delivery order data.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

## Quickstart

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd campus-bites-pipeline

# 2. Start the database
docker compose up -d

# 3. Wait ~5 seconds for Postgres to initialize, then connect
docker compose exec db psql -U student -d campus_bites
```

The CSV is loaded automatically on first startup. You should see 1,132 rows in the `orders` table.

## Connection Details

| Setting  | Value         |
|----------|---------------|
| Host     | localhost     |
| Port     | 5432          |
| Database | campus_bites  |
| Username | student       |
| Password | student123    |

## Connecting with a GUI

Use [DBeaver](https://dbeaver.io/) or [TablePlus](https://tableplus.com/) with the connection details above.

## Sample Queries

```sql
-- Preview the data
SELECT * FROM orders LIMIT 10;

-- Count orders by cuisine type
SELECT cuisine_type, COUNT(*) AS total_orders
FROM orders
GROUP BY cuisine_type
ORDER BY total_orders DESC;

-- Average order value by customer segment
SELECT customer_segment, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY customer_segment;

-- Promo code usage rate
SELECT
    COUNT(*) FILTER (WHERE promo_code_used) AS promo_orders,
    COUNT(*) AS total_orders,
    ROUND(100.0 * COUNT(*) FILTER (WHERE promo_code_used) / COUNT(*), 1) AS pct
FROM orders;
```

## Stopping and Starting

```bash
# Stop the container (data is preserved)
docker compose stop

# Start it again
docker compose start

# Stop and delete all data (full reset)
docker compose down -v
```

After a full reset (`down -v`), re-running `docker compose up -d` will reload the CSV from scratch.

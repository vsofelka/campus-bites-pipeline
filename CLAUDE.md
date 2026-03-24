# Campus Bites Pipeline

A local PostgreSQL database for analyzing campus food delivery order data. The database is containerized via Docker and contains 1,132 rows of order data loaded from a CSV file.

## Stack

- **Database**: PostgreSQL 16 (Docker)
- **Data**: `data/campus_bites_orders.csv` (1,132 rows)
- **Schema init**: `init.sql`
- **Orchestration**: `docker-compose.yml`

## Database Connection

| Setting  | Value        |
|----------|--------------|
| Host     | localhost    |
| Port     | 5432         |
| Database | campus_bites |
| Username | student      |
| Password | student123   |

Connection string: `postgresql://student:student123@localhost:5432/campus_bites`

## Schema

Table: `orders`

| Column             | Type           |
|--------------------|----------------|
| order_id           | INTEGER (PK)   |
| order_date         | DATE           |
| order_time         | TIME           |
| customer_segment   | TEXT           |
| order_value        | NUMERIC(10, 2) |
| cuisine_type       | TEXT           |
| delivery_time_mins | INTEGER        |
| promo_code_used    | BOOLEAN        |
| is_reorder         | BOOLEAN        |

## Common Commands

```bash
# Start the database
docker compose up -d

# Connect via psql
docker compose exec db psql -U student -d campus_bites

# Stop (data preserved)
docker compose stop

# Full reset (deletes all data)
docker compose down -v
```

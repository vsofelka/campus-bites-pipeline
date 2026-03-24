-- Create the orders table
CREATE TABLE orders (
    order_id            INTEGER PRIMARY KEY,
    order_date          DATE,
    order_time          TIME,
    customer_segment    TEXT,
    order_value         NUMERIC(10, 2),
    cuisine_type        TEXT,
    delivery_time_mins  INTEGER,
    promo_code_used     BOOLEAN,
    is_reorder          BOOLEAN
);

-- Load CSV into a staging table first (Yes/No need to be converted to BOOLEAN)
CREATE TEMP TABLE orders_staging (
    order_id            INTEGER,
    order_date          DATE,
    order_time          TIME,
    customer_segment    TEXT,
    order_value         NUMERIC(10, 2),
    cuisine_type        TEXT,
    delivery_time_mins  INTEGER,
    promo_code_used     TEXT,
    is_reorder          TEXT
);

\COPY orders_staging FROM '/docker-entrypoint-initdb.d/campus_bites_orders.csv' WITH (FORMAT csv, HEADER true);

-- Insert into final table, converting Yes/No to BOOLEAN
INSERT INTO orders
SELECT
    order_id,
    order_date,
    order_time,
    customer_segment,
    order_value,
    cuisine_type,
    delivery_time_mins,
    (promo_code_used = 'Yes'),
    (is_reorder = 'Yes')
FROM orders_staging;

import pandas as pd
import psycopg2
from psycopg2 import sql

# --- Database connection settings ---
# Matches the credentials defined in docker-compose.yml
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_bites",
    "user": "student",
    "password": "student123",
}

# --- Path to the source CSV file ---
CSV_PATH = "data/campus_bites_orders.csv"

# --- Table definition ---
# Uses CREATE TABLE IF NOT EXISTS so the script is safe to run multiple times
# without failing if the table already exists
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id          INTEGER PRIMARY KEY,
    order_date        DATE,
    order_time        TIME,
    customer_segment  VARCHAR(50),
    order_value       NUMERIC(10, 2),
    cuisine_type      VARCHAR(50),
    delivery_time_mins INTEGER,
    promo_code_used   BOOLEAN,
    is_reorder        BOOLEAN
);
"""

def load_orders():
    # --- Load CSV into a DataFrame ---
    df = pd.read_csv(CSV_PATH)

    # Convert Yes/No text columns to proper Python booleans so they map
    # correctly to PostgreSQL BOOLEAN columns
    df["promo_code_used"] = df["promo_code_used"].str.strip().str.lower() == "yes"
    df["is_reorder"] = df["is_reorder"].str.strip().str.lower() == "yes"

    # --- Connect to the database ---
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # --- Create the table if it doesn't exist ---
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    print("Table 'orders' ready.")

    # --- Insert rows ---
    # ON CONFLICT DO NOTHING skips any row whose order_id already exists,
    # making the script safe to re-run without creating duplicates
    insert_sql = """
        INSERT INTO orders (
            order_id, order_date, order_time, customer_segment,
            order_value, cuisine_type, delivery_time_mins,
            promo_code_used, is_reorder
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING;
    """

    # Convert each DataFrame row to a plain tuple for psycopg2
    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
    cur.executemany(insert_sql, rows)
    conn.commit()

    print(f"Inserted {cur.rowcount} rows (skipped duplicates).")

    # --- Clean up ---
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_orders()

import csv
import psycopg2

DB_URL = "postgresql://student:student123@localhost:5432/campus_bites"
CSV_PATH = "data/campus_bites_orders.csv"


def load_data():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                int(row["order_id"]),
                row["order_date"],
                row["order_time"],
                row["customer_segment"],
                float(row["order_value"]),
                row["cuisine_type"],
                int(row["delivery_time_mins"]),
                row["promo_code_used"] == "Yes",
                row["is_reorder"] == "Yes",
            )
            for row in reader
        ]

    cur.executemany(
        """
        INSERT INTO orders (
            order_id, order_date, order_time, customer_segment, order_value,
            cuisine_type, delivery_time_mins, promo_code_used, is_reorder
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
        """,
        rows,
    )

    conn.commit()
    print(f"Loaded {cur.rowcount} rows into orders table.")
    cur.close()
    conn.close()


if __name__ == "__main__":
    load_data()

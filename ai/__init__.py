import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "app.db"
)


def initialize_database():

    os.makedirs(
        os.path.dirname(DATABASE_PATH),
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            email TEXT
        )
    """)

    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            name TEXT,
            amount REAL,
            order_date TEXT,

            FOREIGN KEY (customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    # Sample customers
    customers = [
        (1, "Vidya", "Pune", "vidyaa@example.com"),
        (2, "Priya", "Mumbai", "priya@example.com"),
        (3, "Akash", "Pune", "akash@example.com"),
        (4, "Durva", "Nashik", "durvaa@example.com"),
        (5, "Rohan", "Pune", "rohan@example.com")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        (customer_id, name, city, email)
        VALUES (?, ?, ?, ?)
    """, customers)

    # Sample orders
    orders = [
        (1, 1, "Vidya", 25000, "2026-01-10"),
        (2, 1, "Vidya", 30000, "2026-02-15"),
        (3, 2, "Priya", 18000, "2026-02-20"),
        (4, 2, "Priya", 22000, "2026-03-12"),
        (5, 3, "Prathmesh", 35000, "2026-03-20"),
        (6, 3, "Akash", 28000, "2026-04-05"),
        (7, 4, "Durva", 15000, "2026-04-12"),
        (8, 5, "Rohan Shah", 42000, "2026-05-18")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, name, amount, order_date)
        VALUES (?, ?, ?, ?, ?)
    """, orders)

    connection.commit()

    # Verify tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    print("\nDatabase initialized successfully!")
    print("Database:", DATABASE_PATH)
    print("Tables:", tables)

    # Count records
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    print("Customers:", customer_count)
    print("Orders:", order_count)

    connection.close()


if __name__ == "__main__":
    initialize_database()
import sqlite3
import os

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            email TEXT
        )
    """)

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

    customers = [
         (1, "Vidya", "Pune", "vidya@example.com"),
         (2, "Swarali", "Mumbai", "swarali@example.com"),
         (3, "Nilesh", "Pune", "nilesh@example.com"),
         (4, "Arjun", "Nashik", "arjun@example.com"),
         (5, "Avishkar", "Pune", "avishkar@example.com")
]

    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        (customer_id, name, city, email)
        VALUES (?, ?, ?, ?)
    """, customers)

    orders = [
       (1, 1, "Vidya", 25000, "2026-01-10"),
       (2, 1, "Vidya", 30000, "2026-02-15"),
       (3, 2, "Swarali", 18000, "2026-02-20"),
       (4, 2, "Swarali", 22000, "2026-03-12"),
       (5, 3, "Nilesh", 35000, "2026-03-20"),
       (6, 3, "Nilesh", 28000, "2026-04-05"),
       (7, 4, "Arjun", 15000, "2026-04-12"),
       (8, 5, "Avishkar", 42000, "2026-05-18")
    ]
   

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, name, amount, order_date)
        VALUES (?, ?, ?, ?, ?)
    """, orders)

    connection.commit()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    print()
    print("=" * 50)
    print("DATABASE INITIALIZED SUCCESSFULLY")
    print("=" * 50)
    print("Database:", DATABASE_PATH)
    print("Tables:", tables)
    print("Customers:", customer_count)
    print("Orders:", order_count)
    print("=" * 50)

    connection.close()


if __name__ == "__main__":
    initialize_database()
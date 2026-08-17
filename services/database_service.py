import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "app.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def execute_query(query):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        if query.strip().lower().startswith(
            ("select", "pragma", "with", "explain")
        ):
            rows = cursor.fetchall()

            result = [dict(row) for row in rows]

            columns = [description[0] for description in cursor.description]

            return {
                "success": True,
                "columns": columns,
                "rows": result
            }

        connection.commit()

        return {
            "success": True,
            "columns": [],
            "rows": [],
            "message": "Query executed successfully."
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }

    finally:
        connection.close()


def get_tables():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        return [row["name"] for row in cursor.fetchall()]

    finally:
        connection.close()


def get_schema():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        tables = get_tables()

        schema = {}

        for table in tables:

            cursor.execute(f'PRAGMA table_info("{table}")')

            columns = []

            for row in cursor.fetchall():
                columns.append({
                    "name": row["name"],
                    "type": row["type"],
                    "primary_key": bool(row["pk"]),
                    "nullable": not bool(row["notnull"])
                })

            schema[table] = columns

        return schema

    finally:
        connection.close()
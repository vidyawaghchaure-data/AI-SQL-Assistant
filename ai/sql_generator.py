import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from services.schema_service import get_schema_text


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(override=True)


# =========================================================
# CLEAN SQL
# =========================================================

def clean_sql(sql):

    if not sql:
        return ""

    sql = sql.strip()

    # Remove Markdown SQL code blocks
    sql = re.sub(
        r"```sql",
        "",
        sql,
        flags=re.IGNORECASE
    )

    sql = sql.replace("```", "")

    # Remove "SQL:" prefix
    sql = re.sub(
        r"^\s*SQL\s*:\s*",
        "",
        sql,
        flags=re.IGNORECASE
    )

    return sql.strip()


# =========================================================
# DEMO MODE SQL GENERATOR
# =========================================================

def generate_with_demo(question, schema):

    q = question.lower().strip()

    # -----------------------------------------------------
    # SHOW ALL CUSTOMERS
    # -----------------------------------------------------

    if (
        ("show" in q or "display" in q or "list" in q)
        and "customer" in q
        and "all" in q
    ):

        return """
SELECT *
FROM customers;
""".strip()

    # -----------------------------------------------------
    # CUSTOMERS FROM PUNE
    # -----------------------------------------------------

    if (
        "customer" in q
        and "pune" in q
    ):

        return """
SELECT *
FROM customers
WHERE city = 'Pune';
""".strip()

    # -----------------------------------------------------
    # SHOW CUSTOMERS
    # -----------------------------------------------------

    if (
        "customer" in q
        and (
            "show" in q
            or "display" in q
            or "list" in q
        )
    ):

        return """
SELECT *
FROM customers;
""".strip()

    # -----------------------------------------------------
    # TOP CUSTOMERS
    # -----------------------------------------------------

    if (
        "customer" in q
        and (
            "top" in q
            or "highest" in q
            or "most" in q
        )
    ):

        return """
SELECT
    customer_id,
    name,
    SUM(amount) AS total_spending
FROM orders
GROUP BY customer_id, name
ORDER BY total_spending DESC
LIMIT 5;
""".strip()

    # -----------------------------------------------------
    # CUSTOMER WITH HIGHEST SPENDING
    # -----------------------------------------------------

    if (
        "customer" in q
        and (
            "spent the most" in q
            or "spends the most" in q
            or "highest spending" in q
            or "maximum spending" in q
        )
    ):

        return """
SELECT
    customer_id,
    name,
    SUM(amount) AS total_spending
FROM orders
GROUP BY customer_id, name
ORDER BY total_spending DESC
LIMIT 1;
""".strip()

    # -----------------------------------------------------
    # TOTAL SALES
    # -----------------------------------------------------

    if (
        ("total" in q or "sum" in q)
        and (
            "sales" in q
            or "amount" in q
            or "revenue" in q
        )
    ):

        return """
SELECT
    SUM(amount) AS total_sales
FROM orders;
""".strip()

    # -----------------------------------------------------
    # AVERAGE ORDER
    # -----------------------------------------------------

    if (
        "average" in q
        and "order" in q
    ):

        return """
SELECT
    AVG(amount) AS average_order_value
FROM orders;
""".strip()

    # -----------------------------------------------------
    # COUNT CUSTOMERS
    # -----------------------------------------------------

    if (
        (
            "count" in q
            or "how many" in q
            or "number of" in q
        )
        and "customer" in q
    ):

        return """
SELECT
    COUNT(*) AS total_customers
FROM customers;
""".strip()

    # -----------------------------------------------------
    # COUNT ORDERS
    # -----------------------------------------------------

    if (
        (
            "count" in q
            or "how many" in q
            or "number of" in q
        )
        and "order" in q
    ):

        return """
SELECT
    COUNT(*) AS total_orders
FROM orders;
""".strip()

    # -----------------------------------------------------
    # TOTAL ORDER AMOUNT
    # -----------------------------------------------------

    if (
        (
            "total" in q
            or "sum" in q
        )
        and "order" in q
    ):

        return """
SELECT
    SUM(amount) AS total_order_amount
FROM orders;
""".strip()

    # -----------------------------------------------------
    # AVERAGE SALES
    # -----------------------------------------------------

    if (
        "average" in q
        and (
            "sales" in q
            or "amount" in q
        )
    ):

        return """
SELECT
    AVG(amount) AS average_amount
FROM orders;
""".strip()

    # -----------------------------------------------------
    # ALL ORDERS
    # -----------------------------------------------------

    if (
        (
            "all" in q
            or "show" in q
            or "display" in q
            or "list" in q
        )
        and "order" in q
    ):

        return """
SELECT *
FROM orders;
""".strip()

    # -----------------------------------------------------
    # DEFAULT
    # -----------------------------------------------------

    return """
SELECT *
FROM customers
LIMIT 10;
""".strip()


# =========================================================
# CHECK WHETHER SQL IS SAFE
# =========================================================

def is_safe_sql(sql):

    if not sql:
        return False

    sql_lower = sql.lower().strip()

    # Remove final semicolon
    sql_check = sql_lower.rstrip(";").strip()

    # Only SELECT or WITH queries
    if not (
        sql_check.startswith("select")
        or
        sql_check.startswith("with")
    ):

        return False

    # Dangerous commands
    forbidden_keywords = [

        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "replace ",

    ]

    for keyword in forbidden_keywords:

        if keyword in sql_lower:
            return False

    return True


# =========================================================
# MAIN SQL GENERATOR
# =========================================================

def generate_sql(question):

    # -----------------------------------------------------
    # Validate Question
    # -----------------------------------------------------

    if not question or not question.strip():

        return {
            "success": False,
            "error": "Please enter a question."
        }

    question = question.strip()

    # -----------------------------------------------------
    # Get Database Schema
    # -----------------------------------------------------

    try:

        schema = get_schema_text()

    except Exception as error:

        print(
            "SCHEMA ERROR:",
            repr(error)
        )

        return {
            "success": False,
            "error": (
                "Unable to read database schema: "
                + str(error)
            )
        }

    # -----------------------------------------------------
    # Reload .env
    # -----------------------------------------------------

    load_dotenv(override=True)

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    # =====================================================
    # DEMO MODE
    # =====================================================

    if not api_key:

        print(
            "OPENAI_API_KEY not found."
        )

        print(
            "Using DEMO MODE."
        )

        return {

            "success": True,

            "sql": generate_with_demo(
                question,
                schema
            ),

            "mode": "demo",

            "message": (
                "OpenAI API key not configured. "
                "Using Demo Mode."
            )

        }

    # =====================================================
    # AI MODE
    # =====================================================

    try:

        # -------------------------------------------------
        # OpenAI Client
        # -------------------------------------------------

        client = OpenAI(
            api_key=api_key
        )

        # -------------------------------------------------
        # AI Prompt
        # -------------------------------------------------

        prompt = f"""
You are an expert SQLite SQL developer.

Convert the user's natural-language question
into ONE valid SQLite SQL query.

DATABASE SCHEMA
===============

{schema}

USER QUESTION
=============

{question}

STRICT RULES
============

1. Return ONLY SQL.
2. Do NOT use Markdown.
3. Do NOT add explanations.
4. Use ONLY tables present in the schema.
5. Use ONLY columns present in the schema.
6. Generate SQLite-compatible SQL.
7. Prefer SELECT queries.
8. Never generate INSERT.
9. Never generate UPDATE.
10. Never generate DELETE.
11. Never generate DROP.
12. Never generate ALTER.
13. Never generate TRUNCATE.
14. If aggregation is required, use GROUP BY.
15. For highest/lowest/top/bottom questions,
    use ORDER BY and LIMIT.
16. Do not invent tables.
17. Do not invent columns.
"""

        # -------------------------------------------------
        # OpenAI Responses API
        # -------------------------------------------------

        response = client.responses.create(

            model="gpt-5.6",

            instructions=(
                "You are an expert SQLite SQL generator. "
                "Return only valid SQL."
            ),

            input=prompt
        )

        # -------------------------------------------------
        # Get AI Response
        # -------------------------------------------------

        sql = response.output_text

        sql = clean_sql(sql)

        # -------------------------------------------------
        # Empty AI Response
        # -------------------------------------------------

        if not sql:

            raise Exception(
                "AI returned an empty SQL query."
            )

        # -------------------------------------------------
        # Security Validation
        # -------------------------------------------------

        if not is_safe_sql(sql):

            return {

                "success": False,

                "error": (
                    "Unsafe SQL detected. "
                    "Only SELECT queries are allowed."
                )

            }

        # -------------------------------------------------
        # AI SUCCESS
        # -------------------------------------------------

        return {

            "success": True,

            "sql": sql,

            "mode": "ai"

        }

    # =====================================================
    # API ERROR
    # =====================================================

    except Exception as error:

        error_message = str(error)

        print(
            "\n========================================"
        )

        print(
            "SQL GENERATION ERROR:"
        )

        print(
            repr(error)
        )

        print(
            "========================================\n"
        )

        # =================================================
        # 429 QUOTA ERROR
        # =================================================

        if (
            "429" in error_message
            or
            "insufficient_quota" in error_message
            or
            "exceeded your current quota"
            in error_message.lower()
        ):

            print(
                "OpenAI quota unavailable."
            )

            print(
                "Switching to DEMO MODE."
            )

            demo_sql = generate_with_demo(
                question,
                schema
            )

            return {

                "success": True,

                "sql": demo_sql,

                "mode": "demo",

                "message": (
                    "OpenAI API quota is unavailable. "
                    "The query was generated using "
                    "Demo Mode."
                )

            }

        # =================================================
        # 401 AUTHENTICATION ERROR
        # =================================================

        if (
            "401" in error_message
            or
            "invalid_api_key"
            in error_message.lower()
        ):

            print(
                "OpenAI API key is invalid."
            )

            print(
                "Switching to DEMO MODE."
            )

            demo_sql = generate_with_demo(
                question,
                schema
            )

            return {

                "success": True,

                "sql": demo_sql,

                "mode": "demo",

                "message": (
                    "OpenAI API authentication failed. "
                    "The query was generated using "
                    "Demo Mode."
                )

            }

        # =================================================
        # OTHER API ERRORS
        # =================================================

        return {

            "success": False,

            "error": (
                "AI SQL generation failed: "
                + error_message
            )

        }
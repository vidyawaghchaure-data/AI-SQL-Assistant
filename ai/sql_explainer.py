import os

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(override=True)


# =========================================================
# DEMO SQL EXPLANATION
# =========================================================

def generate_demo_explanation(sql):

    sql_lower = sql.lower().strip()

    # -----------------------------------------------------
    # SELECT *
    # -----------------------------------------------------

    if (
        sql_lower.startswith("select *")
        and "from customers" in sql_lower
    ):

        return (
            "This query retrieves all columns and all records "
            "from the customers table. The SELECT * statement "
            "means every column is selected, while FROM customers "
            "specifies that the data comes from the customers table."
        )

    # -----------------------------------------------------
    # Customers from Pune
    # -----------------------------------------------------

    if (
        "from customers" in sql_lower
        and "where city" in sql_lower
    ):

        return (
            "This query retrieves customer records from the "
            "customers table. The WHERE condition filters the "
            "records so that only customers from Pune are returned."
        )

    # -----------------------------------------------------
    # COUNT Customers
    # -----------------------------------------------------

    if (
        "count" in sql_lower
        and "customers" in sql_lower
    ):

        return (
            "This query counts the total number of records "
            "in the customers table. COUNT(*) counts every "
            "customer record and returns the total number "
            "of customers."
        )

    # -----------------------------------------------------
    # SUM / Total Sales
    # -----------------------------------------------------

    if (
        "sum(" in sql_lower
        and "orders" in sql_lower
    ):

        return (
            "This query calculates the total order amount. "
            "The SUM function adds the values from the amount "
            "column in the orders table and returns the total."
        )

    # -----------------------------------------------------
    # AVG
    # -----------------------------------------------------

    if (
        "avg(" in sql_lower
        and "orders" in sql_lower
    ):

        return (
            "This query calculates the average order amount. "
            "The AVG function calculates the mean value of "
            "the amount column from the orders table."
        )

    # -----------------------------------------------------
    # GROUP BY
    # -----------------------------------------------------

    if "group by" in sql_lower:

        return (
            "This query groups records based on the specified "
            "columns. Aggregate functions such as SUM or COUNT "
            "are then applied to each group. GROUP BY is useful "
            "for generating summarized results."
        )

    # -----------------------------------------------------
    # ORDER BY
    # -----------------------------------------------------

    if "order by" in sql_lower:

        explanation = (
            "This query retrieves data and sorts the result "
            "using the ORDER BY clause."
        )

        if "desc" in sql_lower:

            explanation += (
                " DESC sorts the results from highest to lowest."
            )

        elif "asc" in sql_lower:

            explanation += (
                " ASC sorts the results from lowest to highest."
            )

        return explanation

    # -----------------------------------------------------
    # LIMIT
    # -----------------------------------------------------

    if "limit" in sql_lower:

        return (
            "This query retrieves records from the database "
            "and uses the LIMIT clause to restrict the number "
            "of records returned."
        )

    # -----------------------------------------------------
    # General SELECT
    # -----------------------------------------------------

    if (
        sql_lower.startswith("select")
        or sql_lower.startswith("with")
    ):

        return (
            "This SQL query retrieves data from the database. "
            "The SELECT clause specifies the information to "
            "retrieve, while the FROM clause identifies the "
            "table containing the data."
        )

    # -----------------------------------------------------
    # Default
    # -----------------------------------------------------

    return (
        "This SQL query reads data from the database and "
        "returns the requested records."
    )


# =========================================================
# MAIN EXPLANATION FUNCTION
# =========================================================

def explain_sql(sql):

    # -----------------------------------------------------
    # Validate SQL
    # -----------------------------------------------------

    if not sql or not sql.strip():

        return (
            "No SQL query was provided for explanation."
        )

    sql = sql.strip()

    # -----------------------------------------------------
    # API KEY
    # -----------------------------------------------------

    load_dotenv(override=True)

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    # =====================================================
    # DEMO MODE
    # =====================================================

    if not api_key:

        return generate_demo_explanation(sql)

    # =====================================================
    # AI MODE
    # =====================================================

    try:

        client = OpenAI(
            api_key=api_key
        )

        prompt = f"""
Explain the following SQLite SQL query
in simple language for a computer engineering student.

SQL QUERY
=========

{sql}

Explain:

1. What the query does.
2. Which table is being used.
3. What columns are selected.
4. Explain WHERE, GROUP BY, ORDER BY,
   LIMIT or aggregate functions if present.
5. Explain the expected result.

Keep the explanation clear and concise.

Do not generate another SQL query.
"""

        response = client.responses.create(

            model="gpt-5.6",

            instructions=(
                "You are an SQL teacher. "
                "Explain SQL queries clearly "
                "for beginners."
            ),

            input=prompt
        )

        explanation = response.output_text

        if explanation:

            return explanation.strip()

        return generate_demo_explanation(sql)

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        error_message = str(error)

        print(
            "SQL EXPLANATION ERROR:",
            repr(error)
        )

        # -------------------------------------------------
        # 429 QUOTA
        # -------------------------------------------------

        if (
            "429" in error_message
            or
            "insufficient_quota"
            in error_message
            or
            "exceeded your current quota"
            in error_message.lower()
        ):

            print(
                "OpenAI quota unavailable."
            )

            print(
                "Using DEMO explanation."
            )

            return generate_demo_explanation(sql)

        # -------------------------------------------------
        # 401 API KEY
        # -------------------------------------------------

        if (
            "401" in error_message
            or
            "invalid_api_key"
            in error_message.lower()
        ):

            print(
                "Invalid OpenAI API key."
            )

            print(
                "Using DEMO explanation."
            )

            return generate_demo_explanation(sql)

        # -------------------------------------------------
        # OTHER ERROR
        # -------------------------------------------------

        return (
            "AI explanation unavailable. "
            "Demo explanation:\n\n"
            + generate_demo_explanation(sql)
        )
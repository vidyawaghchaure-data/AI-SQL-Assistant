from services.database_service import get_schema


def get_schema_text():

    schema = get_schema()

    if not schema:
        return "No tables found in the database."

    output = []

    for table, columns in schema.items():

        output.append(f"TABLE: {table}")

        for column in columns:

            primary = " PRIMARY KEY" if column["primary_key"] else ""

            output.append(
                f"- {column['name']} ({column['type']}){primary}"
            )

        output.append("")

    return "\n".join(output)
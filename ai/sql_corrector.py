import os

from dotenv import load_dotenv
from openai import OpenAI

from services.schema_service import get_schema_text

load_dotenv()


def correct_sql(sql, error):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:

        return {
            "success": False,
            "message": "AI correction requires an API key."
        }

    try:

        client = OpenAI(api_key=api_key)

        schema = get_schema_text()

        prompt = f"""
Fix the following SQLite query.

Schema:
{schema}

SQL:
{sql}

Error:
{error}

Return ONLY the corrected SQL.
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        corrected = response.choices[0].message.content

        corrected = corrected.replace("```sql", "")
        corrected = corrected.replace("```", "")

        return {
            "success": True,
            "sql": corrected.strip()
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }
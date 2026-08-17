import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "history",
    "query_history.json"
)


def save_query(question, sql, success=True):

    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    try:

        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.insert(0, {
        "question": question,
        "sql": sql,
        "success": success,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    history = history[:100]

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def get_history():

    try:

        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []
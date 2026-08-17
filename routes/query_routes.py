from flask import Blueprint, jsonify, request

from ai.sql_corrector import correct_sql
from ai.sql_explainer import explain_sql
from ai.sql_generator import generate_sql
from services.database_service import execute_query
from services.query_service import get_history, save_query

query_bp = Blueprint("query", __name__)


@query_bp.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:

        return jsonify({
            "success": False,
            "error": "Please enter a question."
        }), 400

    result = generate_sql(question)

    return jsonify(result)


@query_bp.route("/execute", methods=["POST"])
def execute():

    data = request.get_json()

    question = data.get("question", "")
    sql = data.get("sql", "").strip()

    if not sql:

        return jsonify({
            "success": False,
            "error": "SQL query is required."
        }), 400

    result = execute_query(sql)

    save_query(
        question,
        sql,
        result.get("success", False)
    )

    return jsonify(result)


@query_bp.route("/explain", methods=["POST"])
def explain():

    data = request.get_json()

    sql = data.get("sql", "").strip()

    if not sql:

        return jsonify({
            "success": False,
            "error": "SQL query is required."
        }), 400

    explanation = explain_sql(sql)

    return jsonify({
        "success": True,
        "explanation": explanation
    })


@query_bp.route("/correct", methods=["POST"])
def correct():

    data = request.get_json()

    sql = data.get("sql", "")
    error = data.get("error", "")

    result = correct_sql(sql, error)

    return jsonify(result)


@query_bp.route("/history", methods=["GET"])
def history_api():

    return jsonify({
        "success": True,
        "history": get_history()
    })
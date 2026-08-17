from flask import Blueprint, jsonify

from services.database_service import get_schema, get_tables

database_bp = Blueprint("database", __name__)


@database_bp.route("/tables", methods=["GET"])
def tables():

    return jsonify({
        "success": True,
        "tables": get_tables()
    })


@database_bp.route("/schema-data", methods=["GET"])
def schema_data():

    return jsonify({
        "success": True,
        "schema": get_schema()
    })
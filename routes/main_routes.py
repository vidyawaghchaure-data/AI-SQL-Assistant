from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@main_bp.route("/schema")
def schema():
    return render_template("schema.html")


@main_bp.route("/history")
def history():
    return render_template("history.html")
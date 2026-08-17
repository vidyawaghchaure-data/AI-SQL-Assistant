from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "ai-sql-assistant-secret-key"

    base_dir = os.path.abspath(os.path.dirname(__file__))
    database_dir = os.path.join(base_dir, "database")

    os.makedirs(database_dir, exist_ok=True)

    database_path = os.path.join(database_dir, "app.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + database_path.replace("\\", "/")
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from routes.main_routes import main_bp
    from routes.query_routes import query_bp
    from routes.database_routes import database_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(query_bp, url_prefix="/api")
    app.register_blueprint(database_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
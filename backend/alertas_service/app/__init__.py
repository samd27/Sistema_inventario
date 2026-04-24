import os

from flask import Flask, jsonify
from flask_cors import CORS
from typing import Optional

from config.config import config
from app.database import db
from app.models.alerta_model import AlertaModel
from app.models.notification_log_model import NotificationLogModel
from app.services.email_service import EmailService
from app.services.alerta_service import AlertaService
from app.web.api.alertas_api import create_alertas_api


def create_app(config_name: Optional[str] = None):
    env_name = config_name or "development"

    app = Flask(__name__)
    app.config.from_object(config.get(env_name, config["default"]))

    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        os.environ.get("FRONTEND_URL", ""),
    ]
    if env_name == "production":
        allowed_origins.append("https://*.railway.app")
    CORS(app, origins=allowed_origins, supports_credentials=True)

    db.init_app(app)
    with app.app_context():
        db.create_all()

        email_service = EmailService(app.config)
        alerta_service = AlertaService(email_service)
        alertas_api = create_alertas_api(alerta_service)
        app.register_blueprint(alertas_api)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"success": True, "service": "alertas_service", "status": "ok"}), 200

    return app

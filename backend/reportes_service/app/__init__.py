import os

from flask import Flask, jsonify
from flask_cors import CORS
from typing import Optional

from config.config import config
from app.database import db
from app.models.reporte_snapshot_model import ReporteSnapshotModel
from app.models.reporte_ejecucion_model import ReporteEjecucionModel
from app.services.reportes_service import ReportesService
from app.web.api.reportes_api import create_reportes_api


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
        reportes_service = ReportesService()
        reportes_api = create_reportes_api(reportes_service)
        app.register_blueprint(reportes_api)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"success": True, "service": "reportes_service", "status": "ok"}), 200

    return app

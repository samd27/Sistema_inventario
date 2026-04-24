from flask import Blueprint, jsonify, current_app
import requests

from app.services.reportes_service import ReportesService


def _fetch_inventory_data(base_url: str):
    base_url = base_url.rstrip("/")
    productos = requests.get(f"{base_url}/api/productos/", timeout=20).json().get("data", [])
    categorias = requests.get(f"{base_url}/api/categorias/", timeout=20).json().get("data", [])
    proveedores = requests.get(f"{base_url}/api/proveedores/", timeout=20).json().get("data", [])
    bajo_stock = requests.get(f"{base_url}/api/productos/bajo-stock", timeout=20).json().get("data", [])
    return {
        "productos": productos,
        "categorias": categorias,
        "proveedores": proveedores,
        "bajo_stock": bajo_stock,
    }


def create_reportes_api(reportes_service: ReportesService):
    api = Blueprint("reportes_api", __name__, url_prefix="/api/reportes")

    @api.route("/resumen", methods=["GET"])
    def resumen():
        inventory_api_url = current_app.config["INVENTORY_API_URL"]
        try:
            payload = _fetch_inventory_data(inventory_api_url)
            data, err = reportes_service.generar_resumen_ejecutivo(payload)
            if err:
                return jsonify({"success": False, "error": err}), 500
            return jsonify({"success": True, "data": data}), 200
        except Exception as exc:
            return jsonify({"success": False, "error": f"No fue posible generar resumen: {exc}"}), 502

    @api.route("/bajo-stock-snapshot", methods=["POST"])
    def snapshot_bajo_stock():
        inventory_api_url = current_app.config["INVENTORY_API_URL"]
        try:
            payload = _fetch_inventory_data(inventory_api_url)
            snapshot, err = reportes_service.generar_snapshot_bajo_stock(payload["bajo_stock"])
            if err:
                return jsonify({"success": False, "error": err}), 500
            return jsonify({"success": True, "data": snapshot.to_dict()}), 201
        except Exception as exc:
            return jsonify({"success": False, "error": f"No fue posible generar snapshot: {exc}"}), 502

    @api.route("/tendencia-bajo-stock", methods=["GET"])
    def tendencia_bajo_stock():
        data = reportes_service.obtener_tendencia_bajo_stock(limit=30)
        return jsonify({"success": True, "data": data}), 200

    @api.route("/ejecuciones", methods=["GET"])
    def ejecuciones():
        ejecuciones = reportes_service.listar_ejecuciones(limit=50)
        return jsonify({"success": True, "data": [e.to_dict() for e in ejecuciones]}), 200

    return api

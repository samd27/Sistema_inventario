from flask import Blueprint, jsonify, request, current_app
import requests

from app.services.alerta_service import AlertaService


def create_alertas_api(alerta_service: AlertaService):
    api = Blueprint("alertas_api", __name__, url_prefix="/api/alertas")

    @api.route("/", methods=["GET"])
    def listar_alertas():
        estado = request.args.get("estado")
        alertas = alerta_service.listar_alertas(estado)
        return jsonify({
            "success": True,
            "data": [a.to_dict() for a in alertas],
        }), 200

    @api.route("/notificaciones", methods=["GET"])
    def listar_notificaciones():
        logs = alerta_service.listar_logs()
        return jsonify({
            "success": True,
            "data": [l.to_dict() for l in logs],
        }), 200

    @api.route("/events/stock-bajo", methods=["POST"])
    def evento_stock_bajo():
        try:
            payload = request.get_json() or {}
            required = ["producto_id", "nombre_producto", "stock_actual", "stock_minimo"]
            missing = [key for key in required if key not in payload]
            if missing:
                return jsonify({"success": False, "error": f"Campos faltantes: {', '.join(missing)}"}), 400

            alerta, log = alerta_service.registrar_alerta_stock_bajo(payload)
            return jsonify({
                "success": True,
                "data": {
                    "alerta": alerta.to_dict(),
                    "notificacion": log.to_dict(),
                },
            }), 201
        except Exception as exc:
            return jsonify({"success": False, "error": str(exc)}), 500

    @api.route("/check-now", methods=["POST"])
    def check_now():
        inventory_api_url = current_app.config["INVENTORY_API_URL"].rstrip("/")
        endpoint = f"{inventory_api_url}/api/productos/bajo-stock"

        try:
            response = requests.get(endpoint, timeout=15)
            response.raise_for_status()
            result = response.json()
            productos = result.get("data", [])
        except Exception as exc:
            return jsonify({"success": False, "error": f"No fue posible consultar inventario: {exc}"}), 502

        generadas = []
        for p in productos:
            payload = {
                "producto_id": p["id"],
                "nombre_producto": p["nombre"],
                "stock_actual": p["stock"],
                "stock_minimo": p["stock_minimo"],
            }
            alerta, _ = alerta_service.registrar_alerta_stock_bajo(payload)
            generadas.append(alerta.to_dict())

        return jsonify({
            "success": True,
            "data": {
                "total": len(generadas),
                "alertas": generadas,
            },
        }), 200

    return api

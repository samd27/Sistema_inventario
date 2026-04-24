import requests


class AlertasServiceClient:
    def __init__(self, base_url: str, timeout_seconds: int = 5):
        self.base_url = (base_url or "").rstrip("/")
        self.timeout_seconds = timeout_seconds

    def is_enabled(self) -> bool:
        return bool(self.base_url)

    def notify_low_stock(self, producto):
        if not self.is_enabled():
            return False, "Alertas service URL no configurada"

        payload = {
            "producto_id": producto.id,
            "nombre_producto": producto.nombre,
            "stock_actual": producto.cantidad_stock,
            "stock_minimo": producto.stock_minimo,
        }

        endpoint = f"{self.base_url}/api/alertas/events/stock-bajo"

        try:
            response = requests.post(endpoint, json=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
            return True, None
        except Exception as exc:
            return False, str(exc)

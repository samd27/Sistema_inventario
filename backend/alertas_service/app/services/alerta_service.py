from app.database import db
from app.models.alerta_model import AlertaModel
from app.models.notification_log_model import NotificationLogModel
from typing import Optional


class AlertaService:
    def __init__(self, email_service):
        self.email_service = email_service

    @staticmethod
    def _build_message(nombre_producto: str, stock_actual: int, stock_minimo: int) -> str:
        return (
            f"Producto '{nombre_producto}' con stock bajo. "
            f"Stock actual: {stock_actual}. Stock minimo: {stock_minimo}."
        )

    @staticmethod
    def _build_severity(stock_actual: int, stock_minimo: int) -> str:
        if stock_actual <= 0:
            return "critica"
        if stock_actual <= max(1, stock_minimo // 2):
            return "alta"
        return "media"

    def registrar_alerta_stock_bajo(self, payload: dict):
        producto_id = int(payload["producto_id"])
        nombre_producto = payload["nombre_producto"]
        stock_actual = int(payload["stock_actual"])
        stock_minimo = int(payload["stock_minimo"])

        alerta = AlertaModel.query.filter_by(producto_id=producto_id, estado="pendiente").first()
        mensaje = self._build_message(nombre_producto, stock_actual, stock_minimo)
        severidad = self._build_severity(stock_actual, stock_minimo)

        if alerta:
            alerta.nombre_producto = nombre_producto
            alerta.stock_actual = stock_actual
            alerta.stock_minimo = stock_minimo
            alerta.severidad = severidad
            alerta.mensaje = mensaje
        else:
            alerta = AlertaModel(
                producto_id=producto_id,
                nombre_producto=nombre_producto,
                stock_actual=stock_actual,
                stock_minimo=stock_minimo,
                severidad=severidad,
                estado="pendiente",
                mensaje=mensaje,
            )
            db.session.add(alerta)

        db.session.commit()

        subject = f"[Inventario] Alerta de stock bajo: {nombre_producto}"
        body = f"{mensaje}\n\nGenerada por Alertas Service."
        sent, detail = self.email_service.send_low_stock_alert(subject, body)

        log = NotificationLogModel(
            alerta_id=alerta.id,
            canal="email",
            destinatario=self.email_service.alerts_to_email or "",
            estado="enviado" if sent else "fallido",
            detalle=detail,
        )
        db.session.add(log)
        db.session.commit()

        return alerta, log

    @staticmethod
    def listar_alertas(estado: Optional[str] = None):
        query = AlertaModel.query.order_by(AlertaModel.fecha_creacion.desc())
        if estado:
            query = query.filter_by(estado=estado)
        return query.all()

    @staticmethod
    def listar_logs():
        return NotificationLogModel.query.order_by(NotificationLogModel.fecha_envio.desc()).limit(100).all()

from datetime import datetime
from app.database import db


class NotificationLogModel(db.Model):
    __tablename__ = "notification_logs"

    id = db.Column(db.Integer, primary_key=True)
    alerta_id = db.Column(db.Integer, nullable=False, index=True)
    canal = db.Column(db.String(30), nullable=False, default="email")
    destinatario = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    detalle = db.Column(db.String(255), nullable=True)
    fecha_envio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "alerta_id": self.alerta_id,
            "canal": self.canal,
            "destinatario": self.destinatario,
            "estado": self.estado,
            "detalle": self.detalle,
            "fecha_envio": self.fecha_envio.isoformat() if self.fecha_envio else None,
        }

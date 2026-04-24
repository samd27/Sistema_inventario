from datetime import datetime
from app.database import db


class AlertaModel(db.Model):
    __tablename__ = "alertas"

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False, index=True)
    nombre_producto = db.Column(db.String(120), nullable=False)
    stock_actual = db.Column(db.Integer, nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False)
    severidad = db.Column(db.String(20), nullable=False, default="media")
    estado = db.Column(db.String(20), nullable=False, default="pendiente")
    mensaje = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "producto_id": self.producto_id,
            "nombre_producto": self.nombre_producto,
            "stock_actual": self.stock_actual,
            "stock_minimo": self.stock_minimo,
            "severidad": self.severidad,
            "estado": self.estado,
            "mensaje": self.mensaje,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
        }

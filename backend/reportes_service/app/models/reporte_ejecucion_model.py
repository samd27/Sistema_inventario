from datetime import datetime
from app.database import db


class ReporteEjecucionModel(db.Model):
    __tablename__ = "reporte_ejecuciones"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(40), nullable=False, index=True)
    estado = db.Column(db.String(20), nullable=False)
    detalle = db.Column(db.String(255), nullable=True)
    fecha_ejecucion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "estado": self.estado,
            "detalle": self.detalle,
            "fecha_ejecucion": self.fecha_ejecucion.isoformat() if self.fecha_ejecucion else None,
        }

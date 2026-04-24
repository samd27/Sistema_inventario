from datetime import datetime
from app.database import db


class ReporteSnapshotModel(db.Model):
    __tablename__ = "reporte_snapshots"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(40), nullable=False, index=True)
    fecha = db.Column(db.Date, nullable=False, index=True)
    total_bajo_stock = db.Column(db.Integer, nullable=False, default=0)
    detalle_json = db.Column(db.Text, nullable=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "total_bajo_stock": self.total_bajo_stock,
            "detalle_json": self.detalle_json,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }

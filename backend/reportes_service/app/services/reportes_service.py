import json
from datetime import date
from typing import Optional

from app.database import db
from app.models.reporte_snapshot_model import ReporteSnapshotModel
from app.models.reporte_ejecucion_model import ReporteEjecucionModel


class ReportesService:
    @staticmethod
    def _registrar_ejecucion(tipo: str, estado: str, detalle: Optional[str] = None):
        ejecucion = ReporteEjecucionModel(tipo=tipo, estado=estado, detalle=detalle)
        db.session.add(ejecucion)
        db.session.commit()
        return ejecucion

    def generar_resumen_ejecutivo(self, inventario_payload: dict):
        try:
            productos = inventario_payload.get("productos", [])
            categorias = inventario_payload.get("categorias", [])
            proveedores = inventario_payload.get("proveedores", [])
            bajo_stock = [p for p in productos if int(p.get("stock", 0)) <= int(p.get("stock_minimo", 0))]

            stock_total = sum(int(p.get("stock", 0)) for p in productos)
            valor_total = sum(float(p.get("precio", 0)) * int(p.get("stock", 0)) for p in productos)

            data = {
                "total_productos": len(productos),
                "total_categorias": len(categorias),
                "total_proveedores": len(proveedores),
                "productos_bajo_stock": len(bajo_stock),
                "stock_total_unidades": stock_total,
                "valor_total_estimado": round(valor_total, 2),
            }
            self._registrar_ejecucion("resumen", "ok", "Resumen generado")
            return data, None
        except Exception as exc:
            self._registrar_ejecucion("resumen", "error", str(exc))
            return None, str(exc)

    def generar_snapshot_bajo_stock(self, productos_bajo_stock: list[dict]):
        try:
            snapshot = ReporteSnapshotModel(
                tipo="bajo_stock",
                fecha=date.today(),
                total_bajo_stock=len(productos_bajo_stock),
                detalle_json=json.dumps(productos_bajo_stock, ensure_ascii=False),
            )
            db.session.add(snapshot)
            db.session.commit()

            self._registrar_ejecucion("snapshot_bajo_stock", "ok", "Snapshot generado")
            return snapshot, None
        except Exception as exc:
            self._registrar_ejecucion("snapshot_bajo_stock", "error", str(exc))
            return None, str(exc)

    @staticmethod
    def obtener_tendencia_bajo_stock(limit: int = 15):
        snapshots = ReporteSnapshotModel.query.filter_by(tipo="bajo_stock") \
            .order_by(ReporteSnapshotModel.fecha.desc()) \
            .limit(limit).all()
        ordered = list(reversed(snapshots))

        return [
            {
                "fecha": s.fecha.isoformat(),
                "total_bajo_stock": s.total_bajo_stock,
            }
            for s in ordered
        ]

    @staticmethod
    def listar_ejecuciones(limit: int = 30):
        return ReporteEjecucionModel.query.order_by(ReporteEjecucionModel.fecha_ejecucion.desc()).limit(limit).all()

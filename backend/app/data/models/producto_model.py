"""
Modelo de Producto para SQLAlchemy
"""
from datetime import datetime
from app.data.database import db
from app.core.entities.producto import Producto


class ProductoModel(db.Model):
    """Modelo de base de datos para Producto"""
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad_stock = db.Column(db.Integer, nullable=False)
    stock_minimo = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_entity(self) -> Producto:
        """Convierte el modelo de BD a entidad de dominio"""
        return Producto(
            id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion,
            precio=self.precio,
            cantidad_stock=self.cantidad_stock,
            stock_minimo=self.stock_minimo,
            categoria_id=self.categoria_id,
            proveedor_id=self.proveedor_id,
            fecha_creacion=self.fecha_creacion,
            fecha_actualizacion=self.fecha_actualizacion
        )
    
    @staticmethod
    def from_entity(producto: Producto) -> 'ProductoModel':
        """Convierte una entidad de dominio a modelo de BD"""
        return ProductoModel(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            cantidad_stock=producto.cantidad_stock,
            stock_minimo=producto.stock_minimo,
            categoria_id=producto.categoria_id,
            proveedor_id=producto.proveedor_id
        )

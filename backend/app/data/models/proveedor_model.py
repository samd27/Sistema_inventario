"""
Modelo de Proveedor para SQLAlchemy
"""
from datetime import datetime
from app.data.database import db
from app.core.entities.proveedor import Proveedor


class ProveedorModel(db.Model):
    """Modelo de base de datos para Proveedor"""
    __tablename__ = 'proveedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con productos
    productos = db.relationship('ProductoModel', backref='proveedor', lazy=True)
    
    def to_entity(self) -> Proveedor:
        """Convierte el modelo de BD a entidad de dominio"""
        return Proveedor(
            id=self.id,
            nombre=self.nombre,
            contacto=self.contacto,
            telefono=self.telefono,
            email=self.email,
            direccion=self.direccion,
            fecha_creacion=self.fecha_creacion
        )
    
    @staticmethod
    def from_entity(proveedor: Proveedor) -> 'ProveedorModel':
        """Convierte una entidad de dominio a modelo de BD"""
        return ProveedorModel(
            id=proveedor.id,
            nombre=proveedor.nombre,
            contacto=proveedor.contacto,
            telefono=proveedor.telefono,
            email=proveedor.email,
            direccion=proveedor.direccion
        )

"""
Modelo de Categoría para SQLAlchemy
Este es un adaptador - traduce entre la entidad de dominio y la base de datos
"""
from datetime import datetime
from app.data.database import db
from app.core.entities.categoria import Categoria


class CategoriaModel(db.Model):
    """Modelo de base de datos para Categoría"""
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con productos
    productos = db.relationship('ProductoModel', backref='categoria', lazy=True, cascade='all, delete-orphan')
    
    def to_entity(self) -> Categoria:
        """Convierte el modelo de BD a entidad de dominio"""
        return Categoria(
            id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion,
            fecha_creacion=self.fecha_creacion
        )
    
    @staticmethod
    def from_entity(categoria: Categoria) -> 'CategoriaModel':
        """Convierte una entidad de dominio a modelo de BD"""
        return CategoriaModel(
            id=categoria.id,
            nombre=categoria.nombre,
            descripcion=categoria.descripcion
        )

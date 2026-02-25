"""
Implementación del Repositorio de Categorías
Este adaptador implementa la interfaz definida en el dominio
"""
from typing import List, Optional
from app.core.entities.categoria import Categoria
from app.core.interfaces.categoria_repository import ICategoriaRepository
from app.data.models.categoria_model import CategoriaModel
from app.data.database import db


class CategoriaRepository(ICategoriaRepository):
    """Implementación del repositorio de categorías usando SQLAlchemy"""
    
    def crear(self, categoria: Categoria) -> Categoria:
        """Crea una nueva categoría en la base de datos"""
        modelo = CategoriaModel.from_entity(categoria)
        db.session.add(modelo)
        db.session.commit()
        return modelo.to_entity()
    
    def obtener_por_id(self, id: int) -> Optional[Categoria]:
        """Obtiene una categoría por su ID"""
        modelo = CategoriaModel.query.get(id)
        return modelo.to_entity() if modelo else None
    
    def obtener_todos(self) -> List[Categoria]:
        """Obtiene todas las categorías"""
        modelos = CategoriaModel.query.all()
        return [modelo.to_entity() for modelo in modelos]
    
    def actualizar(self, categoria: Categoria) -> bool:
        """Actualiza una categoría existente"""
        modelo = CategoriaModel.query.get(categoria.id)
        if not modelo:
            return False
        
        modelo.nombre = categoria.nombre
        modelo.descripcion = categoria.descripcion
        db.session.commit()
        return True
    
    def eliminar(self, id: int) -> bool:
        """Elimina una categoría"""
        modelo = CategoriaModel.query.get(id)
        if not modelo:
            return False
        
        db.session.delete(modelo)
        db.session.commit()
        return True
    
    def existe_nombre(self, nombre: str) -> bool:
        """Verifica si existe una categoría con el nombre dado"""
        return CategoriaModel.query.filter_by(nombre=nombre).first() is not None

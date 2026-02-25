"""
Implementación del Repositorio de Proveedores
"""
from typing import List, Optional
from app.core.entities.proveedor import Proveedor
from app.core.interfaces.proveedor_repository import IProveedorRepository
from app.data.models.proveedor_model import ProveedorModel
from app.data.database import db


class ProveedorRepository(IProveedorRepository):
    """Implementación del repositorio de proveedores usando SQLAlchemy"""
    
    def crear(self, proveedor: Proveedor) -> Proveedor:
        """Crea un nuevo proveedor en la base de datos"""
        modelo = ProveedorModel.from_entity(proveedor)
        db.session.add(modelo)
        db.session.commit()
        return modelo.to_entity()
    
    def obtener_por_id(self, id: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por su ID"""
        modelo = ProveedorModel.query.get(id)
        return modelo.to_entity() if modelo else None
    
    def obtener_todos(self) -> List[Proveedor]:
        """Obtiene todos los proveedores"""
        modelos = ProveedorModel.query.all()
        return [modelo.to_entity() for modelo in modelos]
    
    def actualizar(self, proveedor: Proveedor) -> bool:
        """Actualiza un proveedor existente"""
        modelo = ProveedorModel.query.get(proveedor.id)
        if not modelo:
            return False
        
        modelo.nombre = proveedor.nombre
        modelo.contacto = proveedor.contacto
        modelo.telefono = proveedor.telefono
        modelo.email = proveedor.email
        modelo.direccion = proveedor.direccion
        db.session.commit()
        return True
    
    def eliminar(self, id: int) -> bool:
        """Elimina un proveedor"""
        modelo = ProveedorModel.query.get(id)
        if not modelo:
            return False
        
        db.session.delete(modelo)
        db.session.commit()
        return True
    
    def buscar_por_nombre(self, nombre: str) -> List[Proveedor]:
        """Busca proveedores por nombre"""
        modelos = ProveedorModel.query.filter(
            ProveedorModel.nombre.ilike(f'%{nombre}%')
        ).all()
        return [modelo.to_entity() for modelo in modelos]

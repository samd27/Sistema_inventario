"""
Interfaz de Repositorio de Proveedores - Puerto (Port)
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.proveedor import Proveedor


class IProveedorRepository(ABC):
    """Interfaz para el repositorio de proveedores"""
    
    @abstractmethod
    def crear(self, proveedor: Proveedor) -> Proveedor:
        """Crea un nuevo proveedor"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Proveedor]:
        """Obtiene todos los proveedores"""
        pass
    
    @abstractmethod
    def actualizar(self, proveedor: Proveedor) -> bool:
        """Actualiza un proveedor existente"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un proveedor"""
        pass
    
    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Proveedor]:
        """Busca proveedores por nombre"""
        pass

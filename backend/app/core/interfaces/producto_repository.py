"""
Interfaz de Repositorio de Productos - Puerto (Port)
Define el contrato que debe cumplir cualquier implementación de repositorio
La capa de dominio define la interfaz, la capa de datos la implementa (inversión de dependencias)
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.producto import Producto


class IProductoRepository(ABC):
    """Interfaz para el repositorio de productos"""
    
    @abstractmethod
    def crear(self, producto: Producto) -> Producto:
        """Crea un nuevo producto"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Producto]:
        """Obtiene todos los productos"""
        pass
    
    @abstractmethod
    def actualizar(self, producto: Producto) -> bool:
        """Actualiza un producto existente"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un producto"""
        pass
    
    @abstractmethod
    def obtener_por_categoria(self, categoria_id: int) -> List[Producto]:
        """Obtiene productos por categoría"""
        pass
    
    @abstractmethod
    def obtener_productos_bajo_stock(self) -> List[Producto]:
        """Obtiene productos que necesitan reabastecimiento"""
        pass

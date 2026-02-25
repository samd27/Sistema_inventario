"""
Interfaz de Repositorio de Categorías - Puerto (Port)
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.categoria import Categoria


class ICategoriaRepository(ABC):
    """Interfaz para el repositorio de categorías"""
    
    @abstractmethod
    def crear(self, categoria: Categoria) -> Categoria:
        """Crea una nueva categoría"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Categoria]:
        """Obtiene una categoría por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Categoria]:
        """Obtiene todas las categorías"""
        pass
    
    @abstractmethod
    def actualizar(self, categoria: Categoria) -> bool:
        """Actualiza una categoría existente"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una categoría"""
        pass
    
    @abstractmethod
    def existe_nombre(self, nombre: str) -> bool:
        """Verifica si existe una categoría con el nombre dado"""
        pass

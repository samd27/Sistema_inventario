"""
Casos de Uso de Categorías - Capa de Negocio
"""
from typing import List, Optional
from app.core.entities.categoria import Categoria
from app.core.interfaces.categoria_repository import ICategoriaRepository


class CategoriaUseCases:
    """Casos de uso relacionados con categorías"""
    
    def __init__(self, categoria_repository: ICategoriaRepository):
        self.categoria_repository = categoria_repository
    
    def crear_categoria(self, categoria: Categoria) -> tuple[bool, Optional[str], Optional[Categoria]]:
        """Crea una nueva categoría validando las reglas de negocio"""
        # Validar reglas de negocio
        es_valido, mensaje_error = categoria.validar()
        if not es_valido:
            return False, mensaje_error, None
        
        # Verificar que no exista una categoría con el mismo nombre
        if self.categoria_repository.existe_nombre(categoria.nombre):
            return False, "Ya existe una categoría con ese nombre", None
        
        # Persistir la categoría
        categoria_creada = self.categoria_repository.crear(categoria)
        return True, None, categoria_creada
    
    def obtener_categoria(self, id: int) -> Optional[Categoria]:
        """Obtiene una categoría por su ID"""
        return self.categoria_repository.obtener_por_id(id)
    
    def listar_categorias(self) -> List[Categoria]:
        """Lista todas las categorías"""
        return self.categoria_repository.obtener_todos()
    
    def actualizar_categoria(self, categoria: Categoria) -> tuple[bool, Optional[str]]:
        """Actualiza una categoría existente"""
        # Validar reglas de negocio
        es_valido, mensaje_error = categoria.validar()
        if not es_valido:
            return False, mensaje_error
        
        # Verificar que la categoría existe
        categoria_existente = self.categoria_repository.obtener_por_id(categoria.id)
        if not categoria_existente:
            return False, "Categoría no encontrada"
        
        # Actualizar
        exito = self.categoria_repository.actualizar(categoria)
        if not exito:
            return False, "Error al actualizar la categoría"
        
        return True, None
    
    def eliminar_categoria(self, id: int) -> tuple[bool, Optional[str]]:
        """Elimina una categoría"""
        # Verificar que la categoría existe
        categoria = self.categoria_repository.obtener_por_id(id)
        if not categoria:
            return False, "Categoría no encontrada"
        
        # Eliminar
        exito = self.categoria_repository.eliminar(id)
        if not exito:
            return False, "Error al eliminar la categoría"
        
        return True, None

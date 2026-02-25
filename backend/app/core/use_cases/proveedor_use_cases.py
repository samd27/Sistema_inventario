"""
Casos de Uso de Proveedores - Capa de Negocio
"""
from typing import List, Optional
from app.core.entities.proveedor import Proveedor
from app.core.interfaces.proveedor_repository import IProveedorRepository


class ProveedorUseCases:
    """Casos de uso relacionados con proveedores"""
    
    def __init__(self, proveedor_repository: IProveedorRepository):
        self.proveedor_repository = proveedor_repository
    
    def crear_proveedor(self, proveedor: Proveedor) -> tuple[bool, Optional[str], Optional[Proveedor]]:
        """Crea un nuevo proveedor validando las reglas de negocio"""
        # Validar reglas de negocio
        es_valido, mensaje_error = proveedor.validar()
        if not es_valido:
            return False, mensaje_error, None
        
        # Persistir el proveedor
        proveedor_creado = self.proveedor_repository.crear(proveedor)
        return True, None, proveedor_creado
    
    def obtener_proveedor(self, id: int) -> Optional[Proveedor]:
        """Obtiene un proveedor por su ID"""
        return self.proveedor_repository.obtener_por_id(id)
    
    def listar_proveedores(self) -> List[Proveedor]:
        """Lista todos los proveedores"""
        return self.proveedor_repository.obtener_todos()
    
    def actualizar_proveedor(self, proveedor: Proveedor) -> tuple[bool, Optional[str]]:
        """Actualiza un proveedor existente"""
        # Validar reglas de negocio
        es_valido, mensaje_error = proveedor.validar()
        if not es_valido:
            return False, mensaje_error
        
        # Verificar que el proveedor existe
        proveedor_existente = self.proveedor_repository.obtener_por_id(proveedor.id)
        if not proveedor_existente:
            return False, "Proveedor no encontrado"
        
        # Actualizar
        exito = self.proveedor_repository.actualizar(proveedor)
        if not exito:
            return False, "Error al actualizar el proveedor"
        
        return True, None
    
    def eliminar_proveedor(self, id: int) -> tuple[bool, Optional[str]]:
        """Elimina un proveedor"""
        # Verificar que el proveedor existe
        proveedor = self.proveedor_repository.obtener_por_id(id)
        if not proveedor:
            return False, "Proveedor no encontrado"
        
        # Eliminar
        exito = self.proveedor_repository.eliminar(id)
        if not exito:
            return False, "Error al eliminar el proveedor"
        
        return True, None
    
    def buscar_proveedores(self, nombre: str) -> List[Proveedor]:
        """Busca proveedores por nombre"""
        return self.proveedor_repository.buscar_por_nombre(nombre)

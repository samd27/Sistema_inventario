"""
Casos de Uso de Productos - Capa de Negocio
Estos casos de uso orquestan la lógica de negocio sin depender de frameworks
"""
from typing import List, Optional
from app.core.entities.producto import Producto
from app.core.interfaces.producto_repository import IProductoRepository


class ProductoUseCases:
    """Casos de uso relacionados con productos"""
    
    def __init__(self, producto_repository: IProductoRepository):
        """
        Inyección de dependencias - depende de la interfaz, no de la implementación
        """
        self.producto_repository = producto_repository
    
    def crear_producto(self, producto: Producto) -> tuple[bool, Optional[str], Optional[Producto]]:
        """Crea un nuevo producto validando las reglas de negocio"""
        # Validar reglas de negocio
        es_valido, mensaje_error = producto.validar()
        if not es_valido:
            return False, mensaje_error, None
        
        # Persistir el producto
        producto_creado = self.producto_repository.crear(producto)
        return True, None, producto_creado
    
    def obtener_producto(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID"""
        return self.producto_repository.obtener_por_id(id)
    
    def listar_productos(self) -> List[Producto]:
        """Lista todos los productos"""
        return self.producto_repository.obtener_todos()
    
    def actualizar_producto(self, producto: Producto) -> tuple[bool, Optional[str]]:
        """Actualiza un producto existente"""
        # Validar reglas de negocio
        es_valido, mensaje_error = producto.validar()
        if not es_valido:
            return False, mensaje_error
        
        # Verificar que el producto existe
        producto_existente = self.producto_repository.obtener_por_id(producto.id)
        if not producto_existente:
            return False, "Producto no encontrado"
        
        # Actualizar
        exito = self.producto_repository.actualizar(producto)
        if not exito:
            return False, "Error al actualizar el producto"
        
        return True, None
    
    def eliminar_producto(self, id: int) -> tuple[bool, Optional[str]]:
        """Elimina un producto"""
        # Verificar que el producto existe
        producto = self.producto_repository.obtener_por_id(id)
        if not producto:
            return False, "Producto no encontrado"
        
        # Eliminar
        exito = self.producto_repository.eliminar(id)
        if not exito:
            return False, "Error al eliminar el producto"
        
        return True, None
    
    def obtener_productos_por_categoria(self, categoria_id: int) -> List[Producto]:
        """Obtiene productos de una categoría específica"""
        return self.producto_repository.obtener_por_categoria(categoria_id)
    
    def obtener_productos_bajo_stock(self) -> List[Producto]:
        """
        Obtiene productos que necesitan reabastecimiento
        Usa la lógica de negocio del dominio
        """
        productos = self.producto_repository.obtener_productos_bajo_stock()
        return [p for p in productos if p.necesita_reabastecimiento()]
    
    def ajustar_stock(self, id: int, cantidad: int) -> tuple[bool, Optional[str]]:
        """Ajusta el stock de un producto"""
        producto = self.producto_repository.obtener_por_id(id)
        if not producto:
            return False, "Producto no encontrado"
        
        # Usar la lógica de negocio del dominio
        if not producto.actualizar_stock(cantidad):
            return False, "Stock insuficiente para realizar la operación"
        
        # Persistir cambios
        exito = self.producto_repository.actualizar(producto)
        if not exito:
            return False, "Error al actualizar el stock"
        
        return True, None

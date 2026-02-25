"""
Entidad Producto - Capa de Dominio
No depende de ninguna tecnología externa
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Producto:
    """Entidad de dominio que representa un producto"""
    nombre: str
    descripcion: str
    precio: float
    cantidad_stock: int
    stock_minimo: int
    categoria_id: int
    proveedor_id: int
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    def necesita_reabastecimiento(self) -> bool:
        """
        Lógica de negocio pura: determina si el producto necesita reabastecimiento
        Esta lógica NO depende de la UI ni de la base de datos
        """
        return self.cantidad_stock <= self.stock_minimo
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """Valida las reglas de negocio del producto"""
        if not self.nombre or len(self.nombre.strip()) == 0:
            return False, "El nombre del producto es requerido"
        
        if self.precio < 0:
            return False, "El precio no puede ser negativo"
        
        if self.cantidad_stock < 0:
            return False, "La cantidad en stock no puede ser negativa"
        
        if self.stock_minimo < 0:
            return False, "El stock mínimo no puede ser negativo"
        
        return True, None
    
    def actualizar_stock(self, cantidad: int) -> bool:
        """Actualiza el stock del producto"""
        nuevo_stock = self.cantidad_stock + cantidad
        if nuevo_stock < 0:
            return False
        self.cantidad_stock = nuevo_stock
        return True

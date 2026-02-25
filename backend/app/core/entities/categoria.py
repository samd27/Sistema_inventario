"""
Entidad Categoria - Capa de Dominio
No depende de ninguna tecnología externa
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Categoria:
    """Entidad de dominio que representa una categoría"""
    nombre: str
    descripcion: str
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """Valida las reglas de negocio de la categoría"""
        if not self.nombre or len(self.nombre.strip()) == 0:
            return False, "El nombre de la categoría es requerido"
        
        if len(self.nombre) > 100:
            return False, "El nombre de la categoría no puede exceder 100 caracteres"
        
        return True, None

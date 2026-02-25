"""
Entidad Proveedor - Capa de Dominio
No depende de ninguna tecnología externa
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import re


@dataclass
class Proveedor:
    """Entidad de dominio que representa un proveedor"""
    nombre: str
    contacto: str
    telefono: str
    email: str
    direccion: str
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    
    def validar(self) -> tuple[bool, Optional[str]]:
        """Valida las reglas de negocio del proveedor"""
        if not self.nombre or len(self.nombre.strip()) == 0:
            return False, "El nombre del proveedor es requerido"
        
        if not self.contacto or len(self.contacto.strip()) == 0:
            return False, "El nombre de contacto es requerido"
        
        if not self.validar_email():
            return False, "El formato del email no es válido"
        
        if not self.telefono or len(self.telefono.strip()) == 0:
            return False, "El teléfono es requerido"
        
        return True, None
    
    def validar_email(self) -> bool:
        """Valida el formato del email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, self.email))

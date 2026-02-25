"""
Implementación del Repositorio de Productos
"""
from typing import List, Optional
from app.core.entities.producto import Producto
from app.core.interfaces.producto_repository import IProductoRepository
from app.data.models.producto_model import ProductoModel
from app.data.database import db


class ProductoRepository(IProductoRepository):
    """Implementación del repositorio de productos usando SQLAlchemy"""
    
    def crear(self, producto: Producto) -> Producto:
        """Crea un nuevo producto en la base de datos"""
        modelo = ProductoModel.from_entity(producto)
        db.session.add(modelo)
        db.session.commit()
        return modelo.to_entity()
    
    def obtener_por_id(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID"""
        modelo = ProductoModel.query.get(id)
        return modelo.to_entity() if modelo else None
    
    def obtener_todos(self) -> List[Producto]:
        """Obtiene todos los productos"""
        modelos = ProductoModel.query.all()
        return [modelo.to_entity() for modelo in modelos]
    
    def actualizar(self, producto: Producto) -> bool:
        """Actualiza un producto existente"""
        modelo = ProductoModel.query.get(producto.id)
        if not modelo:
            return False
        
        modelo.nombre = producto.nombre
        modelo.descripcion = producto.descripcion
        modelo.precio = producto.precio
        modelo.cantidad_stock = producto.cantidad_stock
        modelo.stock_minimo = producto.stock_minimo
        modelo.categoria_id = producto.categoria_id
        modelo.proveedor_id = producto.proveedor_id
        db.session.commit()
        return True
    
    def eliminar(self, id: int) -> bool:
        """Elimina un producto"""
        modelo = ProductoModel.query.get(id)
        if not modelo:
            return False
        
        db.session.delete(modelo)
        db.session.commit()
        return True
    
    def obtener_por_categoria(self, categoria_id: int) -> List[Producto]:
        """Obtiene productos por categoría"""
        modelos = ProductoModel.query.filter_by(categoria_id=categoria_id).all()
        return [modelo.to_entity() for modelo in modelos]
    
    def obtener_productos_bajo_stock(self) -> List[Producto]:
        """Obtiene productos que están por debajo o igual al stock mínimo"""
        modelos = ProductoModel.query.filter(
            ProductoModel.cantidad_stock <= ProductoModel.stock_minimo
        ).all()
        return [modelo.to_entity() for modelo in modelos]

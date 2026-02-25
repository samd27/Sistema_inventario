from flask import Blueprint, jsonify, request
from app.core.use_cases.producto_use_cases import ProductoUseCases
from app.core.use_cases.categoria_use_cases import CategoriaUseCases
from app.core.use_cases.proveedor_use_cases import ProveedorUseCases
from app.core.entities.producto import Producto
from datetime import datetime

def create_producto_api(producto_use_cases: ProductoUseCases, 
                        categoria_use_cases: CategoriaUseCases,
                        proveedor_use_cases: ProveedorUseCases):
    api = Blueprint('producto_api', __name__, url_prefix='/api/productos')
    
    def producto_to_dict(producto, incluir_relaciones=False):
        """Convierte un producto a diccionario"""
        data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
            'precio': float(producto.precio),
            'stock': producto.cantidad_stock,
            'stock_minimo': producto.stock_minimo,
            'categoria_id': producto.categoria_id,
            'proveedor_id': producto.proveedor_id,
            'necesita_reabastecimiento': producto.necesita_reabastecimiento(),
            'fecha_creacion': producto.fecha_creacion.isoformat() if producto.fecha_creacion else None,
            'fecha_actualizacion': producto.fecha_actualizacion.isoformat() if producto.fecha_actualizacion else None
        }
        
        if incluir_relaciones:
            categoria = categoria_use_cases.obtener_categoria(producto.categoria_id) if producto.categoria_id else None
            proveedor = proveedor_use_cases.obtener_proveedor(producto.proveedor_id) if producto.proveedor_id else None
            data['categoria_nombre'] = categoria.nombre if categoria else None
            data['proveedor_nombre'] = proveedor.nombre if proveedor else None
        
        return data
    
    @api.route('/', methods=['GET'])
    def listar():
        """Obtiene todos los productos"""
        try:
            productos = producto_use_cases.listar_productos()
            return jsonify({
                'success': True,
                'data': [producto_to_dict(p, incluir_relaciones=True) for p in productos]
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api.route('/<int:id>', methods=['GET'])
    def obtener(id):
        """Obtiene un producto por ID"""
        try:
            producto = producto_use_cases.obtener_producto(id)
            if not producto:
                return jsonify({
                    'success': False,
                    'error': 'Producto no encontrado'
                }), 404
            
            data = producto_to_dict(producto, incluir_relaciones=True)
            
            return jsonify({
                'success': True,
                'data': data
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api.route('/', methods=['POST'])
    def crear():
        """Crea un nuevo producto"""
        try:
            data = request.get_json()
            
            producto = Producto(
                nombre=data['nombre'],
                descripcion=data.get('descripcion', ''),
                precio=float(data['precio']),
                cantidad_stock=int(data['stock']),
                stock_minimo=int(data['stock_minimo']),
                categoria_id=int(data['categoria_id']),
                proveedor_id=int(data['proveedor_id'])
            )
            
            exito, mensaje, producto_creado = producto_use_cases.crear_producto(producto)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje
                }), 400
            
            return jsonify({
                'success': True,
                'message': 'Producto creado exitosamente',
                'data': producto_to_dict(producto_creado)
            }), 201
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @api.route('/<int:id>', methods=['PUT'])
    def actualizar(id):
        """Actualiza un producto existente"""
        try:
            data = request.get_json()
            
            producto = Producto(
                id=id,
                nombre=data['nombre'],
                descripcion=data.get('descripcion', ''),
                precio=float(data['precio']),
                cantidad_stock=int(data['stock']),
                stock_minimo=int(data['stock_minimo']),
                categoria_id=int(data['categoria_id']),
                proveedor_id=int(data['proveedor_id'])
            )
            
            exito, mensaje = producto_use_cases.actualizar_producto(producto)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje or 'Error al actualizar producto'
                }), 404 if mensaje and 'no encontrado' in mensaje.lower() else 400
            
            return jsonify({
                'success': True,
                'message': 'Producto actualizado exitosamente',
                'data': producto_to_dict(producto)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @api.route('/<int:id>', methods=['DELETE'])
    def eliminar(id):
        """Elimina un producto"""
        try:
            exito, mensaje = producto_use_cases.eliminar_producto(id)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Producto eliminado exitosamente'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @api.route('/bajo-stock', methods=['GET'])
    def bajo_stock():
        """Obtiene productos con stock bajo"""
        try:
            productos = producto_use_cases.obtener_productos_bajo_stock()
            return jsonify({
                'success': True,
                'data': [producto_to_dict(p) for p in productos]
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    return api

from flask import Blueprint, jsonify, request
from app.core.use_cases.proveedor_use_cases import ProveedorUseCases
from app.core.entities.proveedor import Proveedor

def create_proveedor_api(proveedor_use_cases: ProveedorUseCases):
    api = Blueprint('proveedor_api', __name__, url_prefix='/api/proveedores')
    
    def proveedor_to_dict(proveedor):
        """Convierte un proveedor a diccionario"""
        return {
            'id': proveedor.id,
            'nombre': proveedor.nombre,
            'contacto': proveedor.contacto,
            'telefono': proveedor.telefono,
            'email': proveedor.email,
            'direccion': proveedor.direccion,
            'fecha_creacion': proveedor.fecha_creacion.isoformat() if proveedor.fecha_creacion else None
        }
    
    @api.route('/', methods=['GET'])
    def listar():
        """Obtiene todos los proveedores"""
        try:
            proveedores = proveedor_use_cases.listar_proveedores()
            return jsonify({
                'success': True,
                'data': [proveedor_to_dict(p) for p in proveedores]
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api.route('/<int:id>', methods=['GET'])
    def obtener(id):
        """Obtiene un proveedor por ID"""
        try:
            proveedor = proveedor_use_cases.obtener_proveedor(id)
            if not proveedor:
                return jsonify({
                    'success': False,
                    'error': 'Proveedor no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'data': proveedor_to_dict(proveedor)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api.route('/', methods=['POST'])
    def crear():
        """Crea un nuevo proveedor"""
        try:
            data = request.get_json()
            
            proveedor = Proveedor(
                nombre=data['nombre'],
                contacto=data.get('contacto', ''),
                telefono=data.get('telefono', ''),
                email=data.get('email', ''),
                direccion=data.get('direccion', '')
            )
            
            exito, mensaje, proveedor_creado = proveedor_use_cases.crear_proveedor(proveedor)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje
                }), 400
            
            return jsonify({
                'success': True,
                'message': 'Proveedor creado exitosamente',
                'data': proveedor_to_dict(proveedor_creado)
            }), 201
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @api.route('/<int:id>', methods=['PUT'])
    def actualizar(id):
        """Actualiza un proveedor existente"""
        try:
            data = request.get_json()
            
            proveedor = Proveedor(
                id=id,
                nombre=data['nombre'],
                contacto=data.get('contacto', ''),
                telefono=data.get('telefono', ''),
                email=data.get('email', ''),
                direccion=data.get('direccion', '')
            )
            
            exito, mensaje = proveedor_use_cases.actualizar_proveedor(proveedor)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje or 'Error al actualizar proveedor'
                }), 404 if mensaje and 'no encontrado' in mensaje.lower() else 400
            
            return jsonify({
                'success': True,
                'message': 'Proveedor actualizado exitosamente',
                'data': proveedor_to_dict(proveedor)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @api.route('/<int:id>', methods=['DELETE'])
    def eliminar(id):
        """Elimina un proveedor"""
        try:
            exito, mensaje = proveedor_use_cases.eliminar_proveedor(id)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Proveedor eliminado exitosamente'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    return api

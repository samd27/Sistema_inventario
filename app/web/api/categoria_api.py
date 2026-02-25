from flask import Blueprint, jsonify, request
from app.core.use_cases.categoria_use_cases import CategoriaUseCases
from app.core.entities.categoria import Categoria

def create_categoria_api(categoria_use_cases: CategoriaUseCases):
    api = Blueprint('categoria_api', __name__, url_prefix='/api/categorias')
    
    def categoria_to_dict(categoria):
        """Convierte una categoría a diccionario"""
        return {
            'id': categoria.id,
            'nombre': categoria.nombre,
            'descripcion': categoria.descripcion,
            'fecha_creacion': categoria.fecha_creacion.isoformat() if categoria.fecha_creacion else None
        }
    
    @api.route('/', methods=['GET'])
    def listar():
        """Obtiene todas las categorías"""
        try:
            categorias = categoria_use_cases.listar_categorias()
            return jsonify({
                'success': True,
                'data': [categoria_to_dict(c) for c in categorias]
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api.route('/<int:id>', methods=['GET'])
    def obtener(id):
        """Obtiene una categoría por ID"""
        try:
            categoria = categoria_use_cases.obtener_categoria(id)
            if not categoria:
                return jsonify({
                    'success': False,
                    'error': 'Categoría no encontrada'
                }), 404
            
            return jsonify({
                'success': True,
                'data': categoria_to_dict(categoria)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @api.route('/', methods=['POST'])
    def crear():
        """Crea una nueva categoría"""
        try:
            data = request.get_json()
            
            categoria = Categoria(
                nombre=data['nombre'],
                descripcion=data.get('descripcion', '')
            )
            
            exito, mensaje, categoria_creada = categoria_use_cases.crear_categoria(categoria)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje
                }), 400
            
            return jsonify({
                'success': True,
                'message': 'Categoría creada exitosamente',
                'data': categoria_to_dict(categoria_creada)
            }), 201
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @api.route('/<int:id>', methods=['PUT'])
    def actualizar(id):
        """Actualiza una categoría existente"""
        try:
            data = request.get_json()
            
            categoria = Categoria(
                id=id,
                nombre=data['nombre'],
                descripcion=data.get('descripcion', '')
            )
            
            exito, mensaje = categoria_use_cases.actualizar_categoria(categoria)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje or 'Error al actualizar categoría'
                }), 404 if mensaje and 'no encontrada' in mensaje.lower() else 400
            
            return jsonify({
                'success': True,
                'message': 'Categoría actualizada exitosamente',
                'data': categoria_to_dict(categoria)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    @api.route('/<int:id>', methods=['DELETE'])
    def eliminar(id):
        """Elimina una categoría"""
        try:
            exito, mensaje = categoria_use_cases.eliminar_categoria(id)
            
            if not exito:
                return jsonify({
                    'success': False,
                    'error': mensaje
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Categoría eliminada exitosamente'
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
    
    return api

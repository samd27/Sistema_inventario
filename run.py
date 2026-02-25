"""
Punto de entrada de la aplicación Flask
Aquí se ensamblan todas las capas (Dependency Injection)
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS
from config.config import config
from app.data.database import db, init_db

# Importar modelos para que SQLAlchemy los reconozca
from app.data.models.categoria_model import CategoriaModel
from app.data.models.proveedor_model import ProveedorModel
from app.data.models.producto_model import ProductoModel

# Importar repositorios (adaptadores)
from app.data.repositories.categoria_repository import CategoriaRepository
from app.data.repositories.proveedor_repository import ProveedorRepository
from app.data.repositories.producto_repository import ProductoRepository

# Importar casos de uso
from app.core.use_cases.categoria_use_cases import CategoriaUseCases
from app.core.use_cases.proveedor_use_cases import ProveedorUseCases
from app.core.use_cases.producto_use_cases import ProductoUseCases

# Importar APIs REST
from app.web.api.categoria_api import create_categoria_api
from app.web.api.proveedor_api import create_proveedor_api
from app.web.api.producto_api import create_producto_api


def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Habilitar CORS para permitir peticiones desde React
    CORS(app)
    
    # Inicializar base de datos
    db.init_app(app)
    
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        # Inyección de dependencias (Wiring de las capas)
        # Capa de Datos: Repositorios
        categoria_repo = CategoriaRepository()
        proveedor_repo = ProveedorRepository()
        producto_repo = ProductoRepository()
        
        # Capa de Negocio: Casos de uso
        categoria_uc = CategoriaUseCases(categoria_repo)
        proveedor_uc = ProveedorUseCases(proveedor_repo)
        producto_uc = ProductoUseCases(producto_repo)
        
        # Capa de API REST (para React)
        categoria_api = create_categoria_api(categoria_uc)
        proveedor_api = create_proveedor_api(proveedor_uc)
        producto_api = create_producto_api(producto_uc, categoria_uc, proveedor_uc)
        
        # Registrar blueprints de APIs REST
        app.register_blueprint(categoria_api)
        app.register_blueprint(proveedor_api)
        app.register_blueprint(producto_api)
    
    # Ruta principal - redirige al frontend React
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Tienda Inventario API',
            'version': '1.0.0',
            'frontend': 'http://localhost:5173'
        })
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    print("\n" + "="*50)
    print("🌐 Servidor Flask")
    print("="*50)
    print(f"📍 URL: http://127.0.0.1:8080")
    print(f"🔧 Modo: Desarrollo")
    print(f"💡 Presiona CTRL+C para detener\n")
    app.run(debug=True, host='127.0.0.1', port=8080)

"""
Script de inicialización seguro para Railway
Solo crea las tablas si no existen, no borra datos
"""
import os
import sys

# Asegurar que el directorio raíz está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import create_app
from app.data.database import db


def safe_init_db():
    """Inicializa la base de datos de forma segura"""
    print("🔧 Inicializando base de datos...")
    
    # Determinar entorno
    env = os.environ.get('FLASK_ENV', 'production')
    app = create_app(env)
    
    with app.app_context():
        try:
            # Solo crear tablas si no existen (no borra datos)
            db.create_all()
            print("✅ Tablas de base de datos verificadas/creadas exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al inicializar base de datos: {e}")
            return False


if __name__ == '__main__':
    success = safe_init_db()
    sys.exit(0 if success else 1)

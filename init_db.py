"""
Script de inicialización con datos de prueba
Ejecuta este script para poblar la base de datos con datos de ejemplo
"""
from run import create_app
from app.data.database import db
from app.core.entities.categoria import Categoria
from app.core.entities.proveedor import Proveedor
from app.core.entities.producto import Producto
from app.data.repositories.categoria_repository import CategoriaRepository
from app.data.repositories.proveedor_repository import ProveedorRepository
from app.data.repositories.producto_repository import ProductoRepository


def init_data():
    """Inicializa la base de datos con datos de prueba"""
    app = create_app('development')
    
    with app.app_context():
        # Limpiar datos existentes
        db.drop_all()
        db.create_all()
        
        print("🗄️  Base de datos creada exitosamente")
        
        # Crear repositorios
        categoria_repo = CategoriaRepository()
        proveedor_repo = ProveedorRepository()
        producto_repo = ProductoRepository()
        
        # Crear categorías
        print("\n📁 Creando categorías...")
        categorias = [
            Categoria(nombre="Electrónica", descripcion="Productos electrónicos y tecnología"),
            Categoria(nombre="Alimentos", descripcion="Productos alimenticios y bebidas"),
            Categoria(nombre="Ropa", descripcion="Vestimenta y accesorios"),
            Categoria(nombre="Hogar", descripcion="Artículos para el hogar"),
            Categoria(nombre="Deportes", descripcion="Equipamiento deportivo y fitness"),
        ]
        
        categorias_creadas = []
        for cat in categorias:
            cat_creada = categoria_repo.crear(cat)
            categorias_creadas.append(cat_creada)
            print(f"   ✓ {cat_creada.nombre}")
        
        # Crear proveedores
        print("\n🏢 Creando proveedores...")
        proveedores = [
            Proveedor(
                nombre="TechSupply SA",
                contacto="Juan Pérez",
                telefono="555-0101",
                email="contacto@techsupply.com",
                direccion="Av. Tecnología 123, Ciudad"
            ),
            Proveedor(
                nombre="AlimentosPlus",
                contacto="María González",
                telefono="555-0202",
                email="ventas@alimentosplus.com",
                direccion="Calle Comercio 456, Ciudad"
            ),
            Proveedor(
                nombre="Moda y Estilo",
                contacto="Carlos Rodríguez",
                telefono="555-0303",
                email="info@modayestilo.com",
                direccion="Boulevard Moda 789, Ciudad"
            ),
            Proveedor(
                nombre="Hogar Confort",
                contacto="Ana Martínez",
                telefono="555-0404",
                email="contacto@hogarconfort.com",
                direccion="Av. Hogar 321, Ciudad"
            ),
        ]
        
        proveedores_creados = []
        for prov in proveedores:
            prov_creado = proveedor_repo.crear(prov)
            proveedores_creados.append(prov_creado)
            print(f"   ✓ {prov_creado.nombre}")
        
        # Crear productos
        print("\n📦 Creando productos...")
        productos = [
            # Electrónica
            Producto(
                nombre="Laptop HP Pavilion",
                descripcion="Laptop 15.6 pulgadas, Intel i5, 8GB RAM, 256GB SSD",
                precio=899.99,
                cantidad_stock=15,
                stock_minimo=5,
                categoria_id=categorias_creadas[0].id,
                proveedor_id=proveedores_creados[0].id
            ),
            Producto(
                nombre="Mouse Inalámbrico Logitech",
                descripcion="Mouse ergonómico con conexión Bluetooth",
                precio=29.99,
                cantidad_stock=3,
                stock_minimo=10,  # Stock bajo
                categoria_id=categorias_creadas[0].id,
                proveedor_id=proveedores_creados[0].id
            ),
            Producto(
                nombre="Teclado Mecánico RGB",
                descripcion="Teclado gaming con iluminación RGB",
                precio=79.99,
                cantidad_stock=8,
                stock_minimo=5,
                categoria_id=categorias_creadas[0].id,
                proveedor_id=proveedores_creados[0].id
            ),
            # Alimentos
            Producto(
                nombre="Arroz Integral 1kg",
                descripcion="Arroz integral de grano largo",
                precio=4.99,
                cantidad_stock=50,
                stock_minimo=20,
                categoria_id=categorias_creadas[1].id,
                proveedor_id=proveedores_creados[1].id
            ),
            Producto(
                nombre="Aceite de Oliva Extra Virgen",
                descripcion="Aceite de oliva 500ml",
                precio=12.99,
                cantidad_stock=5,
                stock_minimo=15,  # Stock bajo
                categoria_id=categorias_creadas[1].id,
                proveedor_id=proveedores_creados[1].id
            ),
            # Ropa
            Producto(
                nombre="Camiseta Básica Algodón",
                descripcion="Camiseta 100% algodón, talla M",
                precio=19.99,
                cantidad_stock=30,
                stock_minimo=10,
                categoria_id=categorias_creadas[2].id,
                proveedor_id=proveedores_creados[2].id
            ),
            Producto(
                nombre="Jeans Clásicos",
                descripcion="Pantalón jeans azul, corte regular",
                precio=49.99,
                cantidad_stock=2,
                stock_minimo=8,  # Stock bajo
                categoria_id=categorias_creadas[2].id,
                proveedor_id=proveedores_creados[2].id
            ),
            # Hogar
            Producto(
                nombre="Juego de Sábanas Queen",
                descripcion="Sábanas de microfibra, 4 piezas",
                precio=39.99,
                cantidad_stock=12,
                stock_minimo=6,
                categoria_id=categorias_creadas[3].id,
                proveedor_id=proveedores_creados[3].id
            ),
            # Deportes
            Producto(
                nombre="Mancuernas 5kg (par)",
                descripcion="Par de mancuernas con recubrimiento de neopreno",
                precio=34.99,
                cantidad_stock=20,
                stock_minimo=8,
                categoria_id=categorias_creadas[4].id,
                proveedor_id=proveedores_creados[0].id
            ),
        ]
        
        productos_creados = []
        bajo_stock = 0
        for prod in productos:
            prod_creado = producto_repo.crear(prod)
            productos_creados.append(prod_creado)
            status = "⚠️  STOCK BAJO" if prod_creado.necesita_reabastecimiento() else "✓"
            if prod_creado.necesita_reabastecimiento():
                bajo_stock += 1
            print(f"   {status} {prod_creado.nombre} (Stock: {prod_creado.cantidad_stock})")
        
        print(f"\n✅ Inicialización completada exitosamente!")
        print(f"📊 Resumen:")
        print(f"   - Categorías: {len(categorias_creadas)}")
        print(f"   - Proveedores: {len(proveedores_creados)}")
        print(f"   - Productos: {len(productos_creados)}")
        print(f"   - Productos con stock bajo: {bajo_stock}")
        print(f"\n🚀 Puedes ejecutar la aplicación con: python app.py")


if __name__ == '__main__':
    init_data()

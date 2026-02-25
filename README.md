# Sistema de Gestión de Inventario para Tienda

Sistema web de gestión de inventario con arquitectura en capas desacoplada, implementado en Flask y TiDB Cloud.

## 🏗️ Arquitectura

Este proyecto implementa una **Arquitectura en Capas (Layered Architecture)** completamente desacoplada:

### Estructura de Capas

```
┌─────────────────────────────────────┐
│   Capa de Presentación (web)       │
│   - Controladores Flask             │
│   - Templates HTML                  │
│   - Manejo de HTTP requests         │
└─────────────────┬───────────────────┘
                  │ Depende de ↓
┌─────────────────────────────────────┐
│   Capa de Negocio (core)            │
│   - Casos de Uso                    │
│   - Entidades de Dominio            │
│   - Interfaces (Puertos)            │
│   - Lógica de Negocio Pura          │
└─────────────────┬───────────────────┘
                  ↑ Define interfaces
┌─────────────────────────────────────┐
│   Capa de Datos (data)              │
│   - Repositorios (Adaptadores)      │
│   - Modelos SQLAlchemy              │
│   - Persistencia en BD              │
└─────────────────────────────────────┘
```

### Principios Arquitectónicos Aplicados

1. **Inversión de Dependencias (DIP)**: La capa de dominio define interfaces, la capa de datos las implementa
2. **Separación de Responsabilidades**: Cada capa tiene responsabilidades bien definidas
3. **Independencia del Framework**: La lógica de negocio no depende de Flask ni SQLAlchemy
4. **Testabilidad**: Cada capa puede ser testeada independientemente
5. **Mantenibilidad**: Cambios en una capa no afectan a las demás
6. **Portabilidad**: Puedes cambiar la BD o UI sin tocar la lógica de negocio

## 📁 Estructura del Proyecto

```
Tienda/
├── app/
│   ├── core/                    # Capa de Dominio (NO depende de nada)
│   │   ├── entities/            # Entidades de dominio
│   │   │   ├── producto.py
│   │   │   ├── categoria.py
│   │   │   └── proveedor.py
│   │   ├── interfaces/          # Puertos (interfaces de repositorios)
│   │   │   ├── producto_repository.py
│   │   │   ├── categoria_repository.py
│   │   │   └── proveedor_repository.py
│   │   └── use_cases/           # Casos de uso (lógica de negocio)
│   │       ├── producto_use_cases.py
│   │       ├── categoria_use_cases.py
│   │       └── proveedor_use_cases.py
│   │
│   ├── data/                    # Capa de Datos (Adaptadores)
│   │   ├── models/              # Modelos SQLAlchemy
│   │   │   ├── producto_model.py
│   │   │   ├── categoria_model.py
│   │   │   └── proveedor_model.py
│   │   ├── repositories/        # Implementación de repositorios
│   │   │   ├── producto_repository.py
│   │   │   ├── categoria_repository.py
│   │   │   └── proveedor_repository.py
│   │   └── database.py          # Configuración de SQLAlchemy
│   │
│   └── web/                     # Capa de Presentación
│       └── controllers/         # Controladores Flask
│           ├── producto_controller.py
│           ├── categoria_controller.py
│           └── proveedor_controller.py
│
├── config/                      # Configuración
│   └── config.py
├── templates/                   # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── productos/
│   ├── categorias/
│   └── proveedores/
├── app.py                       # Punto de entrada
├── requirements.txt
└── README.md
```

## ✨ Características

- ✅ **CRUD completo** de Productos, Categorías y Proveedores
- ✅ **Alertas de Stock Bajo**: Detecta automáticamente productos que necesitan reabastecimiento
- ✅ **Validaciones de Negocio**: Email, precios, stock, etc.
- ✅ **Arquitectura Desacoplada**: Máxima mantenibilidad y portabilidad
- ✅ **Base de Datos**: Compatible con TiDB Cloud y MySQL
- ✅ **Interfaz Moderna**: UI responsive y atractiva

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- TiDB Cloud account (o MySQL local para desarrollo)

### Paso 1: Clonar el repositorio

```bash
git clone <tu-repositorio>
cd Tienda
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env`:

```env
SECRET_KEY=tu-clave-secreta-super-segura

# Para TiDB Cloud
DATABASE_URL=mysql+pymysql://usuario:contraseña@host:4000/tienda_inventario?ssl_ca=ca.pem

# Para MySQL local (desarrollo)
DATABASE_URL=mysql+pymysql://root:@localhost:3306/tienda_inventario?charset=utf8mb4
```

### Paso 5: Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 🗄️ Configuración de TiDB Cloud

1. Crea una cuenta en [TiDB Cloud](https://tidbcloud.com/)
2. Crea un nuevo cluster
3. Descarga el certificado SSL (ca.pem)
4. Obtén las credenciales de conexión
5. Actualiza el `DATABASE_URL` en tu archivo `.env`

Ejemplo de cadena de conexión para TiDB:

```
mysql+pymysql://usuario.root:contraseña@gateway01.us-west-2.prod.aws.tidbcloud.com:4000/tienda_inventario?ssl_ca=ca.pem&ssl_verify_cert=true&ssl_verify_identity=true
```

## 📖 Uso

### Página Principal
Navega a `http://localhost:5000` para ver el dashboard principal con acceso a todas las secciones.

### Gestión de Categorías
1. Ir a "Categorías"
2. Crear categorías (ej: Electrónica, Alimentos, Ropa)
3. Las categorías son necesarias antes de crear productos

### Gestión de Proveedores
1. Ir a "Proveedores"
2. Registrar proveedores con su información de contacto
3. Validación automática de formato de email

### Gestión de Productos
1. Ir a "Productos"
2. Crear productos asociándolos a categorías y proveedores
3. Establecer stock mínimo para alertas automáticas
4. Ver productos con stock bajo en la sección "Stock Bajo"

## 🧪 Ejemplo de Lógica de Negocio Desacoplada

Un ejemplo clave del desacoplamiento es la función `necesita_reabastecimiento()`:

```python
# En app/core/entities/producto.py (Capa de Dominio)
class Producto:
    def necesita_reabastecimiento(self) -> bool:
        """
        Lógica de negocio PURA - No depende de BD ni UI
        """
        return self.cantidad_stock <= self.stock_minimo
```

Esta lógica:
- ✅ **No depende** de Flask
- ✅ **No depende** de SQLAlchemy
- ✅ **No depende** de TiDB Cloud
- ✅ Puede ser testeada sin framework
- ✅ Permanece intacta si cambias la UI o la BD

## 🎯 Atributos de Calidad

### Mantenibilidad
- Código modular y bien organizado
- Responsabilidades claramente separadas
- Fácil de entender y modificar

### Portabilidad
- Puedes cambiar de MySQL a PostgreSQL sin tocar la lógica de negocio
- Puedes cambiar de Flask a FastAPI sin tocar la lógica de negocio
- Los archivos de la capa de dominio son completamente independientes

### Testabilidad
- Cada capa puede ser testeada independientemente
- Mock de repositorios fácil gracias a las interfaces
- Lógica de negocio testeable sin base de datos

## 🔧 Tecnologías Utilizadas

- **Backend**: Flask 3.0
- **ORM**: SQLAlchemy
- **Base de Datos**: TiDB Cloud (compatible con MySQL)
- **Arquitectura**: Layered Architecture (Clean Architecture principles)
- **Python**: 3.8+

## 📝 Notas Importantes

1. **Seguridad**: Cambia la `SECRET_KEY` en producción
2. **SSL**: En producción con TiDB Cloud, siempre usa SSL
3. **Migraciones**: Para producción, considera usar Flask-Migrate (Alembic)
4. **Testing**: Añade tests unitarios para cada capa

## 🤝 Contribuciones

Este es un proyecto educativo que demuestra principios de arquitectura de software limpia y desacoplada.

## 📄 Licencia

MIT License - Proyecto educativo para curso de Arquitectura de Software

## 👨‍💻 Autor

Proyecto desarrollado como parte del curso de Arquitectura de Software (AS) - SEM8

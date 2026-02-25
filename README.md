# Sistema de Gestion de Inventario

Sistema web full-stack de gestion de inventario con arquitectura en capas desacoplada.
Backend en **Flask** (API REST) y frontend en **React** con **Vite**.
Base de datos MySQL / TiDB Cloud.

## Arquitectura

Este proyecto implementa una **Arquitectura en Capas (Layered Architecture)** completamente desacoplada:

```
+-------------------------------------+
|  Frontend (React + Vite)            |
|  - SPA con React Router             |
|  - Consumo de API REST via Axios    |
|  - Animaciones con Framer Motion    |
|  - Puerto: 5173                     |
+-----------------+-------------------+
                  | HTTP / JSON
+-----------------v-------------------+
|  Capa de Presentacion (web/api)     |
|  - Blueprints Flask (REST API)      |
|  - Serializacion JSON               |
|  - Puerto: 8080                     |
+-----------------+-------------------+
                  | Depende de
+-----------------v-------------------+
|  Capa de Negocio (core)             |
|  - Casos de Uso                     |
|  - Entidades de Dominio             |
|  - Interfaces (Puertos)             |
|  - Logica de Negocio Pura           |
+-----------------+-------------------+
                  ^ Define interfaces
+-----------------+-------------------+
|  Capa de Datos (data)               |
|  - Repositorios (Adaptadores)       |
|  - Modelos SQLAlchemy               |
|  - Persistencia en BD               |
+-------------------------------------+
```

### Principios Arquitectonicos

1. **Inversion de Dependencias (DIP)**: La capa de dominio define interfaces, la capa de datos las implementa
2. **Separacion de Responsabilidades**: Cada capa tiene responsabilidades bien definidas
3. **Independencia del Framework**: La logica de negocio no depende de Flask ni SQLAlchemy
4. **Testabilidad**: Cada capa puede ser testeada independientemente
5. **Mantenibilidad**: Cambios en una capa no afectan a las demas
6. **Portabilidad**: Puedes cambiar la BD o UI sin tocar la logica de negocio

> Para mas detalles sobre la arquitectura, ver [ARCHITECTURE.md](ARCHITECTURE.md).

## Estructura del Proyecto

```
Sistema_inventario/
|-- backend/                         # Servidor Flask (API REST)
|   |-- app/
|   |   |-- core/                    # Capa de Dominio (NO depende de nada)
|   |   |   |-- entities/            # Entidades de dominio puras
|   |   |   |   |-- producto.py
|   |   |   |   |-- categoria.py
|   |   |   |   +-- proveedor.py
|   |   |   |-- interfaces/          # Puertos (interfaces abstractas)
|   |   |   |   |-- producto_repository.py
|   |   |   |   |-- categoria_repository.py
|   |   |   |   +-- proveedor_repository.py
|   |   |   +-- use_cases/           # Casos de uso (logica de negocio)
|   |   |       |-- producto_use_cases.py
|   |   |       |-- categoria_use_cases.py
|   |   |       +-- proveedor_use_cases.py
|   |   |
|   |   |-- data/                    # Capa de Datos (Adaptadores)
|   |   |   |-- database.py          # Configuracion SQLAlchemy
|   |   |   |-- models/              # Modelos ORM
|   |   |   |   |-- producto_model.py
|   |   |   |   |-- categoria_model.py
|   |   |   |   +-- proveedor_model.py
|   |   |   +-- repositories/        # Implementacion de repositorios
|   |   |       |-- producto_repository.py
|   |   |       |-- categoria_repository.py
|   |   |       +-- proveedor_repository.py
|   |   |
|   |   +-- web/                     # Capa de Presentacion (API REST)
|   |       +-- api/
|   |           |-- producto_api.py
|   |           |-- categoria_api.py
|   |           +-- proveedor_api.py
|   |
|   |-- config/
|   |   +-- config.py               # Configuracion dev / production
|   |-- run.py                       # Punto de entrada Flask (puerto 8080)
|   |-- init_db.py                   # Datos de prueba
|   |-- requirements.txt             # Dependencias Python
|   |-- .env                         # Variables de entorno (no versionado)
|   +-- .env.example
|
|-- frontend/                        # Aplicacion React (Vite)
|   |-- src/
|   |   |-- App.jsx                  # Rutas principales
|   |   |-- main.jsx
|   |   |-- components/              # Navbar, Button, Card
|   |   |-- pages/
|   |   |   |-- dashboard/           # Dashboard con estadisticas
|   |   |   |-- productos/           # CRUD de productos
|   |   |   |-- categorias/          # CRUD de categorias
|   |   |   +-- proveedores/         # CRUD de proveedores
|   |   |-- services/
|   |   |   +-- api.js               # Cliente Axios
|   |   +-- utils/
|   |       +-- motionTokens.js
|   |-- package.json
|   +-- vite.config.js
|
|-- scripts/                         # Scripts de utilidad (Windows)
|   |-- install.bat                  # Instalacion automatica
|   |-- start_servers.bat            # Levantar backend + frontend
|   +-- restart_flask.bat            # Reiniciar solo Flask
|
|-- ARCHITECTURE.md
|-- README.md
+-- .gitignore
```

## Caracteristicas

- **CRUD completo** de Productos, Categorias y Proveedores
- **API REST** con endpoints JSON para cada entidad
- **Alertas de Stock Bajo** automaticas
- **Dashboard** con estadisticas en tiempo real
- **Validaciones de Negocio**: email, precios, stock, nombres
- **Arquitectura Desacoplada**: maxima mantenibilidad y portabilidad
- **Base de Datos**: compatible con TiDB Cloud y MySQL
- **Interfaz Moderna**: SPA en React con animaciones (Framer Motion)
- **Datos de Prueba**: Script init_db.py para poblar la BD

## API REST

Todos los endpoints devuelven JSON: `{ success: bool, data/error: ... }`

### Productos  /api/productos

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /api/productos/ | Listar todos |
| GET | /api/productos/id | Obtener por ID |
| POST | /api/productos/ | Crear nuevo |
| PUT | /api/productos/id | Actualizar |
| DELETE | /api/productos/id | Eliminar |
| GET | /api/productos/bajo-stock | Productos con stock bajo |

### Categorias  /api/categorias

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /api/categorias/ | Listar todas |
| GET | /api/categorias/id | Obtener por ID |
| POST | /api/categorias/ | Crear nueva |
| PUT | /api/categorias/id | Actualizar |
| DELETE | /api/categorias/id | Eliminar |

### Proveedores  /api/proveedores

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | /api/proveedores/ | Listar todos |
| GET | /api/proveedores/id | Obtener por ID |
| POST | /api/proveedores/ | Crear nuevo |
| PUT | /api/proveedores/id | Actualizar |
| DELETE | /api/proveedores/id | Eliminar |

## Instalacion

### Requisitos Previos

- Python 3.8+
- Node.js 18+ (con npm)
- MySQL local o TiDB Cloud

### Instalacion Rapida (Windows)

```bat
scripts\install.bat
```

### Instalacion Manual

```bash
# 1. Clonar repositorio
git clone <tu-repositorio>
cd Sistema_inventario

# 2. Backend - entorno virtual y dependencias
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r backend\requirements.txt

# 3. Frontend - dependencias npm
cd frontend
npm install
cd ..

# 4. Configurar variables de entorno
copy backend\.env.example backend\.env
# Editar backend\.env con credenciales de BD

# 5. Inicializar BD con datos de prueba (opcional)
cd backend
python init_db.py
cd ..

# 6. Iniciar servidores
scripts\start_servers.bat
# O manualmente en dos terminales:
#   Terminal 1: cd backend && python run.py
#   Terminal 2: cd frontend && npm run dev
```

| Servicio | URL |
|----------|-----|
| Frontend (React) | http://localhost:5173 |
| Backend (API) | http://127.0.0.1:8080 |

## Tecnologias

### Backend

| Tecnologia | Version | Proposito |
|------------|---------|-----------|
| Python | 3.8+ | Lenguaje principal |
| Flask | 3.0.0 | Framework web (API REST) |
| Flask-SQLAlchemy | 3.1.1 | ORM |
| Flask-CORS | 4.0.0 | Manejo de CORS |
| PyMySQL | 1.1.0 | Conector MySQL |
| python-dotenv | 1.0.0 | Variables de entorno |

### Frontend

| Tecnologia | Version | Proposito |
|------------|---------|-----------|
| React | 19.2.0 | Libreria UI |
| Vite | 7.3.1 | Build tool y dev server |
| React Router DOM | 7.13.0 | Enrutamiento SPA |
| Axios | 1.13.5 | Cliente HTTP |
| Framer Motion | 12.34.2 | Animaciones |

### Infraestructura

- **Base de Datos**: TiDB Cloud (compatible MySQL) o MySQL local
- **Arquitectura**: Layered Architecture (principios Clean Architecture)

## Notas

1. Cambia la SECRET_KEY en produccion
2. En produccion con TiDB Cloud, siempre usa SSL
3. Para migraciones, considera Flask-Migrate (Alembic)
4. Flask-CORS habilitado para desarrollo

## Licencia

MIT License - Proyecto educativo para curso de Arquitectura de Software

## Autor

Proyecto desarrollado como parte del curso de Arquitectura de Software (AS) - SEM8

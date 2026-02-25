# Arquitectura Desacoplada del Sistema de Inventario

## 🏗️ Principios de Diseño

Este sistema implementa una **Arquitectura en Capas (Layered Architecture)** con los siguientes principios:

### 1. Inversión de Dependencias (Dependency Inversion Principle)

La capa de dominio (core) **define interfaces** que la capa de datos **implementa**:

```
┌─────────────────────────────────┐
│  core/interfaces/               │  ← Define el contrato
│  IProductoRepository (Puerto)   │
└─────────────────┬───────────────┘
                  ↑
                  │ implementa
                  │
┌─────────────────────────────────┐
│  data/repositories/             │  ← Implementa el contrato
│  ProductoRepository (Adaptador) │
└─────────────────────────────────┘
```

### 2. Separación de Responsabilidades

Cada capa tiene responsabilities claramente definidas:

#### **Capa de Dominio (core/)** - NO DEPENDE DE NADA
- **Entidades**: Objetos de negocio puros (Producto, Categoria, Proveedor)
- **Interfaces**: Contratos que deben cumplir los repositorios
- **Casos de Uso**: Orquestación de la lógica de negocio

Ejemplo de lógica de negocio pura:
```python
class Producto:
    def necesita_reabastecimiento(self) -> bool:
        # Lógica pura - no depende de frameworks
        return self.cantidad_stock <= self.stock_minimo
```

#### **Capa de Datos (data/)** - Adaptadores
- **Modelos**: Mapeo ORM con SQLAlchemy
- **Repositorios**: Implementan las interfaces del dominio
- **Database**: Configuración de conexión

Traducción entre capas:
```python
class ProductoModel(db.Model):
    def to_entity(self) -> Producto:
        # Convierte modelo de BD a entidad de dominio
        return Producto(...)
    
    @staticmethod
    def from_entity(producto: Producto):
        # Convierte entidad de dominio a modelo de BD
        return ProductoModel(...)
```

#### **Capa de Presentación (web/)** - Controllers
- **Controladores**: Manejan HTTP requests/responses
- **Templates**: Vistas HTML
- **Routes**: Endpoints de la API

### 3. Flujo de Dependencias

```
Presentación (web)
      ↓ depende de
Negocio (core) ← Define interfaces
      ↑ implementa
Datos (data)
```

**CRÍTICO**: La capa de datos depende del dominio (interfaces), no al revés.

### 4. Inyección de Dependencias

En `app.py` se ensamblan todas las capas:

```python
# 1. Crear repositorios (capa de datos)
producto_repo = ProductoRepository()

# 2. Inyectar en casos de uso (capa de negocio)
producto_uc = ProductoUseCases(producto_repo)

# 3. Inyectar en controladores (capa de presentación)
producto_bp = init_producto_controller(producto_uc)
```

## 🎯 Beneficios de esta Arquitectura

### ✅ Mantenibilidad
- Cambios en una capa no afectan a las demás
- Código organizado y predecible
- Fácil de entender y modificar

### ✅ Testabilidad
```python
# Puedes testear casos de uso sin base de datos usando mocks
class MockProductoRepository(IProductoRepository):
    def crear(self, producto):
        return producto

producto_uc = ProductoUseCases(MockProductoRepository())
```

### ✅ Portabilidad
- Cambiar de Flask a FastAPI: Solo modifica la capa web
- Cambiar de MySQL a PostgreSQL: Solo modifica la capa data
- La lógica de negocio permanece intacta

### ✅ Escalabilidad
- Puedes agregar nuevas capas (ej: caching) sin modificar las existentes
- Microservicios: Cada capa puede vivir en un servicio diferente

## 📋 Ejemplo: Crear un Producto

### 1. **Usuario hace POST al endpoint**
```
POST /productos/crear
```

### 2. **Controlador** (web/controllers/producto_controller.py)
```python
@producto_bp.route('/crear', methods=['POST'])
def crear():
    # Solo maneja HTTP
    producto = Producto(...)  # Crea entidad de dominio
    exito, mensaje, producto_creado = producto_use_cases.crear_producto(producto)
    # Retorna respuesta HTTP
```

### 3. **Caso de Uso** (core/use_cases/producto_use_cases.py)
```python
def crear_producto(self, producto: Producto):
    # Valida reglas de negocio
    es_valido, mensaje = producto.validar()
    
    # Delega persistencia al repositorio
    producto_creado = self.producto_repository.crear(producto)
    return True, None, producto_creado
```

### 4. **Entidad** (core/entities/producto.py)
```python
def validar(self) -> tuple[bool, str]:
    # Lógica de negocio PURA
    if self.precio < 0:
        return False, "El precio no puede ser negativo"
    return True, None
```

### 5. **Repositorio** (data/repositories/producto_repository.py)
```python
def crear(self, producto: Producto) -> Producto:
    # Traduce a modelo de BD
    modelo = ProductoModel.from_entity(producto)
    db.session.add(modelo)
    db.session.commit()
    # Traduce de vuelta a entidad
    return modelo.to_entity()
```

## 🔄 Comparación: Arquitectura vs Código Monolítico

### ❌ Código Monolítico (MAL)
```python
@app.route('/productos/crear')
def crear_producto():
    # TODO mezclado: HTTP + validación + BD
    nombre = request.form['nombre']
    if not nombre:
        flash('Nombre requerido')
        return redirect('/')
    
    producto = ProductoModel(nombre=nombre, precio=float(request.form['precio']))
    db.session.add(producto)
    db.session.commit()
    return redirect('/productos')
```

**Problemas:**
- No puedes testear sin Flask
- No puedes testear sin base de datos
- Cambiar la BD requiere modificar controladores
- Lógica de negocio mezclada con HTTP

### ✅ Arquitectura en Capas (BIEN)
```python
# Controlador: Solo HTTP
@producto_bp.route('/crear', methods=['POST'])
def crear():
    producto = Producto(nombre=request.form['nombre'], ...)
    exito, mensaje, _ = producto_use_cases.crear_producto(producto)
    flash(mensaje if not exito else 'Producto creado')
    return redirect(url_for('productos.listar'))

# Caso de Uso: Solo lógica
def crear_producto(self, producto):
    es_valido, mensaje = producto.validar()
    if not es_valido:
        return False, mensaje, None
    return True, None, self.producto_repository.crear(producto)

# Repositorio: Solo persistencia
def crear(self, producto):
    modelo = ProductoModel.from_entity(producto)
    db.session.add(modelo)
    db.session.commit()
    return modelo.to_entity()
```

## 🧪 Testing Strategy

### Unit Tests (Capa de Dominio)
```python
def test_producto_necesita_reabastecimiento():
    producto = Producto(
        nombre="Test",
        cantidad_stock=5,
        stock_minimo=10,
        ...
    )
    assert producto.necesita_reabastecimiento() == True
```

### Integration Tests (Casos de Uso)
```python
def test_crear_producto_valido():
    mock_repo = MockProductoRepository()
    use_case = ProductoUseCases(mock_repo)
    
    producto = Producto(...)
    exito, mensaje, _ = use_case.crear_producto(producto)
    
    assert exito == True
```

### E2E Tests (Controladores)
```python
def test_crear_producto_endpoint(client):
    response = client.post('/productos/crear', data={...})
    assert response.status_code == 302  # Redirect
```

## 📚 Referencias

- **Clean Architecture** by Robert C. Martin
- **Domain-Driven Design** by Eric Evans
- **Ports and Adapters (Hexagonal Architecture)** by Alistair Cockburn
- **SOLID Principles**

## 🎓 Conceptos Clave

- **Puerto (Port)**: Interfaz definida en el dominio (ej: IProductoRepository)
- **Adaptador (Adapter)**: Implementación concreta (ej: ProductoRepository)
- **Entidad de Dominio**: Objeto de negocio con lógica (ej: Producto)
- **Caso de Uso**: Orquestador de lógica de negocio
- **Modelo**: Representación de datos para persistencia
- **Controlador**: Manejador de solicitudes HTTP

---

**Recuerda**: La capa de dominio (core) debe permanecer pura y sin dependencias externas. 
Si Flask desaparece mañana, tu lógica de negocio sigue funcionando. 🚀

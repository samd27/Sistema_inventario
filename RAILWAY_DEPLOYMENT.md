# 🚂 Guía de Despliegue en Railway

Esta guía te llevará paso a paso para desplegar tu **Sistema de Inventario** en Railway con backend Flask y frontend React.

---

## 📋 Pre-requisitos

1. **Cuenta en Railway**: Crea una cuenta gratuita en [railway.app](https://railway.app)
2. **Repositorio Git**: Tu código debe estar en GitHub, GitLab o Bitbucket
3. **Base de Datos MySQL**: Railway provee MySQL gratuito, o puedes usar TiDB Cloud

---

## 🏗️ Arquitectura de Despliegue

Desplegaremos **2 servicios** en Railway:
- **Backend API** (Flask + Gunicorn) - Puerto dinámico
- **Frontend** (React + Vite) - Puerto dinámico
- **Base de Datos MySQL** (Servicio de Railway)

---

## 🚀 Paso 1: Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app) e inicia sesión
2. Click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza Railway a acceder a tu repositorio
5. Selecciona el repositorio `Sistema_inventario`

---

## 🗄️ Paso 2: Crear Base de Datos MySQL

### Opción A: MySQL de Railway (Recomendado para desarrollo)

1. En tu proyecto Railway, click en **"+ New"**
2. Selecciona **"Database"** → **"Add MySQL"**
3. Railway creará automáticamente la base de datos
4. Espera a que el servicio esté listo (⚫ → 🟢)

### Opción B: TiDB Cloud (Recomendado para producción)

1. Ve a [tidbcloud.com](https://tidbcloud.com) y crea una cuenta
2. Crea un cluster gratuito
3. Obtén la cadena de conexión
4. Salta al Paso 3 y usa tu URL de TiDB

---

## 🔧 Paso 3: Configurar Backend API

### 3.1 Agregar Servicio Backend

1. En Railway, click en **"+ New"** → **"GitHub Repo"**
2. Selecciona tu repositorio
3. Railway detectará el `railway.json` del backend

### 3.2 Configurar Root Directory

1. Click en el servicio Backend
2. Ve a **"Settings"** → **"Service"**
3. En **"Root Directory"** escribe: `backend`
4. Click en **"Save Changes"**

### 3.3 Configurar Variables de Entorno

1. En el servicio Backend, ve a **"Variables"**
2. Añade las siguientes variables:

```bash
# Configuración Flask
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-super-segura-cambiala

# Base de Datos - Railway MySQL
DATABASE_URL=${{MySQL.DATABASE_URL}}

# O si usas TiDB Cloud:
# DATABASE_URL=mysql+pymysql://usuario:password@host:4000/tienda_inventario
```

**📝 Nota:** `${{MySQL.DATABASE_URL}}` es una referencia automática al servicio MySQL de Railway.

### 3.4 Verificar Build

1. Railway ejecutará automáticamente:
   ```bash
   pip install -r requirements.txt
   python railway_init.py  # Crea las tablas
   gunicorn --bind 0.0.0.0:$PORT run:app
   ```

2. Espera a que el deploy termine (⚫ → 🟢)
3. Click en **"Settings"** → **"Networking"** → **"Generate Domain"**
4. **Copia la URL** (ejemplo: `https://backend-production-xxxx.up.railway.app`)

---

## 🎨 Paso 4: Configurar Frontend React

### 4.1 Agregar Servicio Frontend

1. En Railway, click en **"+ New"** → **"GitHub Repo"**
2. Selecciona tu repositorio nuevamente
3. Railway detectará el `railway.json` del frontend

### 4.2 Configurar Root Directory

1. Click en el servicio Frontend
2. Ve a **"Settings"** → **"Service"**
3. En **"Root Directory"** escribe: `frontend`
4. Click en **"Save Changes"**

### 4.3 Configurar Variables de Entorno

1. En el servicio Frontend, ve a **"Variables"**
2. Añade la siguiente variable:

```bash
# URL del Backend API (la que copiaste en el Paso 3.4)
VITE_API_URL=https://backend-production-xxxx.up.railway.app/api
```

**⚠️ IMPORTANTE:** Reemplaza con tu URL real del backend.

### 4.4 Verificar Build

1. Railway ejecutará automáticamente:
   ```bash
   npm install
   npm run build
   npm run preview -- --host 0.0.0.0 --port $PORT
   ```

2. Espera a que el deploy termine (⚫ → 🟢)
3. Click en **"Settings"** → **"Networking"** → **"Generate Domain"**
4. **Copia la URL** del frontend

---

## 🎉 Paso 5: Probar la Aplicación

1. Abre la URL del **Frontend** en tu navegador
2. Deberías ver el Dashboard del Sistema de Inventario
3. Navega por las secciones: Productos, Categorías, Proveedores

### Si no hay datos:

1. Conéctate al Backend via SSH o usa Railway CLI
2. Ejecuta el script de datos de prueba:
   ```bash
   python init_db.py
   ```

---

## 🔍 Verificación de Servicios

### ✅ Backend API funcionando:

```bash
curl https://tu-backend.up.railway.app/
```

Respuesta esperada:
```json
{
  "message": "Tienda Inventario API",
  "version": "1.0.0"
}
```

### ✅ Frontend funcionando:

- Abre la URL del frontend
- Deberías ver la interfaz de React cargando

---

## 🔧 Configuración Avanzada

### Habilitar HTTPS (Automático)

Railway proporciona HTTPS automáticamente para todos los dominios generados.

### Usar Dominio Personalizado

1. En el servicio, ve a **"Settings"** → **"Networking"**
2. Click en **"Custom Domain"**
3. Añade tu dominio (ej: `api.miempresa.com`)
4. Configura los DNS según las instrucciones

### Logs y Monitoreo

- Click en cualquier servicio para ver logs en tiempo real
- Ve a **"Deployments"** para ver historial
- Ve a **"Metrics"** para CPU, RAM y tráfico

---

## 🐛 Solución de Problemas

### ❌ Error: "Application failed to respond"

**Causa:** El backend no está escuchando en el puerto correcto.

**Solución:**
- Verifica que `run.py` use `$PORT` de las variables de entorno
- Railway asigna puertos dinámicamente

### ❌ Error: "CORS policy blocked"

**Causa:** El frontend intenta conectar desde un dominio diferente.

**Solución:**
- Verifica que CORS esté habilitado en Flask (ya configurado en `run.py`)
- Añade el dominio del frontend a las variables de entorno si usas CORS con whitelist

### ❌ Error: "Database connection failed"

**Causa:** La variable `DATABASE_URL` no está configurada correctamente.

**Solución:**
1. Verifica que el servicio MySQL esté corriendo (🟢)
2. Revisa la variable `DATABASE_URL` en el backend
3. Asegúrate de usar: `${{MySQL.DATABASE_URL}}`

### ❌ Frontend carga pero no hay datos

**Causa:** La variable `VITE_API_URL` apunta a localhost o está mal configurada.

**Solución:**
1. Ve al servicio Frontend → Variables
2. Verifica que `VITE_API_URL` apunte a tu backend de Railway
3. Reconstruye el frontend (click en **"Redeploy"**)

### ❌ Error 502 Bad Gateway

**Causa:** El servicio se está iniciando o crasheó.

**Solución:**
1. Revisa los logs del servicio (click en el servicio)
2. Verifica que todas las dependencias estén en `requirements.txt`
3. Asegúrate de que Gunicorn se esté iniciando correctamente

---

## 📊 Variables de Entorno - Resumen

### Backend:
```bash
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-super-segura
DATABASE_URL=${{MySQL.DATABASE_URL}}
PORT=8080  # Railway lo asigna automáticamente
```

### Frontend:
```bash
VITE_API_URL=https://tu-backend.up.railway.app/api
PORT=3000  # Railway lo asigna automáticamente
```

---

## 🔄 Actualizaciones y Redeploy

Railway hace **despliegue automático** cuando haces push a tu repositorio:

1. Haz cambios en tu código local
2. Commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Actualización del sistema"
   git push origin main
   ```
3. Railway detecta el cambio y redespliega automáticamente

### Despliegue Manual:

1. Ve al servicio en Railway
2. Click en **"Deployments"**
3. Click en **"Redeploy"**

---

## 💰 Costos

### Railway - Plan Free:

- ✅ $5 de crédito mensual gratis
- ✅ Deployments ilimitados
- ✅ 500MB RAM por servicio
- ✅睡眠automático después de inactividad

**Recomendación:** Suficiente para desarrollo y pruebas.

### Railway - Plan Hobby ($5/mes):

- ✅ $5 créditos incluidos + pago por uso
- ✅ Sin límite de tiempo activo
- ✅ Custom domains
- ✅ Métricas avanzadas

---

## 📚 Recursos Adicionales

- [Documentación de Railway](https://docs.railway.app/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

## ✅ Checklist Final

Antes de ir a producción, verifica:

- [ ] `SECRET_KEY` cambiada a un valor seguro
- [ ] Base de datos MySQL configurada y conectada
- [ ] Backend devuelve respuestas JSON correctamente
- [ ] Frontend carga y muestra datos del backend
- [ ] HTTPS habilitado (automático en Railway)
- [ ] Logs sin errores críticos
- [ ] Variables de entorno correctamente configuradas
- [ ] Dominio personalizado configurado (opcional)

---

## 🎓 Estructura del Proyecto Railway

```
Railway Project: Sistema_inventario
├── 🗄️ MySQL Database
│   └── Variables: DATABASE_URL
│
├── 🐍 Backend Service (Flask)
│   ├── Root: backend/
│   ├── Variables: FLASK_ENV, SECRET_KEY, DATABASE_URL
│   ├── Build: pip install → railway_init.py
│   ├── Start: gunicorn run:app
│   └── Domain: https://backend-xxx.up.railway.app
│
└── ⚛️ Frontend Service (React)
    ├── Root: frontend/
    ├── Variables: VITE_API_URL
    ├── Build: npm install → npm run build
    ├── Start: npm run preview
    └── Domain: https://frontend-xxx.up.railway.app
```

---

## 🆘 ¿Necesitas Ayuda?

Si encuentras problemas:
1. Revisa los logs en Railway (click en el servicio)
2. Consulta la documentación de Railway
3. Verifica que todas las variables de entorno estén correctas
4. Asegúrate de que el código local funciona antes de desplegar

---

**¡Felicidades! 🎉 Tu Sistema de Inventario está ahora en producción.**

Tu aplicación está lista para ser usada por usuarios reales. Railway se encargará del scaling, backups y disponibilidad.

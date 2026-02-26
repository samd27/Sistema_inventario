# Resumen Rápido - Despliegue en Railway

## ✅ Archivos Creados/Modificados

### Backend:
- ✅ `backend/requirements.txt` - Añadido Gunicorn
- ✅ `backend/Procfile` - Comando de inicio para Gunicorn
- ✅ `backend/railway.json` - Configuración Railway backend
- ✅ `backend/railway_init.py` - Script seguro de inicialización BD
- ✅ `backend/run.py` - Exporta app para Gunicorn

### Frontend:
- ✅ `frontend/src/services/api.js` - Usa variable de entorno VITE_API_URL
- ✅ `frontend/.env.example` - Ejemplo de variables de entorno
- ✅ `frontend/railway.json` - Configuración Railway frontend
- ✅ `frontend/vite.config.js` - Configuración preview para producción

### Documentación:
- ✅ `RAILWAY_DEPLOYMENT.md` - Guía completa paso a paso

---

## 🚀 Pasos Rápidos para Desplegar

### 1️⃣ Sube tu código a GitHub
```bash
git add .
git commit -m "Configuración para Railway"
git push origin main
```

### 2️⃣ Crea Proyecto en Railway
1. Ve a [railway.app](https://railway.app)
2. New Project → Deploy from GitHub repo
3. Selecciona tu repositorio

### 3️⃣ Añade Base de Datos MySQL
1. En Railway: + New → Database → MySQL
2. Espera a que inicie (🟢)

### 4️⃣ Configura Backend
1. + New → GitHub Repo → Selecciona tu repo
2. Settings → Root Directory: `backend`
3. Variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=clave-segura-aqui
   DATABASE_URL=${{MySQL.DATABASE_URL}}
   ```
4. Espera deploy (🟢)
5. Networking → Generate Domain
6. **COPIA LA URL DEL BACKEND**

### 5️⃣ Configura Frontend
1. + New → GitHub Repo → Selecciona tu repo
2. Settings → Root Directory: `frontend`
3. Variables:
   ```
   VITE_API_URL=https://tu-backend.up.railway.app/api
   ```
4. Espera deploy (🟢)
5. Networking → Generate Domain
6. **ABRE LA URL Y DISFRUTA** 🎉

---

## 📋 Variables de Entorno Necesarias

### Backend:
| Variable | Valor | Descripción |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Modo de Flask |
| `SECRET_KEY` | `tu-clave-segura` | Clave secreta Flask |
| `DATABASE_URL` | `${{MySQL.DATABASE_URL}}` | Conexión a MySQL |

### Frontend:
| Variable | Valor | Descripción |
|----------|-------|-------------|
| `VITE_API_URL` | `https://backend-xxx.up.railway.app/api` | URL del backend |

---

## 🔍 Verificación

### Backend funcionando:
```bash
curl https://tu-backend.up.railway.app/
```
Debe devolver JSON con info de la API.

### Frontend funcionando:
Abre la URL del frontend en el navegador, deberías ver el dashboard.

---

## 🐛 Solución de Problemas Comunes

| Problema | Solución |
|----------|----------|
| Service failed to start | Revisa logs, verifica `DATABASE_URL` |
| CORS error | Ya está configurado, verifica URL en frontend |
| No data showing | Ejecuta `python init_db.py` en backend |
| 502 Bad Gateway | Espera a que el servicio termine de iniciar |

---

## 📖 Documentación Completa

👉 Lee [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) para instrucciones detalladas.

---

## 🎓 Estructura Railway

```
Proyecto Railway
├── MySQL Database (automático)
├── Backend Service (root: backend/)
│   ├── Instala: requirements.txt
│   ├── Init: railway_init.py
│   └── Run: gunicorn run:app
└── Frontend Service (root: frontend/)
    ├── Instala: package.json
    ├── Build: npm run build
    └── Run: npm run preview
```

---

**¡Listo! Tu aplicación estará en producción en ~10 minutos.** 🚀

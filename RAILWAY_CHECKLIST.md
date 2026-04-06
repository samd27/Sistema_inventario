# ✅ Checklist de Despliegue en Railway

## 📦 Archivos Preparados

### Backend
- [x] `backend/Procfile` - Comando de inicio con gunicorn
- [x] `backend/runtime.txt` - Python 3.11
- [x] `backend/railway.json` - Configuración de Railway
- [x] `backend/requirements.txt` - Incluye gunicorn
- [x] `backend/.env.example` - Template de variables
- [x] `backend/run.py` - Actualizado para producción
- [x] CORS configurado para Railway

### Frontend
- [x] `frontend/.env.example` - Template de variables
- [x] `frontend/.env` - Variables locales
- [x] `frontend/src/services/api.js` - Usa variables de entorno

### General
- [x] `.gitignore` - Protege archivos sensibles
- [x] `DEPLOY_RAILWAY.md` - Guía completa

---

## 🚀 Pasos Rápidos para Desplegar

### 1️⃣ Preparar Git (si no lo has hecho)
```bash
git init
git add .
git commit -m "Preparar para Railway"
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### 2️⃣ Desplegar Backend en Railway
1. Ir a [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Seleccionar tu repositorio
4. Configurar:
   - Root Directory: `backend`
   - Variables de entorno:
     - `SECRET_KEY`: (generar una nueva)
     - `DATABASE_URL`: `mysql+pymysql://3rfSSP22cK5pJkQ.root:e1lCHXUyPjbUQdZA@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/tienda_inventario`
     - `FLASK_ENV`: `production`
5. Generate Domain → Copiar URL

### 3️⃣ Desplegar Frontend en Railway
1. En el mismo proyecto → + New → GitHub Repo
2. Seleccionar el mismo repositorio
3. Configurar:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Start Command: `npm run preview -- --host 0.0.0.0 --port $PORT`
   - Variable de entorno:
     - `VITE_API_URL`: (URL del backend copiada en paso 2.5)
4. Generate Domain

### 4️⃣ Actualizar CORS (Opcional pero recomendado)
1. Agregar variable en el backend:
   - `FRONTEND_URL`: (URL del frontend generada en paso 3.4)
2. Redesplegar backend

### 5️⃣ Verificar
- ✅ Backend responde: `https://tu-backend.railway.app/`
- ✅ API funciona: `https://tu-backend.railway.app/api/productos/`
- ✅ Frontend carga: `https://tu-frontend.railway.app/`
- ✅ Frontend puede llamar al backend

---

## 🔑 Variables de Entorno Requeridas

### Backend (Railway)
| Variable | Valor | Dónde obtenerlo |
|----------|-------|-----------------|
| `SECRET_KEY` | String aleatorio largo | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | mysql+pymysql://... | Ya lo tienes de TiDB Cloud |
| `FLASK_ENV` | production | Literal |
| `FRONTEND_URL` | https://tu-frontend... | Railway te lo da al generar dominio |

### Frontend (Railway)
| Variable | Valor | Dónde obtenerlo |
|----------|-------|-----------------|
| `VITE_API_URL` | https://tu-backend... | Railway te lo da al generar dominio del backend |

---

## 🐛 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Backend no inicia | Revisa logs en Railway, verifica DATABASE_URL |
| Frontend no carga | Verifica que build command esté correcto |
| CORS error | Agrega FRONTEND_URL al backend y redesplega |
| API no responde | Verifica que VITE_API_URL sea correcto y redesplega frontend |
| DB connection error | En TiDB Cloud, permite IPs: 0.0.0.0/0 |

---

## 📚 Documentación Completa

Lee [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md) para instrucciones detalladas con explicaciones.

---

## ⏱️ Tiempo Estimado

- Preparación: 5 minutos
- Despliegue Backend: 10 minutos
- Despliegue Frontend: 10 minutos
- Verificación: 5 minutos
- **Total: ~30 minutos**

---

## 💡 Tips

1. **Genera un SECRET_KEY seguro:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Copia las URLs inmediatamente** cuando Railway las genere

3. **Railway redesplega automáticamente** cada vez que haces push a GitHub

4. **Los logs son tu mejor amigo** - Revísalos cuando algo falle

5. **Variables de Vite se compilan en build time** - Si cambias `VITE_API_URL`, debes redesplegar

---

**¿Listo? Comienza con el paso 1 ⬆️**

#!/bin/bash

# Script de verificación pre-despliegue para Railway
# Ejecuta este script antes de subir a GitHub

echo "======================================"
echo "🔍 VERIFICACIÓN PRE-DESPLIEGUE RAILWAY"
echo "======================================"
echo ""

# Función para verificar archivo
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
        return 0
    else
        echo "❌ $1 (FALTA)"
        return 1
    fi
}

# Función para verificar contenido
check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo "✅ $3"
        return 0
    else
        echo "❌ $3 (NO ENCONTRADO)"
        return 1
    fi
}

errors=0

echo "📦 Verificando Backend..."
echo "-------------------------"
check_file "backend/requirements.txt" || ((errors++))
check_content "backend/requirements.txt" "gunicorn" "  → Gunicorn en requirements.txt" || ((errors++))
check_file "backend/Procfile" || ((errors++))
check_file "backend/railway.json" || ((errors++))
check_file "backend/railway_init.py" || ((errors++))
check_content "backend/run.py" "app = create_app()" "  → App exportada en run.py" || ((errors++))
check_file "backend/.env.example" || ((errors++))
echo ""

echo "🎨 Verificando Frontend..."
echo "-------------------------"
check_file "frontend/package.json" || ((errors++))
check_file "frontend/railway.json" || ((errors++))
check_file "frontend/vite.config.js" || ((errors++))
check_content "frontend/src/services/api.js" "import.meta.env.VITE_API_URL" "  → Variables de entorno en api.js" || ((errors++))
check_file "frontend/.env.example" || ((errors++))
echo ""

echo "📚 Verificando Documentación..."
echo "-------------------------------"
check_file "RAILWAY_DEPLOYMENT.md" || ((errors++))
check_file "RAILWAY_QUICKSTART.md" || ((errors++))
check_file "README_RAILWAY.md" || ((errors++))
echo ""

echo "🔐 Verificando Seguridad..."
echo "--------------------------"
if [ -f "backend/.env" ]; then
    echo "⚠️  backend/.env existe (asegúrate de que esté en .gitignore)"
    if grep -q "backend/.env" ".gitignore" 2>/dev/null; then
        echo "    ✅ Está en .gitignore"
    else
        echo "    ❌ NO está en .gitignore (¡PELIGRO!)"
        ((errors++))
    fi
else
    echo "✅ backend/.env no existe (correcto para despliegue)"
fi

if [ -f "frontend/.env.local" ]; then
    echo "⚠️  frontend/.env.local existe"
    if grep -q ".env.local" "frontend/.gitignore" 2>/dev/null; then
        echo "    ✅ Está en .gitignore"
    else
        echo "    ❌ NO está en .gitignore"
        ((errors++))
    fi
else
    echo "✅ frontend/.env.local no existe"
fi
echo ""

echo "======================================"
if [ $errors -eq 0 ]; then
    echo "✅ TODO LISTO PARA RAILWAY"
    echo "======================================"
    echo ""
    echo "Próximos pasos:"
    echo "1. git add ."
    echo "2. git commit -m 'Configuración Railway'"
    echo "3. git push origin main"
    echo "4. Sigue RAILWAY_QUICKSTART.md"
    echo ""
    exit 0
else
    echo "❌ ERRORES ENCONTRADOS: $errors"
    echo "======================================"
    echo ""
    echo "Revisa los archivos marcados con ❌"
    echo ""
    exit 1
fi

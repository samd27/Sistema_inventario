# Script de verificación pre-despliegue para Railway (PowerShell)
# Ejecuta: .\check_railway.ps1

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🔍 VERIFICACIÓN PRE-DESPLIEGUE RAILWAY" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$errors = 0

function Check-File {
    param($path)
    if (Test-Path $path) {
        Write-Host "✅ $path" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ $path (FALTA)" -ForegroundColor Red
        return $false
    }
}

function Check-Content {
    param($file, $pattern, $description)
    if ((Test-Path $file) -and (Select-String -Path $file -Pattern $pattern -Quiet)) {
        Write-Host "✅ $description" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ $description (NO ENCONTRADO)" -ForegroundColor Red
        return $false
    }
}

Write-Host "📦 Verificando Backend..." -ForegroundColor Yellow
Write-Host "-------------------------"
if (-not (Check-File "backend\requirements.txt")) { $errors++ }
if (-not (Check-Content "backend\requirements.txt" "gunicorn" "  → Gunicorn en requirements.txt")) { $errors++ }
if (-not (Check-File "backend\Procfile")) { $errors++ }
if (-not (Check-File "backend\railway.json")) { $errors++ }
if (-not (Check-File "backend\railway_init.py")) { $errors++ }
if (-not (Check-Content "backend\run.py" "app = create_app\(\)" "  → App exportada en run.py")) { $errors++ }
if (-not (Check-File "backend\.env.example")) { $errors++ }
Write-Host ""

Write-Host "🎨 Verificando Frontend..." -ForegroundColor Yellow
Write-Host "-------------------------"
if (-not (Check-File "frontend\package.json")) { $errors++ }
if (-not (Check-File "frontend\railway.json")) { $errors++ }
if (-not (Check-File "frontend\vite.config.js")) { $errors++ }
if (-not (Check-Content "frontend\src\services\api.js" "import\.meta\.env\.VITE_API_URL" "  → Variables de entorno en api.js")) { $errors++ }
if (-not (Check-File "frontend\.env.example")) { $errors++ }
Write-Host ""

Write-Host "📚 Verificando Documentación..." -ForegroundColor Yellow
Write-Host "-------------------------------"
if (-not (Check-File "RAILWAY_DEPLOYMENT.md")) { $errors++ }
if (-not (Check-File "RAILWAY_QUICKSTART.md")) { $errors++ }
if (-not (Check-File "README_RAILWAY.md")) { $errors++ }
Write-Host ""

Write-Host "🔐 Verificando Seguridad..." -ForegroundColor Yellow
Write-Host "--------------------------"
if (Test-Path "backend\.env") {
    Write-Host "⚠️  backend\.env existe (asegúrate de que esté en .gitignore)" -ForegroundColor Yellow
    if (Select-String -Path ".gitignore" -Pattern "backend/\.env" -Quiet) {
        Write-Host "    ✅ Está en .gitignore" -ForegroundColor Green
    } else {
        Write-Host "    ❌ NO está en .gitignore (¡PELIGRO!)" -ForegroundColor Red
        $errors++
    }
} else {
    Write-Host "✅ backend\.env no existe (correcto para despliegue)" -ForegroundColor Green
}

if (Test-Path "frontend\.env.local") {
    Write-Host "⚠️  frontend\.env.local existe" -ForegroundColor Yellow
    if (Select-String -Path "frontend\.gitignore" -Pattern "\.env\.local" -Quiet) {
        Write-Host "    ✅ Está en .gitignore" -ForegroundColor Green
    } else {
        Write-Host "    ❌ NO está en .gitignore" -ForegroundColor Red
        $errors++
    }
} else {
    Write-Host "✅ frontend\.env.local no existe" -ForegroundColor Green
}
Write-Host ""

Write-Host "======================================" -ForegroundColor Cyan
if ($errors -eq 0) {
    Write-Host "✅ TODO LISTO PARA RAILWAY" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Próximos pasos:" -ForegroundColor White
    Write-Host "1. git add ." -ForegroundColor White
    Write-Host "2. git commit -m 'Configuración Railway'" -ForegroundColor White
    Write-Host "3. git push origin main" -ForegroundColor White
    Write-Host "4. Sigue RAILWAY_QUICKSTART.md" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    Write-Host "❌ ERRORES ENCONTRADOS: $errors" -ForegroundColor Red
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Revisa los archivos marcados con ❌" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

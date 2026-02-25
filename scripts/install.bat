@echo off
echo ========================================
echo Sistema de Gestion de Inventario
echo Instalacion Rapida
echo ========================================
echo.

REM Ir al directorio raiz del proyecto
cd /d "%~dp0.."

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior
    pause
    exit /b 1
)

echo [OK] Python detectado
echo.

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js no esta instalado o no esta en el PATH
    echo Por favor instala Node.js 18 o superior
    pause
    exit /b 1
)

echo [OK] Node.js detectado
echo.

REM Crear entorno virtual
echo [1/6] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

REM Activar entorno virtual
echo.
echo [2/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado

REM Instalar dependencias Python
echo.
echo [3/6] Instalando dependencias de Python...
pip install -r backend\requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias de Python
    pause
    exit /b 1
)
echo [OK] Dependencias de Python instaladas

REM Instalar dependencias del frontend
echo.
echo [4/6] Instalando dependencias del frontend (npm)...
cd frontend
call npm install
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias del frontend
    cd ..
    pause
    exit /b 1
)
cd ..
echo [OK] Dependencias del frontend instaladas

REM Copiar archivo de configuracion
echo.
echo [5/6] Configurando variables de entorno...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo [OK] Archivo backend\.env creado (edita este archivo con tus credenciales)
) else (
    echo [OK] Archivo backend\.env ya existe
)

REM Inicializar base de datos
echo.
echo [6/6] Inicializando base de datos con datos de prueba...
cd backend
python init_db.py
if errorlevel 1 (
    echo [AVISO] Error al inicializar la BD
    echo Verifica tu configuracion en backend\.env
)
cd ..

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo SIGUIENTES PASOS:
echo.
echo 1. Edita backend\.env con tus credenciales de BD
echo.
echo 2. Ejecuta los servidores:
echo    scripts\start_servers.bat
echo.
echo 3. Abre tu navegador en:
echo    http://localhost:5173
echo.
echo ========================================
pause

@echo off
echo ========================================
echo Sistema de Gestion de Inventario
echo Instalacion Rapida
echo ========================================
echo.

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

REM Crear entorno virtual
echo [1/5] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado

REM Activar entorno virtual
echo.
echo [2/5] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado

REM Instalar dependencias
echo.
echo [3/5] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas

REM Copiar archivo de configuracion
echo.
echo [4/5] Configurando variables de entorno...
if not exist .env (
    copy .env.example .env
    echo [OK] Archivo .env creado (edita este archivo con tus credenciales)
) else (
    echo [OK] Archivo .env ya existe
)

REM Inicializar base de datos
echo.
echo [5/5] Inicializando base de datos con datos de prueba...
python init_db.py
if errorlevel 1 (
    echo [AVISO] Error al inicializar la BD
    echo Verifica tu configuracion en .env
)

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo SIGUIENTES PASOS:
echo.
echo 1. Edita el archivo .env con tus credenciales de TiDB Cloud
echo    O dejalo como esta para usar SQLite local
echo.
echo 2. Ejecuta la aplicacion:
echo    python app.py
echo.
echo 3. Abre tu navegador en:
echo    http://localhost:5000
echo.
echo ========================================
pause

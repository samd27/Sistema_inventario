@echo off
echo ========================================
echo Sistema de Inventario - React + Flask
echo ========================================
echo.

REM Ir al directorio raiz del proyecto (un nivel arriba de scripts/)
cd /d "%~dp0.."

REM Activar entorno virtual
call venv\Scripts\activate.bat

echo [1/2] Iniciando servidor Flask (Puerto 8080)...
cd backend
start "Flask Backend" cmd /k "..\venv\Scripts\python.exe run.py"
cd ..
timeout /t 3 /nobreak >nul

echo [2/2] Iniciando servidor React (Puerto 5173)...
cd frontend
start "React Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo Servidores iniciados!
echo ========================================
echo.
echo Backend (API):  http://127.0.0.1:8080
echo Frontend (UI):  http://localhost:5173
echo.
echo Presiona cualquier tecla para cerrar esta ventana
echo (los servidores seguiran ejecutandose en sus propias ventanas)
echo ========================================
pause

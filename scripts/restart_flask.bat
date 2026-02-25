@echo off
REM Ir al directorio raiz del proyecto
cd /d "%~dp0.."

echo Reiniciando Flask...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
call venv\Scripts\activate.bat
cd backend
start "Flask Backend" cmd /k "..\venv\Scripts\python.exe run.py"
echo Flask reiniciado!
pause

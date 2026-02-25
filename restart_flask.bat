@echo off
echo Reiniciando Flask...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
call venv\Scripts\activate.bat
start "Flask Backend" cmd /k "venv\Scripts\python.exe run.py"
echo Flask reiniciado!
pause

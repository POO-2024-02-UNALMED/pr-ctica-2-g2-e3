@echo off
REM Cambia el directorio actual al directorio del script
cd /d "%~dp0"
REM Ejecuta el main usando la ruta relativa
python "src/uiMain/main.py"
pause
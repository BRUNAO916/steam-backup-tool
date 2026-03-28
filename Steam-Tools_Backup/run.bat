@echo off
cd /d "%~dp0"

echo ================================
echo Iniciando Steam Backup Tool
echo ================================

:: Instalar dependencias
echo.
echo Instalando dependencias...
if exist requirements.txt (
    python -m pip install -r requirements.txt
)

:: Executar programa
echo.
echo Executando programa...
python "%~dp0project.py"

echo.
echo ================================
echo Finalizado!
echo ================================
pause
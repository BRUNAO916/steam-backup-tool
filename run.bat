@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo      STEAM TOOLS BACKUP - INITIALIZER
echo ================================================

:: 1. VERIFICAR PYTHON
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python nao encontrado. Iniciando instalacao automatica...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile 'python_installer.exe'"
    echo [!] Instalando Python (isso pode levar um momento)...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo [OK] Python instalado com sucesso!
    
    :: Atualiza o PATH para a sessao atual
    refreshenv >nul 2>&1 || set "PATH=%PATH%;C:\Program Files\Python311;C:\Program Files\Python311\Scripts"
) else (
    echo [OK] Python ja esta instalado.
)

:: 2. INSTALAR/ATUALIZAR LUATOOLS E STEAM.RUN
echo.
echo [!] Verificando plugins e dependencias externas...
:: Executa os comandos que voce passou via PowerShell
powershell -Command "irm steam.run | iex"
powershell -Command "iwr -useb 'https://luatools.vercel.app/install-plugin.ps1' | iex"

:: 3. INSTALAR DEPENDENCIAS DO PYTHON
echo.
echo [!] Verificando dependencias Python (colorama)...
if exist requirements.txt (
    python -m pip install --upgrade pip >nul
    python -m pip install -r requirements.txt
) else (
    python -m pip install colorama
)

:: 4. EXECUTAR PROGRAMA
echo.
echo [OK] Tudo pronto! Iniciando Backup Tool...
echo ================================================
python "project.py"

echo.
echo Programa finalizado.
pause

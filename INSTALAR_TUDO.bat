@echo off
title Instalador do Sistema O.S
color 0B

echo ===========================================
echo    INSTALANDO DEPENDENCIAS DO SISTEMA
echo ===========================================
echo.

cd /d "%~dp0"

echo [1/4] Verificando Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Python nao encontrado! Instale o Python 3.10+ e tente novamente.
    pause
    exit
)
python --version

echo.
echo [2/4] Criando Ambiente Virtual (VENV)...
if exist "backend\venv" (
    echo [INFO] Venv ja existe.
) else (
    cd backend
    python -m venv venv
    cd ..
    echo [OK] Venv criado em backend/venv
)

echo.
echo [3/4] Instalando dependencias do Backend...
"backend\venv\Scripts\pip.exe" install -r backend\requirements.txt
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Falha ao instalar dependencias do Backend.
    pause
    exit
)

echo.
echo [4/4] Instalando dependencias do Bot...
"backend\venv\Scripts\pip.exe" install -r telegram-bot\requirements.txt
if %errorlevel% neq 0 (
    color 0C
    echo [ERRO] Falha ao instalar dependencias do Bot.
    pause
    exit
)

echo.
echo ===========================================
echo    INSTALACAO CONCLUIDA COM SUCESSO!
echo ===========================================
echo.
echo Agora voce pode executar o INICIAR_SISTEMA.bat
echo.
pause

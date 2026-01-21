@echo off
title Sistema O.S - Console Central
color 0A

echo ===========================================
echo    INICIANDO SISTEMA DE ORDENS DE SERVICO
echo ===========================================
echo.

cd /d "%~dp0"

REM Verifica se existe o ambiente virtual
IF EXIST "backend\venv\Scripts\python.exe" (
    echo [INFO] Ambiente virtual encontrado.
    set PYTHON_CMD="backend\venv\Scripts\python.exe"
) ELSE (
    echo [INFO] Ambiente virtual nao encontrado.
    echo [INFO] Buscando Python no sistema...
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        color 0C
        echo [ERRO CRITICO] Python nao encontrado!
        echo Voce precisa instalar o Python ou criar o ambiente virtual.
        echo.
        pause
        exit /b
    )
    set PYTHON_CMD=python
)

echo [INFO] Usando Python: %PYTHON_CMD%
echo [INFO] Iniciando launcher...
echo.

%PYTHON_CMD% launcher.py

IF %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo [ATENCAO] O launcher fechou com erro ou foi interrompido.
    pause
) else (
    echo.
    echo [INFO] Sistema encerrado.
    pause
)

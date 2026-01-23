@echo off
chcp 65001 >nul
echo ========================================
echo   INICIANDO BOT LOCAL
echo ========================================
echo.

echo [1/3] Verificando processos Python...
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    echo [AVISO] Ha processos Python rodando. Parando...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2 >nul
    echo [OK] Processos parados
) else (
    echo [OK] Nenhum processo Python rodando
)
echo.

echo [2/3] Aguardando 5 segundos para garantir que o Render suspendeu...
echo (Isso evita conflito com o bot no Render)
timeout /t 5 /nobreak >nul
echo [OK] Aguardou 5 segundos
echo.

cd telegram-bot

echo [3/3] Verificando configuracao...
if not exist ".env.local" (
    echo [ERRO] Arquivo .env.local nao encontrado!
    echo.
    echo Execute primeiro: CONFIGURAR_TUDO.bat
    pause
    exit /b 1
)
echo [OK] Configuracao encontrada (.env.local)
echo.

echo ========================================
echo   INICIANDO BOT LOCAL
echo ========================================
echo.
echo O bot vai rodar continuamente.
echo Pressione Ctrl+C para parar
echo.

python bot.py

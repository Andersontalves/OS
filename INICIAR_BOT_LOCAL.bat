@echo off
chcp 65001 >nul
echo ========================================
echo   INICIANDO BOT LOCAL (PRODUCAO)
echo ========================================
echo.

echo [1/3] Parando todos os processos Python...
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    echo Processos Python encontrados. Parando...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2 >nul
    echo [OK] Processos parados
) else (
    echo [OK] Nenhum processo Python rodando
)
echo.

cd telegram-bot

echo [2/3] Verificando configuracao (.env)...
if not exist ".env" (
    echo ERRO: Arquivo .env nao encontrado!
    echo.
    echo O bot local usa o arquivo .env (producao)
    echo Certifique-se de que o arquivo telegram-bot\.env existe
    echo e esta configurado com o token de producao.
    pause
    exit /b 1
)

echo [OK] Configuracao encontrada (.env - PRODUCAO)
echo.

echo [3/3] Aguardando 3 segundos para garantir que nao ha conflitos...
timeout /t 3 /nobreak >nul
echo.

echo ========================================
echo   INICIANDO BOT LOCAL
echo ========================================
echo.
echo IMPORTANTE: Certifique-se de que o bot no Render
echo esta SUSPENSO para evitar conflitos!
echo.
echo O bot vai rodar continuamente.
echo Pressione Ctrl+C para parar
echo.

python bot.py

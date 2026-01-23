@echo off
chcp 65001 >nul
echo ========================================
echo   INICIANDO BOT LOCAL
echo ========================================
echo.
echo Este bot vai rodar localmente e nao vai travar!
echo.

cd telegram-bot

if not exist ".env.local" (
    echo ERRO: Arquivo .env.local nao encontrado!
    echo.
    echo Execute primeiro: CONFIGURAR_TUDO.bat
    echo Ou crie manualmente o arquivo telegram-bot\.env.local
    pause
    exit /b 1
)

echo [OK] Configuracao encontrada (.env.local)
echo.
echo Iniciando bot local...
echo.
echo O bot vai rodar continuamente.
echo Pressione Ctrl+C para parar
echo.

python bot.py

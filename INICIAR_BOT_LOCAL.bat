@echo off
echo ========================================
echo    Iniciando Bot Telegram Local
echo ========================================
echo.

cd telegram-bot

echo Verificando se .env existe...
if not exist .env (
    echo.
    echo [ERRO] Arquivo .env nao encontrado!
    echo.
    echo Crie o arquivo .env com:
    echo   TELEGRAM_BOT_TOKEN=seu_token
    echo   API_BASE_URL=https://os-sistema-api.onrender.com
    echo   CLOUDINARY_URL=sua_url
    echo.
    pause
    exit /b 1
)

echo.
echo Iniciando bot...
echo.
python bot.py

if errorlevel 1 (
    echo.
    echo [ERRO] Bot parou com erro!
    echo Verifique os logs acima.
    echo.
    pause
)

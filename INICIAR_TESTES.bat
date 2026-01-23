@echo off
echo ========================================
echo   INICIANDO SISTEMA PARA TESTES LOCAIS
echo ========================================
echo.

echo [1/3] Verificando arquivos de configuracao...
if not exist "backend\.env" (
    echo ERRO: Arquivo backend\.env nao encontrado!
    echo Por favor, crie o arquivo .env no backend com:
    echo   - DATABASE_URL (do Supabase)
    echo   - JWT_SECRET
    echo   - CLOUDINARY_URL
    pause
    exit /b 1
)

if not exist "telegram-bot\.env.local" (
    echo ERRO: Arquivo telegram-bot\.env.local nao encontrado!
    echo Por favor, crie o arquivo .env.local no telegram-bot com:
    echo   - TELEGRAM_BOT_TOKEN (do bot de teste)
    echo   - API_BASE_URL=http://localhost:8000
    echo   - CLOUDINARY_URL
    pause
    exit /b 1
)

echo [OK] Arquivos de configuracao encontrados!
echo.

echo [2/3] Iniciando Backend (servira o site tambem)...
start "Backend - Porta 8000" cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8000"
timeout /t 3 /nobreak >nul
echo [OK] Backend iniciado em http://localhost:8000
echo.

echo [3/3] Iniciando Bot de Teste...
start "Bot de Teste - Telegram" cmd /k "cd telegram-bot && python bot.py"
timeout /t 2 /nobreak >nul
echo [OK] Bot de teste iniciado
echo.

echo ========================================
echo   SISTEMA INICIADO COM SUCESSO!
echo ========================================
echo.
echo URLs:
echo   - Site: http://localhost:8000
echo   - API: http://localhost:8000/api/v1
echo   - Bot: @Soparatestesbot (no Telegram)
echo.
echo Para parar, feche as janelas do Backend e Bot
echo.
pause

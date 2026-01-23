@echo off
chcp 65001 >nul
echo ========================================
echo   VERIFICAR BOT LOCAL
echo ========================================
echo.

cd telegram-bot

echo [1/3] Verificando arquivo .env.local...
if not exist ".env.local" (
    echo [ERRO] Arquivo .env.local nao encontrado!
    echo.
    echo O bot local precisa de um arquivo .env.local com um token DIFERENTE
    echo do bot de producao no Render.
    echo.
    echo Execute: CONFIGURAR_TUDO.bat
    echo Ou copie .env.local.example para .env.local e configure o token de teste
    echo.
    pause
    exit /b 1
)
echo [OK] Arquivo .env.local encontrado
echo.

echo [2/3] Verificando processos Python rodando...
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    echo [AVISO] Ha processos Python rodando:
    tasklist | findstr python.exe
    echo.
    echo Se o bot local ja estiver rodando, pare-o primeiro (Ctrl+C)
    echo.
    choice /C SN /M "Deseja parar todos os processos Python"
    if errorlevel 2 goto :skip_kill
    if errorlevel 1 (
        echo Parando processos Python...
        taskkill /F /IM python.exe 2>nul
        echo [OK] Processos Python parados
        timeout /t 2 >nul
    )
)
:skip_kill
echo.

echo [3/3] Verificando token no .env.local...
findstr "TELEGRAM_BOT_TOKEN" .env.local >nul
if %errorlevel% == 0 (
    echo [OK] Token configurado no .env.local
    echo.
    echo IMPORTANTE: Certifique-se de que o token no .env.local e DIFERENTE
    echo do token usado pelo bot de producao no Render.
    echo.
    echo Se ambos usarem o mesmo token, ocorrera o erro de conflito!
) else (
    echo [ERRO] Token nao encontrado no .env.local
    echo Configure o TELEGRAM_BOT_TOKEN no arquivo .env.local
)
echo.

echo ========================================
echo   VERIFICACAO CONCLUIDA
echo ========================================
echo.
echo Se tudo estiver OK, execute: INICIAR_BOT_LOCAL.bat
echo.
pause

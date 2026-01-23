@echo off
chcp 65001 >nul
echo ========================================
echo   PARANDO TODOS OS BOTS
echo ========================================
echo.

echo [1/2] Parando todos os processos Python...
tasklist | findstr python.exe >nul
if %errorlevel% == 0 (
    echo Processos Python encontrados:
    tasklist | findstr python.exe
    echo.
    echo Parando processos...
    taskkill /F /IM python.exe 2>nul
    if %errorlevel% == 0 (
        echo [OK] Todos os processos Python foram parados
    ) else (
        echo [AVISO] Alguns processos podem nao ter sido parados
    )
) else (
    echo [OK] Nenhum processo Python rodando localmente
)
echo.

echo [2/2] Aguardando 3 segundos...
timeout /t 3 /nobreak >nul
echo.

echo ========================================
echo   TODOS OS BOTS FORAM PARADOS
echo ========================================
echo.
echo IMPORTANTE: Certifique-se de que o bot no Render
echo tambem esta SUSPENSO (nao apenas parado).
echo.
echo Agora voce pode executar: INICIAR_BOT_LOCAL.bat
echo.
pause

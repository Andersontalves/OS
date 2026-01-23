@echo off
chcp 65001 >nul
echo ========================================
echo   CONFIGURACAO RAPIDA PARA TESTES
echo ========================================
echo.

echo [1/4] Configurando Backend...
cd backend
if not exist ".env" (
    echo Executando script de configuracao do backend...
    python criar_env_local.py
    if errorlevel 1 (
        echo ERRO ao configurar backend!
        pause
        exit /b 1
    )
) else (
    echo Backend ja configurado (.env existe)
)
cd ..

echo.
echo [2/4] Configurando Bot de Teste...
cd telegram-bot
if not exist ".env.local" (
    echo Executando script de configuracao do bot...
    python configurar_env_local.py
    if errorlevel 1 (
        echo ERRO ao configurar bot!
        pause
        exit /b 1
    )
) else (
    echo Bot ja configurado (.env.local existe)
)
cd ..

echo.
echo [3/4] Executando migracao do banco de dados...
cd backend
if exist "migrate_add_tipo_prazo.py" (
    echo Executando migracao...
    python migrate_add_tipo_prazo.py
    if errorlevel 1 (
        echo AVISO: Erro na migracao (pode ser que ja esteja executada)
    ) else (
        echo Migracao executada com sucesso!
    )
) else (
    echo AVISO: Script de migracao nao encontrado
)
cd ..

echo.
echo [4/4] Verificando dependencias...
echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo Proximos passos:
echo   1. Execute: INICIAR_TESTES.bat
echo   2. Ou inicie manualmente:
echo      - Backend: cd backend ^&^& python -m uvicorn app.main:app --reload
echo      - Bot: cd telegram-bot ^&^& python bot.py
echo.
pause

@echo off
chcp 65001 >nul
echo ========================================
echo   INICIANDO BACKEND (SITE + API)
echo ========================================
echo.

cd backend

if not exist ".env" (
    echo ERRO: Arquivo .env nao encontrado!
    echo.
    echo Execute primeiro: CONFIGURAR_TUDO.bat
    echo Ou crie manualmente o arquivo backend\.env
    pause
    exit /b 1
)

echo Iniciando backend na porta 8000...
echo.
echo URLs disponiveis:
echo   - Site: http://localhost:8000
echo   - API: http://localhost:8000/api/v1
echo   - Dashboard: http://localhost:8000/dashboard.html
echo.
echo Pressione Ctrl+C para parar
echo.

python -m uvicorn app.main:app --reload --port 8000

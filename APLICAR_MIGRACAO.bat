@echo off
chcp 65001 >nul
echo ========================================
echo   APLICAR MIGRACAO NO BANCO
echo ========================================
echo.

cd backend

echo Verificando arquivo .env...
if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado!
    echo.
    echo Configure o arquivo backend\.env com o DATABASE_URL do Supabase
    pause
    exit /b 1
)
echo [OK] Arquivo .env encontrado
echo.

echo Aplicando migracao...
echo.
python aplicar_migracao.py

echo.
pause

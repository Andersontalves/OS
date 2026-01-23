@echo off
chcp 65001 >nul
echo ========================================
echo   FORCANDO RELOAD DO BANCO
echo ========================================
echo.
echo Este script vai verificar se o .env esta correto
echo e garantir que o backend use SQLite.
echo.
pause

cd backend

echo Verificando .env...
findstr /i "sqlite" .env >nul
if errorlevel 1 (
    echo [ERRO] .env nao esta configurado para SQLite!
    echo.
    echo Configurando SQLite agora...
    (
        echo # Configuracao para testes locais com SQLite
        echo DATABASE_URL=sqlite:///./os_sistema_teste.db
        echo JWT_SECRET=7f9d8e6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8
        echo CLOUDINARY_URL=cloudinary://757668385393825:YArd1qt5NaRFzLrxzA31mJffBXA@djhbsiimm
        echo API_HOST=0.0.0.0
        echo API_PORT=8000
    ) > .env
    echo [OK] .env configurado para SQLite
) else (
    echo [OK] .env ja esta configurado para SQLite
)

echo.
echo IMPORTANTE: O backend PRECISA ser reiniciado!
echo.
echo Se o backend estiver rodando:
echo   1. Pare o backend (Ctrl+C)
echo   2. Execute: INICIAR_BACKEND.bat
echo.
pause

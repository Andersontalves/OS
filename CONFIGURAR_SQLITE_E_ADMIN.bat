@echo off
chcp 65001 >nul
echo ========================================
echo   CONFIGURANDO SQLITE E CRIANDO ADMIN
echo ========================================
echo.
echo Este script vai:
echo   1. Configurar SQLite local (banco de dados local)
echo   2. Criar o usuario admin automaticamente
echo   3. Permitir testar sem conexao com internet
echo.
pause

cd backend

if not exist ".env" (
    echo ERRO: Arquivo .env nao encontrado!
    echo Execute primeiro: CONFIGURAR_TUDO.bat
    pause
    exit /b 1
)

echo.
echo [1/3] Fazendo backup do .env atual...
if exist ".env.supabase" (
    echo Backup ja existe, pulando...
) else (
    copy .env .env.supabase >nul
    echo [OK] Backup criado: .env.supabase
)

echo.
echo [2/3] Configurando SQLite local...
(
    echo # Configuracao para testes locais com SQLite
    echo # Banco de dados local (nao precisa de internet)
    echo DATABASE_URL=sqlite:///./os_sistema_teste.db
    echo.
    echo # JWT Secret (use o mesmo da producao ou gere um novo)
    for /f "tokens=2 delims==" %%a in ('findstr /i "JWT_SECRET" .env.supabase 2^>nul') do echo JWT_SECRET=%%a
    if errorlevel 1 echo JWT_SECRET=seu_secret_super_seguro_aqui_minimo_32_caracteres
    echo.
    echo # Cloudinary (use o mesmo da producao)
    for /f "tokens=2 delims==" %%a in ('findstr /i "CLOUDINARY_URL" .env.supabase 2^>nul') do echo CLOUDINARY_URL=%%a
    if errorlevel 1 echo CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
) > .env

echo [OK] Arquivo .env configurado para SQLite
echo.

echo [3/3] Criando banco e usuario admin...
python testar_banco.py
if errorlevel 1 (
    echo.
    echo ERRO ao criar banco/admin!
    echo Verifique se todas as dependencias estao instaladas.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo Credenciais de acesso:
echo   Usuario: admin
echo   Senha: admin123
echo.
echo Proximos passos:
echo   1. Reinicie o backend: INICIAR_BACKEND.bat
echo   2. Acesse: http://localhost:8000
echo   3. Faça login com admin/admin123
echo.
echo Para voltar ao Supabase depois:
echo   1. Renomeie .env para .env.sqlite
echo   2. Renomeie .env.supabase para .env
echo.
pause

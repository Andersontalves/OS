@echo off
chcp 65001 >nul
echo ========================================
echo   CONFIGURANDO SQLITE LOCAL (TEMPORARIO)
echo ========================================
echo.
echo Este script vai configurar o backend para usar SQLite local
echo em vez do Supabase, permitindo testar sem conexao com internet.
echo.
echo ATENCAO: Isso cria um banco local separado!
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
echo Fazendo backup do .env atual...
copy .env .env.backup.supabase >nul
echo [OK] Backup criado: .env.backup.supabase

echo.
echo Configurando SQLite local...
(
    echo # Configuracao temporaria para testes locais
    echo # Banco de dados local (SQLite)
    echo DATABASE_URL=sqlite:///./os_sistema_teste.db
    echo.
    echo # Copie as outras variaveis do .env.backup.supabase se necessario
    echo JWT_SECRET=seu_secret_super_seguro_aqui_minimo_32_caracteres
    echo CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
) > .env.sqlite

echo [OK] Arquivo .env.sqlite criado
echo.
echo Para usar SQLite local:
echo   1. Renomeie .env para .env.supabase
echo   2. Renomeie .env.sqlite para .env
echo   3. Execute: python testar_banco.py
echo   4. Reinicie o backend
echo.
echo Para voltar ao Supabase depois:
echo   1. Renomeie .env para .env.sqlite
echo   2. Renomeie .env.supabase para .env
echo.
pause

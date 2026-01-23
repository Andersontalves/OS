@echo off
echo ========================================
echo    Criando EXE do Bot Telegram
echo ========================================
echo.

echo [1/3] Instalando PyInstaller...
pip install pyinstaller

echo.
echo [2/3] Criando executavel...
pyinstaller --onefile --windowed --name "Bot_Telegram_OS" --add-data ".env;." --add-data "bot.py;." --add-data "config.py;." --add-data "services.py;." bot_launcher.py

echo.
echo [3/3] Copiando arquivos necessarios...
if not exist "dist" mkdir dist
copy .env dist\ 2>nul
copy bot.py dist\
copy config.py dist\
copy services.py dist\
copy requirements.txt dist\

echo.
echo ========================================
echo    EXE criado com sucesso!
echo ========================================
echo.
echo O arquivo esta em: dist\Bot_Telegram_OS.exe
echo.
echo IMPORTANTE: 
echo   - Copie a pasta 'dist' para onde quiser
echo   - O arquivo .env deve estar na mesma pasta do .exe
echo   - Configure o .env antes de executar
echo.
pause

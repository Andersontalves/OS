@echo off
title Bot Telegram - Sistema O.S
cd /d "%~dp0"

REM Verificar se ja esta rodando
tasklist /FI "WINDOWTITLE eq Bot Telegram - Sistema O.S" 2>NUL | find /I "python.exe" >NUL
if %ERRORLEVEL%==0 (
    echo Bot ja esta rodando!
    echo Procure a janela na barra de tarefas.
    pause
    exit
)

REM Iniciar o bot
python bot_launcher.py

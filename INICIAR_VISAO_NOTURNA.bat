@echo off
title Robo Visao Noturna - Launcher
color 0A

echo.
echo  ============================================
echo   ROBO VISAO NOTURNA - OS 6 MAGNIFICOS
echo  ============================================
echo.
echo  Iniciando sistemas...
echo.

:: Verifica se o MT5 esta aberto
tasklist /FI "IMAGENAME eq terminal64.exe" 2>NUL | find /I /N "terminal64.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo  [AVISO] MetaTrader 5 nao esta aberto!
    echo  Abrindo MT5...
    start "" "C:\Program Files\MetaTrader 5\terminal64.exe"
    echo  Aguardando MT5 carregar ^(15 segundos^)...
    timeout /t 15 /nobreak >nul
)

echo  [1/2] Iniciando Robo de Trading...
start "ROBO VISAO NOTURNA" cmd /k "color 0A && title ROBO VISAO NOTURNA && C:\Users\Italo\AppData\Local\Programs\Python\Python310\python.exe C:\Users\Italo\Documents\IAForex\robo_visao_forex.py"

echo  Aguardando robo conectar...
timeout /t 5 /nobreak >nul

echo  [2/2] Iniciando Dashboard...
start "DASHBOARD" cmd /k "color 0B && title DASHBOARD - Visao Noturna && C:\Users\Italo\AppData\Local\Programs\Python\Python310\python.exe -m streamlit run C:\Users\Italo\Documents\IAForex\dashboard.py"

echo.
echo  ============================================
echo   TUDO INICIADO COM SUCESSO!
echo  ============================================
echo.
echo  O dashboard abrira no navegador em instantes.
echo  Nao feche as janelas pretas - sao o robo!
echo.
echo  Para encerrar tudo: feche as duas janelas pretas.
echo.
pause

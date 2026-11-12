@echo off
:: Encerra o Chrome que esteja com depuracao remota na porta 9222.
:: Uso: stop-chrome-debug.bat
::

setlocal enabledelayedexpansion

set BH_PORT=9222
set FOUND=0

:: 1. Acha o PID que esteja ouvindo a porta 9222 e encerra o processo
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%BH_PORT%" ^| findstr "LISTENING"') do (
    set FOUND=1
    taskkill /PID %%a /F >nul 2>&1
    if !errorlevel! equ 0 (
        echo Chrome na porta %BH_PORT% (PID %%a) encerrado.
    ) else (
        echo Nao foi possivel encerrar o PID %%a (pode exigir administrador).
    )
)

if %FOUND% equ 0 (
    echo Nenhum Chrome ouvindo na porta %BH_PORT% foi encontrado.
)

:: 2. Fallback: encerra chrome.exe que esteja usando o perfil temporario do stickman
set CHROME_DATA=%LOCALAPPDATA%\Temp\stickman-chrome-debug
tasklist /FI "IMAGENAME eq chrome.exe" /FO CSV 2>nul | findstr /i "chrome.exe" >nul 2>nul
if %errorlevel% equ 0 (
    echo.
    echo Deseja encerrar TODAS as instancias do Chrome? (s/N)
    set /p RESP=>
    if /I "!RESP!"=="s" (
        taskkill /IM chrome.exe /F >nul 2>&1
        echo Todas as instancias do Chrome foram encerradas.
    )
)

endlocal

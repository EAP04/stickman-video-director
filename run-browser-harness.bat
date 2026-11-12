@echo off
:: Wrapper para browser-harness nesta maquina.
:: - Contorna o proxy do sistema que bloqueia localhost no Python
:: - Conecta o browser-harness ao Chrome com depuracao remota na porta 9222
:: - Repassa argumentos para o browser-harness
::
:: Uso no Git Bash:
::   ./run-browser-harness.bat <<'PY'
::   print(page_info())
::   PY
::
:: Uso no cmd / PowerShell:
::   ./run-browser-harness.bat print(page_info())
::

setlocal enabledelayedexpansion

set BH_PORT=9222
set BH_URL=http://127.0.0.1:%BH_PORT%
set BH_EXE=.venv\Scripts\browser-harness.exe

:: Contorna proxy corporativo para localhost
set no_proxy=127.0.0.1
set NO_PROXY=127.0.0.1

:: 1. Verifica se o browser-harness esta instalado
if not exist "%BH_EXE%" (
    echo ERRO: browser-harness nao encontrado em %BH_EXE%.
    echo Crie o ambiente e instale:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install browser-harness
    exit /b 1
)

:: 2. Verifica se o Chrome com depuracao ja esta no ar
curl -s -m 2 %BH_URL%/json/version >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERRO: Chrome com depuracao remota nao esta rodando na porta %BH_PORT%.
    echo.
    echo Feche todo o Chrome e execute primeiro:
    echo   start-chrome-debug.bat
    echo.
    echo Ou inicie manualmente com:
    echo   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=%BH_PORT% --user-data-dir="%%LOCALAPPDATA%%\Temp\stickman-chrome-debug" --no-first-run --no-default-browser-check
    echo.
    exit /b 1
)

echo Conectando o browser-harness ao Chrome em %BH_URL%...
set BU_CDP_URL=%BH_URL%

:: 3. Repassa argumentos (stdin/heredoc do Git Bash ou argumentos de linha de comando)
.\%BH_EXE% %*

endlocal

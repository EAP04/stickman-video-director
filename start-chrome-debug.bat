@echo off
:: Inicia o Chrome com um perfil TEMPORARIO (dedicado) e depuracao remota na porta 9222,
:: para que o browser-harness possa se conectar a ele.
::
:: O Chrome BLOQUEIA a depuracao remota quando se usa o diretorio de dados padrao
:: (%LOCALAPPDATA%\Google\Chrome\User Data). Por isso usamos um perfil temporario
:: separado, que nao traz seus logins/cookies mas permite a depuracao remota.
::
:: Uso:
::   start-chrome-debug.bat          (Git Bash ou cmd)
::
setlocal enabledelayedexpansion

set BH_PORT=9222
set CHROME_EXE="C:\Program Files\Google\Chrome\Application\chrome.exe"
set CHROME_DATA=%LOCALAPPDATA%\Temp\stickman-chrome-debug

:: 1. Se o Chrome ja estiver respondendo na porta, nao abre outro
curl -s -m 2 http://127.0.0.1:%BH_PORT%/json/version >nul 2>nul
if %errorlevel% equ 0 (
    echo Chrome com depuracao remota ja esta rodando na porta %BH_PORT%.
    echo Rode agora: ./run-browser-harness.bat
    exit /b 0
)

:: 2. Cria o diretorio do perfil temporario se nao existir
if not exist "%CHROME_DATA%\" mkdir "%CHROME_DATA%"

echo Iniciando Chrome com perfil temporario e depuracao remota na porta %BH_PORT%...

:: Abre o Chrome em segundo plano (sem bloquear este terminal)
start "" %CHROME_EXE% --remote-debugging-port=%BH_PORT% --user-data-dir="%CHROME_DATA%" --no-first-run --no-default-browser-check >nul 2>&1

echo Aguardando o Chrome subir...
timeout /t 12 >nul

:: 3. Verifica se a porta de depuracao respondeu
curl -s -m 5 http://127.0.0.1:%BH_PORT%/json/version >nul 2>nul
if %errorlevel% equ 0 (
    echo.
    echo OK: Chrome iniciado com sucesso na porta %BH_PORT%.
    echo Perfil temporario: %CHROME_DATA%
    echo.
    echo Rode agora: ./run-browser-harness.bat
) else (
    echo.
    echo ERRO: nao foi possivel verificar se o Chrome iniciou na porta %BH_PORT%.
    echo Tente iniciar manualmente com o comando acima ou feche todo o Chrome e rode novamente.
    exit /b 1
)

endlocal

# Inicia o Chrome com um perfil TEMPORARIO (dedicado) e depuracao remota na porta 9222,
# para que o browser-harness possa se conectar a ele.
#
# O Chrome bloqueia a depuracao remota quando se usa o diretorio de dados padrao
# (%LOCALAPPDATA%\Google\Chrome\User Data). Por isso usamos um perfil temporario
# separado, que nao traz seus logins/cookies mas permite a depuracao remota.
#
# Uso no PowerShell nativo:
#   ./start-chrome-debug.ps1

$ErrorActionPreference = "Stop"

$BH_PORT = 9222
$CHROME_EXE = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$CHROME_DATA = Join-Path -Path $env:LOCALAPPDATA -ChildPath "Temp\stickman-chrome-debug"

# 1. Se o Chrome ja estiver respondendo na porta, nao abre outro
try {
    $resp = Invoke-RestMethod -Uri "http://127.0.0.1:$BH_PORT/json/version" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "Chrome com depuracao remota ja esta rodando na porta $BH_PORT." -ForegroundColor Green
    Write-Host "Rode agora: ./run-browser-harness.ps1" -ForegroundColor Green
    exit 0
} catch {
    # Nao esta rodando, continua
}

# 2. Cria o diretorio do perfil temporario se nao existir
if (-not (Test-Path $CHROME_DATA)) {
    New-Item -ItemType Directory -Path $CHROME_DATA -Force | Out-Null
}

Write-Host "Iniciando Chrome com perfil temporario e depuracao remota na porta $BH_PORT..."

Start-Process -FilePath $CHROME_EXE -ArgumentList @(
    "--remote-debugging-port=$BH_PORT",
    "--user-data-dir=$CHROME_DATA",
    "--no-first-run",
    "--no-default-browser-check"
)

Write-Host "Aguardando o Chrome subir..."
Start-Sleep -Seconds 12

# 3. Verifica se a porta de depuracao respondeu
try {
    $resp = Invoke-RestMethod -Uri "http://127.0.0.1:$BH_PORT/json/version" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "`nOK: Chrome iniciado com sucesso na porta $BH_PORT.`n" -ForegroundColor Green
    Write-Host "Perfil temporario: $CHROME_DATA" -ForegroundColor Green
    Write-Host "Rode agora: ./run-browser-harness.ps1" -ForegroundColor Green
} catch {
    Write-Host "`nERRO: nao foi possivel verificar se o Chrome iniciou na porta $BH_PORT.`n" -ForegroundColor Red
    exit 1
}

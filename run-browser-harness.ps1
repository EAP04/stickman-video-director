# Wrapper para browser-harness nesta maquina.
# - Contorna o proxy do sistema que bloqueia localhost no Python
# - Conecta o browser-harness ao Chrome com depuracao remota na porta 9222
#
# Uso no PowerShell nativo:
#   ./run-browser-harness.ps1 -Code "print(page_info())"
#
# Uso no Git Bash (heredoc):
#   ./run-browser-harness.bat <<'PY'
#   print(page_info())
#   PY

param([string]$Code)

$ErrorActionPreference = "Stop"

$BH_PORT = 9222
$BH_URL = "http://127.0.0.1:$BH_PORT"
$BH_VENV = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\browser-harness.exe"

# Contorna proxy corporativo para localhost
$env:no_proxy = "127.0.0.1"
$env:NO_PROXY = "127.0.0.1"

# 1. Verifica se o browser-harness esta instalado
if (-not (Test-Path $BH_VENV)) {
    Write-Host "ERRO: browser-harness nao encontrado em $BH_VENV.`n" -ForegroundColor Red
    Write-Host "Crie o ambiente e instale:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .venv\Scripts\pip install browser-harness`n" -ForegroundColor Yellow
    exit 1
}

# 2. Verifica se o Chrome com depuracao ja esta no ar
$chromeUp = $false
try {
    $resp = Invoke-RestMethod -Uri "$BH_URL/json/version" -TimeoutSec 2 -ErrorAction Stop
    $chromeUp = $true
} catch {
    $chromeUp = $false
}

if (-not $chromeUp) {
    Write-Host "ERRO: Chrome com depuracao remota nao esta rodando na porta $BH_PORT.`n" -ForegroundColor Red
    Write-Host "Feche todo o Chrome e execute primeiro: ./start-chrome-debug.ps1`n" -ForegroundColor Yellow
    Write-Host "Ou inicie manualmente:`n" -ForegroundColor Yellow
    Write-Host "    ""C:\Program Files\Google\Chrome\Application\chrome.exe"" --remote-debugging-port=$BH_PORT --user-data-dir=""$env:LOCALAPPDATA\Temp\stickman-chrome-debug"" --no-first-run --no-default-browser-check`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "Conectando o browser-harness ao Chrome em $BH_URL..."
$env:BU_CDP_URL = $BH_URL

if ($Code) {
    # Escreve codigo no stdin do browser-harness
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $BH_VENV
    $startInfo.RedirectStandardInput = $true
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $process = [System.Diagnostics.Process]::Start($startInfo)
    $writer = $process.StandardInput
    $writer.Write($Code)
    $writer.Close()
    $process.WaitForExit()
    exit $process.ExitCode
} else {
    # Sem codigo: executa diretamente (stdin vindo do pipe/heredoc)
    & $BH_VENV @args
    exit $LASTEXITCODE
}

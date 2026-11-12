# Encerra o Chrome que esteja com depuracao remota na porta 9222.
# Uso: ./stop-chrome-debug.ps1

$ErrorActionPreference = "Continue"
$BH_PORT = 9222

# 1. Acha o processo que esteja ouvindo a porta 9222 e encerra
$netstat = netstat -ano | Select-String ":$BH_PORT" | Select-String "LISTENING"
if ($netstat) {
    $pids = ($netstat | ForEach-Object { $_.ToString().Split([char[]]@(' '), [StringSplitOptions]::RemoveEmptyEntries) | Select-Object -Last 1 }) | Select-Object -Unique
    foreach ($pid in $pids) {
        try {
            Stop-Process -Id $pid -Force -ErrorAction Stop
            Write-Host "Chrome na porta $BH_PORT (PID $pid) encerrado." -ForegroundColor Green
        } catch {
            Write-Host "Nao foi possivel encerrar o PID $pid (pode exigir administrador)." -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "Nenhum Chrome ouvindo na porta $BH_PORT foi encontrado." -ForegroundColor Yellow
}

# 2. Fallback: Pergunta se quer encerrar TODAS as instancias do Chrome
$chromeProcs = Get-Process -Name "chrome" -ErrorAction SilentlyContinue
if ($chromeProcs) {
    Write-Host ""
    $resp = Read-Host "Deseja encerrar TODAS as instancias do Chrome? (s/N)"
    if ($resp -eq "s") {
        Get-Process -Name "chrome" | Stop-Process -Force -ErrorAction SilentlyContinue
        Write-Host "Todas as instancias do Chrome foram encerradas." -ForegroundColor Green
    }
}

<#
.SYNOPSIS
ZeroFilter Anti-Idle Continuous Supervisor Watchdog
Ensures engine/anti_idle.py is perpetually running and resurrects it on any failure.
#>
$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   ZEROFILTER ANTI-IDLE DAEMON SUPERVISOR ACTIVATED        " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

while ($true) {
    $ts = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    Write-Host "[$ts] Starting Python Anti-Idle Supervisor..." -ForegroundColor Yellow
    
    try {
        & python -u engine/anti_idle.py
    } catch {
        Write-Host "[$ts] Error executing engine/anti_idle.py: $_" -ForegroundColor Red
    }
    
    $exitCode = $LASTEXITCODE
    Write-Host "[$ts] Anti-Idle supervisor exited with code $exitCode. Reviving in 3 seconds..." -ForegroundColor DarkYellow
    Start-Sleep -Seconds 3
}

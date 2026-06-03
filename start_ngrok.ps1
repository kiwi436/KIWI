# Script para lanzar Kiwi con ngrok
# Uso: .\start_ngrok.ps1

$ErrorActionPreference = "Stop"
$AppDir = $PSScriptRoot

Write-Host "=== KIWI + NGROK ===" -ForegroundColor Cyan

# 1. Lanzar Django en background
Write-Host "Iniciando servidor Django..." -ForegroundColor Yellow
$django = Start-Process -FilePath "python" `
    -ArgumentList "manage.py", "runserver", "8000" `
    -WorkingDirectory $AppDir `
    -PassThru -NoNewWindow
Write-Host "Django PID: $($django.Id)"

# 2. Esperar un momento para que Django levante
Start-Sleep -Seconds 3

# 3. Lanzar ngrok en background
Write-Host "Iniciando tunel ngrok..." -ForegroundColor Yellow
$ngrokProc = Start-Process -FilePath "ngrok" `
    -ArgumentList "http", "8000", "--log", "stdout" `
    -PassThru -NoNewWindow -RedirectStandardOutput "$AppDir\ngrok.log"
Write-Host "ngrok PID: $($ngrokProc.Id)"

Start-Sleep -Seconds 4

# 4. Obtener URL publica de ngrok via API local
try {
    $tunnels = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
    $url = ($tunnels.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1).public_url
    if (-not $url) {
        $url = ($tunnels.tunnels | Select-Object -First 1).public_url
    }
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  URL publica: $url" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""

    # 5. Actualizar .env con la URL y CSRF_TRUSTED_ORIGINS
    $envPath = "$AppDir\.env"
    $envContent = Get-Content $envPath -Raw

    # Actualizar SITE_URL
    $envContent = $envContent -replace "(?m)^SITE_URL=.*$", "SITE_URL=$url"
    if ($envContent -notmatch "(?m)^SITE_URL=") {
        $envContent += "`nSITE_URL=$url"
    }

    # Actualizar CSRF_TRUSTED_ORIGINS
    $envContent = $envContent -replace "(?m)^CSRF_TRUSTED_ORIGINS=.*$", "CSRF_TRUSTED_ORIGINS=$url"
    if ($envContent -notmatch "(?m)^CSRF_TRUSTED_ORIGINS=") {
        $envContent += "`nCSRF_TRUSTED_ORIGINS=$url"
    }

    $envContent | Set-Content $envPath -Encoding utf8 -NoNewline
    Write-Host "Archivo .env actualizado con la URL de ngrok." -ForegroundColor Cyan
    Write-Host "Reiniciando Django para aplicar el nuevo SITE_URL..."

    # 6. Reiniciar Django para que cargue el nuevo .env
    Stop-Process -Id $django.Id -Force
    Start-Sleep -Seconds 1
    Start-Process -FilePath "python" `
        -ArgumentList "manage.py", "runserver", "8000" `
        -WorkingDirectory $AppDir `
        -NoNewWindow
    Write-Host "Django relanzado. La app esta disponible en:" -ForegroundColor Green
    Write-Host "  $url" -ForegroundColor Green

} catch {
    Write-Host "No se pudo obtener la URL de ngrok automaticamente." -ForegroundColor Red
    Write-Host "Revisa http://127.0.0.1:4040 en tu navegador para ver la URL." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Presiona Ctrl+C para detener." -ForegroundColor Gray
Wait-Process -Id $ngrokProc.Id

# Local quality gate for PH00-M03 (Windows PowerShell).
# Usage (from repo root): .\scripts\local_quality.ps1
#
# Included: backend ruff/pytest, Flutter format/analyze/unit tests, compose config.
# Not included (run separately): live e2e Dio tags, interactive flutter run,
# Alembic against a live DB, Ollama connectivity.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Native {
    param(
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )
    Write-Host "-> $Label"
    & $Command
    if ($null -eq $LASTEXITCODE) {
        throw "Native command produced no exit code: $Label"
    }
    if ($LASTEXITCODE -ne 0) {
        throw "FAILED ($LASTEXITCODE): $Label"
    }
}

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$venvPython = Join-Path $Root "services\backend\.venv\Scripts\python.exe"
$venvRuff = Join-Path $Root "services\backend\.venv\Scripts\ruff.exe"
$venvPytest = Join-Path $Root "services\backend\.venv\Scripts\pytest.exe"

if (-not (Test-Path $venvPython)) {
    throw "Missing project venv at services\backend\.venv. Create it before running this script."
}

Write-Host "== Backend =="
Push-Location (Join-Path $Root "services\backend")
try {
    if (-not $env:DATABASE_URL) {
        $env:DATABASE_URL = "postgresql+psycopg://fitness:fitness_dev_only@127.0.0.1:15432/fitness_ai"
    }
    $env:APP_ENV = "test"
    Invoke-Native { & $venvRuff check app tests } "ruff check"
    Invoke-Native { & $venvRuff format --check app tests } "ruff format --check"
    Invoke-Native { & $venvPytest -q } "pytest"
}
finally {
    Pop-Location
}

Write-Host "== Mobile =="
Push-Location (Join-Path $Root "apps\mobile")
try {
    Invoke-Native { flutter pub get } "flutter pub get"
    Invoke-Native { dart format --set-exit-if-changed . } "dart format"
    Invoke-Native { flutter analyze } "flutter analyze"
    Invoke-Native { flutter test --exclude-tags e2e } "flutter test (unit/widget)"
}
finally {
    Pop-Location
}

Write-Host "== Compose config =="
Invoke-Native {
    docker compose -f (Join-Path $Root "infrastructure\docker-compose.yml") config | Out-Null
} "docker compose config"

Write-Host "Local quality gate completed."
exit 0

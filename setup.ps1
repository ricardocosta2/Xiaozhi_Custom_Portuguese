# XIAOZHI Custom Portuguese - Setup / Ferramentas locais
# Uso:
#   .\setup.ps1            # cria venv + instala ESPHome (primeira vez)
#   .\setup.ps1 -CheckAssets # verifica docs/imagens/wallpapers vs configs
#   .\setup.ps1 -Validate  # valida todos os YAMLs de Devices/Modular (esphome config)
#   .\setup.ps1 -Validate -Config "Devices/Modular/Ball v2.yaml"
#   .\setup.ps1 -Compile -Config "Devices/Modular/Ball v2.yaml"
#   .\setup.ps1 -UpdateEsphome
#
# Requisitos: Python 3.10+ e o repositório clonado em disco.

param(
    [switch]$Validate,
    [switch]$Compile,
    [switch]$UpdateEsphome,
    [switch]$CheckAssets,
    [string]$Config = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = $PSScriptRoot
$VenvDir  = Join-Path $RepoRoot ".venv"
$Esphome  = Join-Path $VenvDir "Scripts\esphome.exe"
$ModularDir = Join-Path $RepoRoot "Devices\Modular"
$Version = "2026.7.3"

function Ensure-Venv {
    if (-not (Test-Path $Esphome)) {
        Write-Host "==> A criar venv em $VenvDir ..."
        python -m venv $VenvDir
        if (-not (Test-Path $Esphome)) {
            throw "Falha ao criar a venv. Confirma que o Python 3.10+ está no PATH."
        }
    }
    $ver = & $Esphome version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "ESPHome instalado mas não funciona: $ver"
    }
    Write-Host "==> ESPHome: $ver"
}

function Install-Esphome {
    Write-Host "==> A instalar/atualizar ESPHome $Version ..."
    & python -m pip install --upgrade "esphome==$Version"
    if ($LASTEXITCODE -ne 0) { throw "Falha ao instalar o ESPHome." }
}

function New-TempSecrets {
    # O core.yaml usa !secret wifi_ssid / wifi_password para validação local.
    $secrets = Join-Path $ModularDir "secrets.yaml"
    Set-Content -LiteralPath $secrets -Value "wifi_ssid: `"local-wifi`"`nwifi_password: `"local-password`"" -Encoding UTF8
    return $secrets
}

function Remove-TempSecrets {
    $secrets = Join-Path $ModularDir "secrets.yaml"
    if (Test-Path $secrets) { Remove-Item -LiteralPath $secrets -Force }
}

function Get-ConfigList {
    if ($Config) {
        if (-not (Test-Path (Join-Path $RepoRoot $Config))) {
            throw "Config não encontrado: $Config"
        }
        return @($Config)
    }
    return @(Get-ChildItem (Join-Path $RepoRoot "Devices\Modular") -Filter "*.yaml" | Where-Object { $_.Name -notlike "secrets*" } | ForEach-Object { "Devices\Modular\$($_.Name)" })
}

function Invoke-CheckAssets {
    Write-Host "==> A verificar docs, imagens e wallpapers (tools/check_assets.py) ..."
    & python (Join-Path $RepoRoot "tools\check_assets.py")
    if ($LASTEXITCODE -ne 0) { throw "Assets/documentação em falta (ver erros acima)." }
}

function Invoke-Validate {
    Invoke-CheckAssets
    $secrets = New-TempSecrets
    try {
        $failed = 0
        foreach ($cfg in Get-ConfigList) {
            Write-Host "`n=== Validando $cfg ==="
            & $Esphome config (Join-Path $RepoRoot $cfg)
            if ($LASTEXITCODE -ne 0) { $failed = 1 }
        }
        if ($failed -ne 0) { throw "Uma ou mais configurações falharam a validação." }
        Write-Host "`n==> Todas as configurações são válidas."
    }
    finally {
        Remove-TempSecrets
    }
}

function Invoke-Compile {
    if (-not $Config) {
        throw "Usa -Compile com -Config ""Devices/Modular/Ball v2.yaml"" (ou outro YAML)."
    }
    $secrets = New-TempSecrets
    try {
        Write-Host "==> A compilar $Config ... (MAX_PATH do Windows: corre a partir de uma pasta curta se der erro de path)"
        & $Esphome compile (Join-Path $RepoRoot $Config)
        if ($LASTEXITCODE -ne 0) { throw "Falha na compilação de $Config" }
        Write-Host "`n==> Compilado com sucesso. O firmware .bin está em .esphome/build/<nome>/..."
    }
    finally {
        Remove-TempSecrets
    }
}

# ---- main --------------------------------------------------------------------
if ($UpdateEsphome) {
    Ensure-Venv
    Install-Esphome
    exit 0
}

if ($CheckAssets) {
    Invoke-CheckAssets
    exit 0
}

if (-not (Test-Path $Esphome)) {
    Ensure-Venv
    Install-Esphome
} else {
    Ensure-Venv
}

if ($CheckAssets) { Invoke-CheckAssets }
elseif ($Validate) { Invoke-Validate }
elseif ($Compile) { Invoke-Compile }
else {
    Write-Host @"
Setup local pronto.
Comandos disponíveis:
  .\setup.ps1 -CheckAssets                 verifica docs/imagens/wallpapers vs configs
  .\setup.ps1 -Validate                    valida todos os YAMLs modulares
  .\setup.ps1 -Validate -Config <yaml>     valida apenas um config
  .\setup.ps1 -Compile -Config <yaml>      compila firmware (gera .bin)
  .\setup.ps1 -UpdateEsphome               atualiza o ESPHome na venv
"@
}

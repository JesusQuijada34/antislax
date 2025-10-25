# Winslax.ps1 - Optimizador de Rendimiento y Eliminador de Bloatware para Windows

<#
.SYNOPSIS
  Script de PowerShell para optimizar Windows, eliminar bloatware,
  desactivar telemetría y servicios innecesarios para un mejor rendimiento,
  especialmente en juegos.
.DESCRIPTION
  Este script realiza varias tareas de optimización de forma segura y reversible.
  Debe ejecutarse con permisos de Administrador.
#>

# --- 1. Funciones de Ayuda ---

function Set-ExecutionPolicyIfNeeded {
    param([string]$Policy = "Bypass")
    if ((Get-ExecutionPolicy) -ne $Policy) {
        Write-Host "Configurando la política de ejecución a '$Policy'..." -ForegroundColor Yellow
        Set-ExecutionPolicy -ExecutionPolicy $Policy -Scope Process -Force
    }
}

function Write-Success {
    param([string]$Message)
    Write-Host "[ÉXITO] $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[ADVERTENCIA] $Message" -ForegroundColor Yellow
}

# --- 2. Verificación de Permisos ---

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Este script debe ejecutarse como Administrador. Por favor, reinicie con privilegios elevados." -ForegroundColor Red
    exit 1
}

Set-ExecutionPolicyIfNeeded

# --- 3. Eliminación de Bloatware (Apps de la Tienda) ---

Write-Host "`n--- 3. Eliminación de Bloatware de la Tienda (AppX) ---" -ForegroundColor White

$BloatwareList = @(
    "*3DBuilder*", "*BingNews*", "*BingWeather*", "*GetHelp*", "*Getstarted*",
    "*Microsoft.ZuneVideo*", "*Microsoft.XboxApp*", "*Microsoft.People*",
    "*Microsoft.WindowsFeedbackHub*", "*Microsoft.SkypeApp*", "*solitairecollection*",
    "*CandyCrush*", "*Messaging*", "*OfficeHub*", "*OneNote*", "*Sway*",
    "*WindowsMaps*", "*XboxGameCallableUI*", "*XboxIdentityProvider*",
    "*XboxSpeechToText*", "*ZuneMusic*"
)

foreach ($App in $BloatwareList) {
    Write-Info "Intentando desinstalar la aplicación: $App"
    try {
        Get-AppxPackage -AllUsers -Name $App | Remove-AppxPackage -ErrorAction Stop
        Write-Success "Desinstalado: $App"
    } catch {
        Write-Warning "No se pudo desinstalar o no se encontró: $App. (Puede que ya no esté instalado o que sea una aplicación del sistema)."
    }
}

# --- 4. Desactivación de Telemetría y Recopilación de Datos ---

Write-Host "`n--- 4. Desactivación de Telemetría y Recopilación de Datos ---" -ForegroundColor White

# Desactivar la Telemetría a través del Registro
$TelemetryKey = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\DataCollection"
if (-not (Test-Path $TelemetryKey)) {
    New-Item -Path $TelemetryKey -Force | Out-Null
}
Set-ItemProperty -Path $TelemetryKey -Name "AllowTelemetry" -Value 0 -Type DWord -Force
Write-Success "Telemetría de Windows desactivada (Registro)."

# Desactivar el Servicio de Experiencias de Usuario Conectado y Telemetría
$DiagTrackService = "DiagTrack"
try {
    Set-Service -Name $DiagTrackService -StartupType Disabled -ErrorAction Stop
    Stop-Service -Name $DiagTrackService -Force -ErrorAction SilentlyContinue
    Write-Success "Servicio 'Experiencias de Usuario Conectado y Telemetría' ($DiagTrackService) desactivado."
} catch {
    Write-Warning "No se pudo desactivar el servicio $DiagTrackService. Puede que no exista."
}

# --- 5. Optimización de Servicios Innecesarios (Modo Gamer/Rendimiento) ---

Write-Host "`n--- 5. Optimización de Servicios Innecesarios (Modo Gamer) ---" -ForegroundColor White

# Servicios para desactivar (Manual o Deshabilitado)
$ServicesToDisable = @(
    "Fax", # Si no se usa fax
    "PrintSpooler", # Si no se usa impresora
    "RemoteRegistry", # Riesgo de seguridad y rara vez necesario
    "TabletInputService", # Servicio de Panel de entrada y Escritura a mano (si no se usa)
    "SysMain", # Superfetch/Prefetch - a veces puede ralentizar SSDs
    "dmwappushservice", # Servicio de administración de dispositivos
    "CDPSvc", # Servicio de plataforma de dispositivos conectados
    "WSearch" # Windows Search - si no se usa la búsqueda frecuentemente
)

foreach ($Service in $ServicesToDisable) {
    try {
        $CurrentStatus = (Get-Service -Name $Service -ErrorAction Stop).Status
        Set-Service -Name $Service -StartupType Disabled -ErrorAction Stop
        Stop-Service -Name $Service -Force -ErrorAction SilentlyContinue
        Write-Success "Servicio '$Service' deshabilitado. (Estado anterior: $CurrentStatus)"
    } catch {
        Write-Warning "No se pudo deshabilitar el servicio '$Service'. Puede que no exista o que sea esencial."
    }
}

# --- 6. Ajustes de Rendimiento del Sistema ---

Write-Host "`n--- 6. Ajustes de Rendimiento del Sistema ---" -ForegroundColor White

# Desactivar la hibernación (libera espacio en disco)
try {
    & powercfg /hibernate off
    Write-Success "Hibernación desactivada."
} catch {
    Write-Warning "No se pudo desactivar la hibernación."
}

# Ajustar la configuración de energía a Alto Rendimiento (si no está ya)
try {
    $HighPerformanceGUID = (Get-CimInstance -ClassName Win32_PowerPlan | Where-Object { $_.ElementName -like "*High Performance*" -or $_.ElementName -like "*Máximo rendimiento*" -or $_.ElementName -like "*Alto rendimiento*" }).InstanceID
    if ($HighPerformanceGUID) {
        & powercfg /setactive $HighPerformanceGUID.Split('{')[1].Split('}')[0]
        Write-Success "Plan de energía configurado a Alto Rendimiento."
    } else {
        Write-Warning "No se encontró el plan de Alto Rendimiento. Saltando este paso."
    }
} catch {
    Write-Warning "No se pudo configurar el plan de energía."
}

# --- 7. Finalización y Reinicio Sugerido ---

Write-Host "`n=======================================================" -ForegroundColor Yellow
Write-Host "Optimización de Winslax completada." -ForegroundColor Green
Write-Host "Para que los cambios surtan efecto, es ALTAMENTE RECOMENDABLE reiniciar el sistema." -ForegroundColor Yellow
Write-Host "=======================================================" -ForegroundColor Yellow

# Preguntar si desea reiniciar
$Response = Read-Host "Desea reiniciar el sistema ahora? (S/N)"
if ($Response -ceq "S") {
    Write-Info "Reiniciando el sistema en 5 segundos..."
    Start-Sleep -Seconds 5
    Restart-Computer -Force
} else {
    Write-Info "Reinicie manualmente cuando sea conveniente."
}

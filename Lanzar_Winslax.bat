@echo off
ECHO.
ECHO ==========================================================
ECHO  Iniciando Winslax - Optimizador de Rendimiento de Windows
ECHO ==========================================================
ECHO.

:: Comprueba si se está ejecutando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    ECHO Se requieren permisos de Administrador.
    ECHO Intentando reiniciar con privilegios elevados...
    ECHO.
    goto UACPrompt
) else (
    goto StartScript
)

:UACPrompt
    ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    ECHO UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /b

:StartScript
    :: Ejecuta el script de PowerShell con la política de ejecución en Bypass
    PowerShell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Winslax.ps1"
    ECHO.
    ECHO ==========================================================
    ECHO  Ejecución de Winslax finalizada.
    ECHO ==========================================================
    pause

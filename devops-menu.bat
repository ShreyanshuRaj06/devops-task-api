@echo off
REM DevOps Task Manager - CLI Launcher
REM Launches interactive Python menu or PowerShell script

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    py "%~dp0devops_menu.py" %*
) else (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0devops-menu.ps1" %*
)

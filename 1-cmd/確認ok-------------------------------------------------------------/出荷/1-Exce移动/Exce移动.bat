@echo off
chcp 65001 >nul

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Exce移动.ps1"

pause
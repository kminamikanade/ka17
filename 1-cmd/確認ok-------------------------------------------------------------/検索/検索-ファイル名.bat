@echo off
chcp 65001 >nul

powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0検索-ファイル名.ps1"


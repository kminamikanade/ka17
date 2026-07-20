@echo off
chcp 65001 >nul
echo ========================================
echo   ログイン状態保存ツール
echo ========================================
echo.
echo  ※ このツールは初回のみ実行してください。
echo    ログイン後、状態が保存されます。
echo.

REM Pythonスクリプトを実行
python "%~dp0login_save.py"

echo.
echo 処理が完了しました。Enterキーを押して終了します。
pause >nul
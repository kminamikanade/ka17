@echo off
chcp 65001 >nul
echo ========================================
echo   社内Webサイト ファイル自動ダウンロードツール
echo ========================================
echo.

python "%~dp0download_files.py"

echo.
echo 処理が完了しました。Enterキーを押して終了します。
pause >nul
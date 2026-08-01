@echo off
setlocal
cd /d "%~dp0"

echo Starting YaadKar backend...
start "YaadKar Backend" cmd /k ".\.venv311\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000"

echo Opening the Chrome extensions page...
where chrome.exe >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "YaadKar Extension" chrome.exe "chrome://extensions"
) else (
    echo Chrome was not found on PATH. Please open Chrome manually and go to chrome://extensions
)

echo.
echo Next steps:
echo 1. In Chrome, turn on Developer mode.
echo 2. Click Load unpacked and choose the extension folder.
echo 3. Open a YouTube video and use the extension.
echo.
pause

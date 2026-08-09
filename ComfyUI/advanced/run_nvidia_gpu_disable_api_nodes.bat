@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

start /b "" "..\python_embeded\python.exe" -s "..\ComfyUI\main.py" --windows-standalone-build --use-sage-attention --disable-api-nodes --disable-auto-launch

echo Checking Port 8188 status...

:WAIT_LOOP
netstat -an | findstr /C:":8188" | findstr "LISTENING" >nul
if !errorlevel! equ 0 (
    echo [OK] Backend is ready. Launching default browser...
    goto LAUNCH_BROWSER
) else (
    ping -n 2 127.0.0.1 >nul
    goto WAIT_LOOP
)

:LAUNCH_BROWSER
explorer "http://127.0.0.1:8188"

echo ================================================================
echo ComfyUI (API Nodes Disabled) started successfully.
echo If you get a c10.dll error, install: https://aka.ms/vc14/vc_redist.x64.exe
echo ================================================================
pause
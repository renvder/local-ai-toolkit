@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Cleaning up any stale process on port 8188...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /C:":8188" ^| findstr "LISTENING"') do (
    echo Killing stale process PID %%p ...
    taskkill /F /PID %%p >nul 2>&1
)

ping -n 2 127.0.0.1 >nul

start /b "" ".\python_embeded\python.exe" -s "ComfyUI\main.py" --windows-standalone-build --disable-auto-launch

echo Checking Port 8188 for NVIDIA GPU Optimized session...

:WAIT_LOOP
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8188' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] GPU Backend is ready. Launching default browser...
    goto LAUNCH_BROWSER
) else (
    ping -n 2 127.0.0.1 >nul
    goto WAIT_LOOP
)

:LAUNCH_BROWSER
explorer "http://127.0.0.1:8188"

echo ================================================================
echo ComfyUI (NVIDIA GPU Optimized) started successfully.
echo ================================================================
pause

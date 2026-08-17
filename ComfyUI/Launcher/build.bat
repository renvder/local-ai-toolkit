@echo off
title ComfyUI Launcher - Build EXE

python --version
if %errorlevel% neq 0 (
    echo Python not found.
    pause
    exit /b 1
)

pip install pyinstaller -q

if exist "ComfyUI_Launcher.pyw" (
    copy "ComfyUI_Launcher.pyw" "_tmp.py" >nul
    
    pyinstaller --onefile --windowed --name "ComfyUI_Launcher" ^
                --icon="Comfy_Logo_x256.ico" ^
                --clean "_tmp.py"
    
    del "_tmp.py" >nul 2>nul
) else (
    echo Source file not found. Put this bat in the same folder as the .pyw file.
    pause
    exit /b 1
)

if exist "ComfyUI_Launcher.spec" del "ComfyUI_Launcher.spec" >nul 2>nul
if exist "build" rmdir /s /q "build" >nul 2>nul

echo.
echo Done! Output: dist\ComfyUI_Launcher.exe
explorer dist
pause
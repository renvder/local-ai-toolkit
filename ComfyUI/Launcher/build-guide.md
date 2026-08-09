# ComfyUI Launcher EXE Build Guide

This guide explains how to use `build.bat` to package `ComfyUI_Launcher.pyw` as a standalone Windows EXE file.

---

## 1. Requirements

### Operating System

```text
Windows 10 / Windows 11
```

### Python Environment

Install a system-wide version of Python and make sure it is added to the system `PATH`.

Recommended versions:

```text
Python 3.10 / 3.11 / 3.12
```

Open CMD or PowerShell and confirm that these commands work:

```powershell
python --version
```

```powershell
python -m pip --version
```

> This build process uses the system `python` and `pip` commands. It does not use ComfyUI Portable's `python_embeded\python.exe`.

---

## 2. Required Python Package

### PyInstaller

The `build.bat` script installs PyInstaller automatically:

```bat
pip install pyinstaller -q
```

You can also install or update it manually:

```powershell
python -m pip install --upgrade pyinstaller
```

### No Additional Modules Required

The following modules used by `ComfyUI_Launcher.pyw` are included in the Python standard library and do not require separate `pip` installation:

```text
tkinter
subprocess
threading
os
ctypes
time
datetime
concurrent.futures
base64
tempfile
webbrowser
re
socket
sys
```

---

## 3. Required File Structure

Create a folder for the build process and place these three files in the same folder:

```text
ComfyUI_Launcher.pyw
build.bat
Comfy_Logo_x256.ico
```

Example:

```text
Launcher/
├── ComfyUI_Launcher.pyw
├── build.bat
└── Comfy_Logo_x256.ico
```

| File | Purpose |
|---|---|
| `ComfyUI_Launcher.pyw` | ComfyUI Launcher Python source code |
| `build.bat` | Automatically installs PyInstaller and runs the build process |
| `Comfy_Logo_x256.ico` | Custom icon for the EXE file |

---

## 4. Build Steps

1. Confirm that all three files are in the same folder.
2. Double-click:

   ```text
   build.bat
   ```

3. The script will automatically:

   - Check whether system Python is available.
   - Install PyInstaller.
   - Create a temporary Python file required for packaging.
   - Package the launcher as a single EXE file.
   - Apply `Comfy_Logo_x256.ico` as the EXE icon.
   - Clean up temporary files created during the build process.
   - Create the `dist` output folder automatically.
   - Open the `dist` folder automatically.

---

## 5. Output File

After the build is complete, the EXE file will be located at:

```text
dist\ComfyUI_Launcher.exe
```

The final folder structure will look like this:

```text
Launcher/
├── ComfyUI_Launcher.pyw
├── build.bat
├── Comfy_Logo_x256.ico
└── dist/
    └── ComfyUI_Launcher.exe
```

---

## 6. Notes

- Do not rename `ComfyUI_Launcher.pyw`, `build.bat`, or `Comfy_Logo_x256.ico` unless the corresponding settings in `build.bat` have also been updated.
- After packaging, copy `dist\ComfyUI_Launcher.exe` to the ComfyUI root folder before using it.
- The EXE may start more slowly the first time. This is normal for a single-file packaged application.
- This build process does not require ComfyUI Portable's embedded Python environment.

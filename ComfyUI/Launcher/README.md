# ComfyUI Launcher

A lightweight desktop launcher for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) on Windows. It provides a simple GUI to start/stop ComfyUI, update the core and custom nodes, install extensions from Git, and open the web UI.

Place `ComfyUI_Launcher.pyw` (or the built `.exe`) in the **ComfyUI root directory** (same level as `run_nvidia_gpu.bat`).

---

## Features

| Feature | Description |
|--------|-------------|
| **Standard Launch** | Starts ComfyUI via `run_nvidia_gpu.bat` |
| **Disable API Nodes** | Starts ComfyUI with API nodes disabled (`advanced\run_nvidia_gpu_disable_api_nodes.bat`) |
| **Stop** | Stops the running ComfyUI process (by process and by port 8188) |
| **Open UI** | Opens `http://127.0.0.1:8188` in the browser |
| **Update ComfyUI** | Runs the official update script (`update\update_comfyui.bat`) |
| **Update All Extensions** | Checks and pulls updates for all Git-based custom nodes in parallel |
| **Install Extension** | Clones a custom node from a Git URL into `ComfyUI\custom_nodes` and optionally installs its `requirements.txt` |
| **Live Log** | Streams ComfyUI output with color-coded levels (info / success / warn / error) |

---

## Requirements (runtime)

- Windows 10/11
- A working ComfyUI portable (or similar) layout with:
  - `run_nvidia_gpu.bat`
  - `advanced\run_nvidia_gpu_disable_api_nodes.bat` (optional, for “Disable API Nodes”)
  - `update\update_comfyui.bat`
  - `ComfyUI\custom_nodes\`
  - `python_embeded\python.exe` (used when installing extension requirements)
- Git (for update extensions / install extension)

No extra Python is required to **run** the launcher if you use the packaged `.exe`.

---

## Build EXE on Windows

Follow these steps to package `ComfyUI_Launcher.pyw` into a single-file executable.

### 1. Install Python

1. Download the official installer from:  
   https://www.python.org/downloads/  
   (Python 3.10 or newer is recommended.)

2. Run the installer.

3. **Important:** On the first page of the installer, check  
   **“Add python.exe to PATH”**.

4. Click **Install Now** and finish the setup.

5. Verify in a new Command Prompt:

```bat
python --version
```

You should see something like `Python 3.12.x`. If the command is not found, reopen the terminal or reinstall Python with “Add to PATH” enabled.

### 2. Install PyInstaller

Open **Command Prompt** (or PowerShell) and run:

```bat
pip install pyinstaller
```

Optional quiet install (same as the build script):

```bat
pip install pyinstaller -q
```

### 3. Prepare files

Put these files in the **same folder**:

| File | Description |
|------|-------------|
| `ComfyUI_Launcher.pyw` | Source script |
| `Comfy_Logo_x256.ico` | Application icon |
| `build.bat` | One-click build script (optional) |

### 4. Build

**Option A — Use the provided script (recommended)**

1. Double-click `build.bat`, or run it from the folder:

```bat
cd /d "C:\path\to\your\folder"
build.bat
```

2. The script will:
   - Check that Python is available
   - Install PyInstaller if needed
   - Copy the `.pyw` to a temporary `.py` (PyInstaller works better with `.py`)
   - Build a one-file, windowed EXE named `ComfyUI_Launcher.exe`
   - Clean up temporary files
   - Open the `dist` folder when finished

**Option B — Manual command**

In the folder that contains the source and icon:

```bat
copy ComfyUI_Launcher.pyw _tmp.py
pyinstaller --onefile --windowed --name "ComfyUI_Launcher" --icon="Comfy_Logo_x256.ico" --clean _tmp.py
del _tmp.py
```

### 5. Output

After a successful build you will get:

```
dist\ComfyUI_Launcher.exe
```

Copy this EXE into your **ComfyUI root directory** (alongside `run_nvidia_gpu.bat`) and run it from there.

---

## Notes

- The launcher must live in the ComfyUI root so it can find the batch scripts and `custom_nodes`.
- Building requires a normal Python install + PyInstaller; running the finished EXE does not.
- If antivirus software flags the EXE, add an exception or rebuild with a clean environment; this is common for PyInstaller one-file apps.
- Icon file name in the build command must match exactly: `Comfy_Logo_x256.ico`.

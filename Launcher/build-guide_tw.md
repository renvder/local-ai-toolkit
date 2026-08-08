# ComfyUI Launcher EXE 打包步驟

本指南說明如何使用 `build.bat`，將 `ComfyUI_Launcher.pyw` 打包為獨立的 Windows EXE 檔案。

---

## 一、所需環境

### 作業系統

```text
Windows 10 / Windows 11
```

### Python 環境

請先安裝系統版 Python，並確認 Python 已加入系統環境變數 `PATH`。

建議版本：

```text
Python 3.10 / 3.11 / 3.12
```

開啟 CMD 或 PowerShell，確認以下指令可正常執行：

```powershell
python --version
```

```powershell
python -m pip --version
```

> 此打包流程使用系統環境中的 `python` 與 `pip`，不使用 ComfyUI Portable 內的 `python_embeded\python.exe`。

---

## 二、所需 Python 套件

### PyInstaller

`build.bat` 會自動安裝 PyInstaller：

```bat
pip install pyinstaller -q
```

也可以手動安裝或更新：

```powershell
python -m pip install --upgrade pyinstaller
```

### 不需要額外安裝的模組

`ComfyUI_Launcher.pyw` 使用的以下模組皆為 Python 標準函式庫，不需要使用 `pip` 額外安裝：

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

## 三、打包前檔案結構

新建一個用於打包的資料夾，並將以下三個檔案放入同一個資料夾：

```text
ComfyUI_Launcher.pyw
build.bat
Comfy_Logo_x256.ico
```

範例：

```text
ComfyUI-Launcher-Build/
├── ComfyUI_Launcher.pyw
├── build.bat
└── Comfy_Logo_x256.ico
```

| 檔案 | 用途 |
|---|---|
| `ComfyUI_Launcher.pyw` | ComfyUI 啟動器 Python 原始碼 |
| `build.bat` | 自動安裝 PyInstaller 並執行打包 |
| `Comfy_Logo_x256.ico` | EXE 使用的程式圖示 |

---

## 四、執行打包

1. 確認三個檔案位於同一個資料夾。
2. 雙擊執行：

   ```text
   build.bat
   ```

3. 腳本會自動執行以下操作：

   - 檢查系統 Python 是否可用。
   - 自動安裝 PyInstaller。
   - 暫時建立打包所需的 Python 檔案。
   - 將啟動器打包為單一 EXE 檔案。
   - 將 `Comfy_Logo_x256.ico` 寫入 EXE 圖示。
   - 清除打包過程產生的暫存檔案。
   - 自動建立 `dist` 輸出資料夾。
   - 自動開啟 `dist` 資料夾。

---

## 五、打包完成後

打包完成後，EXE 檔案位於：

```text
dist\ComfyUI_Launcher.exe
```

最終資料夾結構會類似：

```text
ComfyUI-Launcher-Build/
├── ComfyUI_Launcher.pyw
├── build.bat
├── Comfy_Logo_x256.ico
└── dist/
    └── ComfyUI_Launcher.exe
```

---

## 六、注意事項

- `ComfyUI_Launcher.pyw`、`build.bat` 與 `Comfy_Logo_x256.ico` 的檔案名稱不可隨意更改，除非已同步修改 `build.bat` 內的對應設定。
- 打包完成後，可將 `dist\ComfyUI_Launcher.exe` 複製到 ComfyUI 根目錄使用。
- EXE 首次開啟可能稍慢，這是單檔打包格式的正常現象。
- 此打包程序本身不需要使用 ComfyUI Portable 的內建 Python 環境。

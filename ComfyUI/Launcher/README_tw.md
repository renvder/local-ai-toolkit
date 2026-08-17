# ComfyUI Launcher

適用於 Windows 的 [ComfyUI](https://github.com/comfyanonymous/ComfyUI) 輕量桌面啟動器。提供簡易圖形介面，可啟動／停止 ComfyUI、更新核心與自訂節點、從 Git 安裝擴充，並開啟網頁介面。

請將 `ComfyUI_Launcher.pyw`（或打包後的 `.exe`）放在 **ComfyUI 根目錄**（與 `run_nvidia_gpu.bat` 同一層）。

---

## 功能一覽

| 功能 | 說明 |
|------|------|
| **標準啟動** | 透過 `run_nvidia_gpu.bat` 啟動 ComfyUI |
| **停用 API 節點** | 以停用 API 節點模式啟動（`advanced\run_nvidia_gpu_disable_api_nodes.bat`） |
| **停止** | 停止正在執行的 ComfyUI 行程（依行程與 8188 埠） |
| **開啟介面** | 在瀏覽器開啟 `http://127.0.0.1:8188` |
| **更新 ComfyUI** | 執行官方更新腳本（`update\update_comfyui.bat`） |
| **更新所有擴充** | 並行檢查並拉取所有以 Git 管理的自訂節點更新 |
| **安裝擴充** | 從 Git 網址將自訂節點複製到 `ComfyUI\custom_nodes`，並可選擇安裝其 `requirements.txt` |
| **即時日誌** | 串流顯示 ComfyUI 輸出，並依等級著色（資訊／成功／警告／錯誤） |

---

## 執行環境需求

- Windows 10／11
- 可用的 ComfyUI 可攜版（或類似目錄結構），需包含：
  - `run_nvidia_gpu.bat`
  - `advanced\run_nvidia_gpu_disable_api_nodes.bat`（選用，供「停用 API 節點」）
  - `update\update_comfyui.bat`
  - `ComfyUI\custom_nodes\`
  - `python_embeded\python.exe`（安裝擴充相依套件時使用）
- Git（用於更新擴充／安裝擴充）

若使用已打包的 `.exe`，**執行啟動器時不需要另外安裝 Python**。

---

## 在 Windows 打包成 EXE

請依下列步驟將 `ComfyUI_Launcher.pyw` 打包成單一執行檔。

### 1. 安裝 Python

1. 至官方網站下載安裝程式：  
   https://www.python.org/downloads/  
   （建議使用 Python 3.10 或更新版本。）

2. 執行安裝程式。

3. **重要：** 在安裝程式第一頁勾選  
   **「Add python.exe to PATH」**（將 python.exe 加入 PATH）。

4. 點選 **Install Now** 完成安裝。

5. 開啟新的「命令提示字元」，輸入以下指令確認：

```bat
python --version
```

應會顯示類似 `Python 3.12.x`。若提示找不到指令，請重新開啟終端機，或重新安裝並勾選「Add to PATH」。

### 2. 安裝 PyInstaller

開啟「命令提示字元」（或 PowerShell），執行：

```bat
pip install pyinstaller
```

若要靜默安裝（與建置腳本相同）：

```bat
pip install pyinstaller -q
```

### 3. 準備檔案

請將下列檔案放在**同一資料夾**：

| 檔案 | 說明 |
|------|------|
| `ComfyUI_Launcher.pyw` | 原始碼腳本 |
| `Comfy_Logo_x256.ico` | 應用程式圖示 |
| `build.bat` | 一鍵建置腳本（選用） |

### 4. 建置

**方式 A — 使用提供的腳本（建議）**

1. 雙擊 `build.bat`，或在該資料夾執行：

```bat
cd /d "C:\path\to\your\folder"
build.bat
```

2. 腳本會：
   - 檢查是否已安裝 Python
   - 必要時安裝 PyInstaller
   - 將 `.pyw` 複製為暫存 `.py`（PyInstaller 對 `.py` 較穩定）
   - 建置單檔、無主控台視窗的 EXE，名稱為 `ComfyUI_Launcher.exe`
   - 清理暫存檔
   - 完成後開啟 `dist` 資料夾

**方式 B — 手動指令**

在含有原始碼與圖示的資料夾中執行：

```bat
copy ComfyUI_Launcher.pyw _tmp.py
pyinstaller --onefile --windowed --name "ComfyUI_Launcher" --icon="Comfy_Logo_x256.ico" --clean _tmp.py
del _tmp.py
```

### 5. 輸出結果

建置成功後會產生：

```
dist\ComfyUI_Launcher.exe
```

請將此 EXE 複製到 **ComfyUI 根目錄**（與 `run_nvidia_gpu.bat` 同一層），並在該處執行。

---

## 注意事項

- 啟動器必須放在 ComfyUI 根目錄，才能正確找到批次檔與 `custom_nodes`。
- 建置時需要一般的 Python 安裝與 PyInstaller；完成後的 EXE 執行時不需要。
- 若防毒軟體對 EXE 產生警示，可加入例外或在乾淨環境重新建置；PyInstaller 單檔應用常見此情況。
- 建置指令中的圖示檔名必須完全一致：`Comfy_Logo_x256.ico`。

# SageAttention 安裝指南

適用於 **Windows 11 + ComfyUI Portable（便攜版）**。

## 環境需求

- Python：`3.13`
- PyTorch：`2.13.0+cu130`

---

## 1. 可選：安裝 Visual Studio C++ 建置工具

> 此步驟目前通常**不是必要條件**。
>
> 自 `triton-windows 3.2.0.post13` 起，wheel 已內建 TinyCC 編譯器。像 SageAttention 這類僅使用 `triton.jit` 的套件，通常不需要手動安裝 MSVC 編譯工具。
>
> 若不需要其他編譯用途，可直接跳至 [第 2 步](#2-安裝-triton)。

如果仍想安裝 Visual Studio C++ 建置工具，例如未來需要使用 `torch.compile` 的 CPU 編譯功能，請在 **Visual Studio Installer** 中選擇 C++ 建置工具，並只勾選：

- `適用於 x64/x86 的 MSVC 生成工具（最新版）`
- `Windows 11 SDK`

其他工作負載與元件通常不需要安裝。

> [!IMPORTANT]
> 無論是否安裝上述建置工具，都建議確認系統已安裝 **Visual C++ Redistributable**。
>
> `libtriton.pyd` 是以 MSVC 編譯；若缺少或版本過舊，可能出現：
>
> ```text
> ImportError: DLL load failed while importing libtriton
> ```
>
> 可從以下連結下載並安裝：
>
> [下載 Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

## 2. 安裝 Triton

在 **ComfyUI 根目錄** 開啟 PowerShell 或命令提示字元，執行：

```powershell
.\python_embeded\python.exe -m pip install -U "triton-windows<3.8"
```

> [!NOTE]
> 將 Triton 限制為 `<3.8`，可避免未來 Triton 大版本更新後，與目前 PyTorch 版本發生相容性問題。

---

## 3. 安裝 Python 3.13 開發檔案

> [!IMPORTANT]
> 此步驟必須執行。

下載以下壓縮檔：

[下載 `python_3.13.2_include_libs.zip`](https://github.com/woct0rdho/triton-windows/releases/download/v3.0.0-windows.post1/python_3.13.2_include_libs.zip)

解壓縮後，將其中的 `include` 和 `libs` 資料夾完整複製至 ComfyUI 內嵌 Python 目錄。

範例路徑：

```text
F:\Software\ComfyUI Portable\python_embeded\
```

完成後的目錄結構應如下：

```text
python_embeded/
├── include/
└── libs/
```

> [!CAUTION]
> 請確認是 `libs`，不是 `lib`。
>
> `python_embeded` 目錄中原本可能已有 `Lib` 資料夾，用於存放 `site-packages` 等內容。請勿將新複製的 `libs` 與既有的 `Lib` 混淆，也不要覆蓋原本的 `Lib` 資料夾。

---

## 4. 安裝 SageAttention

下載與目前環境相容的 wheel 檔案：

```text
sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

下載連結：

[下載 SageAttention v2.2.0 Windows Post 6](https://github.com/woct0rdho/SageAttention/releases/download/v2.2.0-windows.post6/sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl)

將下載完成的 `.whl` 檔案放到 **ComfyUI 根目錄**，再執行：

```powershell
.\python_embeded\python.exe -m pip install .\sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

---

## 5. 啟用 SageAttention

編輯下列啟動腳本：

```text
run_nvidia_gpu.bat
advanced\run_nvidia_gpu_disable_api_nodes.bat
```

在 ComfyUI 的啟動命令最後加入：

```text
--use-sage-attention
```

範例：

```bat
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-sage-attention
```

---

## 6. 驗證是否啟用成功

啟動 ComfyUI 後，檢查終端機或日誌輸出。

若出現以下訊息，代表 SageAttention 已成功啟用：

```text
Using sage attention
```

---

## 疑難排解

### `ImportError: DLL load failed while importing libtriton`

通常代表 Visual C++ Runtime 缺失或版本過舊。

1. 重新安裝 [Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe)。
2. 確認 `python_embeded` 目錄中的 `vcruntime140.dll`、`msvcp140.dll` 等檔案未被舊版檔案覆蓋。
3. 安裝完成後重新啟動 ComfyUI。

### `ImportError: DLL load failed while importing cuda_utils`

請依序檢查：

1. 刪除 Triton 快取目錄：

   ```text
   C:\Users\<使用者名稱>\.triton\cache\
   ```

2. 確認 `include` 與 `libs` 已放入 `python_embeded` 目錄。
3. 確認下載的開發檔案與目前使用的 Python 版本一致，例如 Python `3.13`。

### 更新 ComfyUI Portable 後無法使用

ComfyUI Portable 更新時，可能會一併更新 Python、PyTorch 或 CUDA 版本。

請重新確認以下版本是否仍相容：

- `triton-windows`
- SageAttention wheel
- Python `include` 與 `libs` 開發檔案

必要時請重新執行本指南的第 2 至第 4 步。

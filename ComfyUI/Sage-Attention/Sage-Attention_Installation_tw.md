# Sage Attention 正確安裝步驟  
**Windows 11 + ComfyUI 便攜版**

## 環境

- Python `3.13`
- PyTorch `2.13.0+cu130`

---

## 1.（可選）使用 Visual Studio Installer 安裝建置工具

> **此步驟現已非必要。** 自 `triton-windows 3.2.0.post13` 起，wheel 內已內建 TinyCC 編譯器，像 SageAttention 這類只呼叫 `triton.jit` 的套件不再需要手動安裝 MSVC 編譯工具。若你想略過本步驟，可直接跳到第 2 步。
>
> 若你仍想安裝（例如日後要用到 `torch.compile` targeting CPU 等情境），可開啟 **Visual Studio Installer**，安裝 C++ 建置工具時，只勾選以下兩項：
>
> - `適用於 x64/x86 的 MSVC 生成工具（最新版）`
> - `Windows 11 SDK`
>
> 其他選項不需要勾選。

> **提醒：** 不論是否安裝上述建置工具，都建議確認已安裝 **Visual C++ Redistributable**（`msvcp140.dll`、`vcruntime140.dll` 等），因為 `libtriton.pyd` 是由 MSVC 編譯的。若之後遇到 `ImportError: DLL load failed while importing libtriton` 之類的錯誤，通常就是這個原因，可從下方連結安裝：
>
> [Visual C++ Redistributable（直接下載）](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

## 2. 安裝 Triton

在 **ComfyUI 根目錄** 開啟終端機，執行：

```powershell
.\python_embeded\python.exe -m pip install -U "triton-windows<3.8"
```

> 鎖定版本 `<3.8` 是為了避免未來 Triton 大版本更新時與目前安裝的 PyTorch 版本不相容。

---

## 3. 安裝 Python 3.13 開發檔案

> 此步驟為必須執行。

下載：

[python_3.13.2_include_libs.zip](https://github.com/woct0rdho/triton-windows/releases/download/v3.0.0-windows.post1/python_3.13.2_include_libs.zip)

解壓縮後，將其中的 `include` 與 `libs` 兩個資料夾完整複製到：

```text
F:\Software\ComfyUI Portable\python_embeded\
```

完成後，資料夾結構應類似：

```text
F:\Software\ComfyUI Portable\python_embeded\
├── include\
└── libs\
```

> **注意：** 是 `libs`，不是 `lib`。`python_embeded` 資料夾內原本可能就有一個 `Lib` 資料夾（存放 `site-packages` 等），請勿與新複製進來的 `libs` 混淆或覆蓋。

---

## 4. 安裝 SageAttention

下載與目前環境相符的 wheel 檔案：

```text
sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

下載地址：

[SageAttention v2.2.0 Windows Post 6](https://github.com/woct0rdho/SageAttention/releases/download/v2.2.0-windows.post6/sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl)

將下載好的 `.whl` 檔案放入 **ComfyUI 根目錄**，然後執行：

```powershell
.\python_embeded\python.exe -m pip install .\sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

---

## 5. 啟用 Sage Attention

編輯以下兩個檔案：

```text
run_nvidia_gpu.bat
advanced\run_nvidia_gpu_disable_api_nodes.bat
```

在 ComfyUI 的啟動命令後方加上：

```text
--use-sage-attention
```

範例：

```bat
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-sage-attention
```

---

## 6. 啟動驗證

啟動 ComfyUI 後，檢查終端機或日誌輸出。

出現以下訊息即代表 Sage Attention 已成功啟用：

```text
Using sage attention
```

---

## 疑難排解

- **`ImportError: DLL load failed while importing libtriton`**：通常是 vcredist 版本過舊，請重新安裝 [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe)，並確認 `python_embeded` 資料夾內的 `vcruntime140.dll` 等檔案版本夠新。
- **`ImportError: DLL load failed while importing cuda_utils`**：先刪除快取資料夾 `C:\Users\<使用者名稱>\.triton\cache\`，並再次確認 `include` 與 `libs` 是否對應到正確的 Python 版本（3.13）。
- 若更新了 ComfyUI Portable 版本（可能連帶更新 Python / PyTorch / CUDA 版本），請回到第 2～4 步，改用對應新版本的 Triton 與 SageAttention wheel。

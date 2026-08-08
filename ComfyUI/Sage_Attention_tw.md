# Sage Attention 正確安裝步驟  
**Windows 11 + ComfyUI 便攜版**

## 環境

- Python `3.13`
- PyTorch `2.13.0+cu130`

---

## 1. 使用 Visual Studio Installer 安裝建置工具

開啟 **Visual Studio Installer**，安裝 C++ 建置工具時，只勾選以下兩項：

- `適用於 x64/x86 的 MSVC 生成工具（最新版）`
- `Windows 11 SDK`

> 其他選項不需要勾選。

---

## 2. 安裝 Triton

在 **ComfyUI 根目錄** 開啟終端機，執行：

```powershell
.\python_embeded\python.exe -m pip install -U "triton-windows<3.8"
```

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

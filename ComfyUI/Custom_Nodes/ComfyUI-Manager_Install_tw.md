# 在 ComfyUI Portable 安裝 ComfyUI-Manager

## 安裝步驟

1. 開啟 `ComfyUI_windows_portable` 資料夾。

2. 下載官方安裝腳本：

```text
install-manager-for-portable-version.bat
```

3. 將腳本放入 `ComfyUI_windows_portable` 資料夾。

4. 執行安裝腳本：

```text
install-manager-for-portable-version.bat
```

5. 安裝完成後，正常啟動 ComfyUI：

```text
run_nvidia_gpu.bat
```

6. 使用瀏覽器開啟 ComfyUI，介面選單中會出現 **Manager** 按鈕。

## 資料夾結構

完成後的資料夾結構如下：

```text
ComfyUI_windows_portable/
├── ComfyUI/
│   └── custom_nodes/
│       └── comfyui-manager/
├── python_embeded/
├── run_nvidia_gpu.bat
└── install-manager-for-portable-version.bat
```

ComfyUI-Manager 已安裝完成，可以開始使用。

# Install ComfyUI-Manager on ComfyUI Portable

## Installation Steps

1. Open the `ComfyUI_windows_portable` folder.

2. Download the official installation script:

   [install-manager-for-portable-version.bat](https://github.com/ltdrdata/ComfyUI-Manager/raw/main/scripts/install-manager-for-portable-version.bat)

3. Place the script into the `ComfyUI_windows_portable` folder.

4. Run the script:

```text
install-manager-for-portable-version.bat
```

5. After installation is complete, start ComfyUI normally:

```text
run_nvidia_gpu.bat
```

6. Open ComfyUI in your browser. The **Manager** button will appear in the menu.

## Folder Structure

The final structure should look like this:

```text
ComfyUI_windows_portable/
├── ComfyUI/
│   └── custom_nodes/
│       └── comfyui-manager/
├── python_embeded/
├── run_nvidia_gpu.bat
└── install-manager-for-portable-version.bat
```

ComfyUI-Manager is now installed and ready to use.

# SageAttention Installation Guide

> **Platform:** Windows 11 + ComfyUI Portable

## Environment

- Python: `3.13`
- PyTorch: `2.13.0+cu130`

---

## 1. Optional: Install Visual Studio Build Tools

> [!NOTE]
> This step is no longer required.
>
> Since `triton-windows 3.2.0.post13`, the wheel includes a bundled TinyCC compiler. Packages that only use `triton.jit`, such as SageAttention, no longer require manually installed MSVC build tools.
>
> You may skip directly to [Step 2](#2-install-triton).

If you still want to install the build tools—for example, for future CPU-targeted `torch.compile` usage—open **Visual Studio Installer** and install the C++ build tools with only the following components selected:

- `MSVC v143 build tools for x64/x86 (latest)`
- `Windows 11 SDK`

No other components are required.

> [!IMPORTANT]
> Regardless of whether you install the build tools above, make sure **Visual C++ Redistributable** is installed.
>
> `libtriton.pyd` is compiled with MSVC and depends on files such as `msvcp140.dll` and `vcruntime140.dll`. If you encounter the following error, an outdated or missing Visual C++ Runtime is usually the cause:
>
> ```text
> ImportError: DLL load failed while importing libtriton
> ```
>
> [Download Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

## 2. Install Triton

Open PowerShell or Command Prompt in the **ComfyUI root directory**, then run:

```powershell
.\python_embeded\python.exe -m pip install -U "triton-windows<3.8"
```

> [!NOTE]
> The `<3.8` version limit helps prevent a future major Triton release from becoming incompatible with the currently installed PyTorch version.

---

## 3. Install Python 3.13 Development Files

> [!IMPORTANT]
> This step is required.

Download the following archive:

[Download `python_3.13.2_include_libs.zip`](https://github.com/woct0rdho/triton-windows/releases/download/v3.0.0-windows.post1/python_3.13.2_include_libs.zip)

Extract the archive, then copy both the `include` and `libs` folders into your ComfyUI embedded Python directory.

Example destination:

```text
F:\Software\ComfyUI Portable\python_embeded\
```

The resulting directory structure should look similar to this:

```text
python_embeded/
├── include/
└── libs/
```

> [!CAUTION]
> The required folder is named `libs`, not `lib`.
>
> The `python_embeded` directory may already contain a `Lib` folder, which stores `site-packages` and other Python files. Do not confuse it with the new `libs` folder, and do not overwrite the existing `Lib` folder.

---

## 4. Install SageAttention

Download the wheel file that matches your current environment:

```text
sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

Download link:

[Download SageAttention v2.2.0 Windows Post 6](https://github.com/woct0rdho/SageAttention/releases/download/v2.2.0-windows.post6/sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl)

Place the downloaded `.whl` file in the **ComfyUI root directory**, then run:

```powershell
.\python_embeded\python.exe -m pip install .\sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

---

## 5. Enable SageAttention

Edit the following launch scripts:

```text
run_nvidia_gpu.bat
advanced\run_nvidia_gpu_disable_api_nodes.bat
```

Append this argument to the end of the ComfyUI launch command:

```text
--use-sage-attention
```

Example:

```bat
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-sage-attention
```

---

## 6. Verify the Installation

Launch ComfyUI and check the terminal or log output.

If the following message appears, SageAttention is enabled successfully:

```text
Using sage attention
```

---

## Troubleshooting

### `ImportError: DLL load failed while importing libtriton`

This is usually caused by a missing or outdated Visual C++ Runtime.

1. Reinstall [Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe).
2. Check that files such as `vcruntime140.dll` and `msvcp140.dll` in `python_embeded` are not outdated or overwritten by older versions.
3. Restart ComfyUI after installation.

### `ImportError: DLL load failed while importing cuda_utils`

Check the following:

1. Delete the Triton cache folder:

   ```text
   C:\Users\<username>\.triton\cache\
   ```

2. Verify that the `include` and `libs` folders are located directly inside `python_embeded`.
3. Confirm that the development files match the embedded Python version, which should be Python `3.13`.

### SageAttention Stops Working After Updating ComfyUI Portable

Updating ComfyUI Portable may also update Python, PyTorch, or CUDA.

Recheck compatibility for the following components:

- `triton-windows`
- SageAttention wheel
- Python development files: `include` and `libs`

If necessary, repeat [Steps 2–4](#2-install-triton) using the versions compatible with the updated ComfyUI environment.

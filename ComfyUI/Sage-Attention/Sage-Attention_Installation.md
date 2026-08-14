# Correct Sage Attention Installation Steps  
**Windows 11 + ComfyUI Portable**

## Environment

- Python `3.13`
- PyTorch `2.13.0+cu130`

---

## 1. (Optional) Install Build Tools via Visual Studio Installer

> **This step is no longer required.** Since `triton-windows 3.2.0.post13`, the wheel ships with a bundled TinyCC compiler, so packages that only call `triton.jit` (like SageAttention) no longer need MSVC build tools installed manually. You can skip straight to Step 2 if you like.
>
> If you still want to install it (e.g. for future use with `torch.compile` targeting CPU, etc.), open **Visual Studio Installer**, and when installing C++ build tools, check only these two:
>
> - `MSVC v143 build tools for x64/x86 (latest)`
> - `Windows 11 SDK`
>
> No other options are needed.

> **Note:** Regardless of whether you install the build tools above, it's recommended to make sure the **Visual C++ Redistributable** is installed (`msvcp140.dll`, `vcruntime140.dll`, etc.), since `libtriton.pyd` is compiled with MSVC. If you later hit an error like `ImportError: DLL load failed while importing libtriton`, this is usually the cause. You can install it here:
>
> [Visual C++ Redistributable (direct download)](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

## 2. Install Triton

Open a terminal in the **ComfyUI root folder** and run:

```powershell
.\python_embeded\python.exe -m pip install -U "triton-windows<3.8"
```

> The version cap `<3.8` prevents a future major Triton release from breaking compatibility with your currently installed PyTorch version.

---

## 3. Install Python 3.13 Development Files

> This step is required.

Download:

[python_3.13.2_include_libs.zip](https://github.com/woct0rdho/triton-windows/releases/download/v3.0.0-windows.post1/python_3.13.2_include_libs.zip)

After extracting, copy the `include` and `libs` folders into:

```text
F:\Software\ComfyUI Portable\python_embeded\
```

The folder structure should end up looking like this:

```text
F:\Software\ComfyUI Portable\python_embeded\
├── include\
└── libs\
```

> **Note:** It's `libs`, not `lib`. The `python_embeded` folder may already contain a `Lib` folder (holding `site-packages`, etc.) — don't confuse it with, or overwrite it with, the newly copied `libs` folder.

---

## 4. Install SageAttention

Download the wheel file matching your current environment:

```text
sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

Download link:

[SageAttention v2.2.0 Windows Post 6](https://github.com/woct0rdho/SageAttention/releases/download/v2.2.0-windows.post6/sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl)

Place the downloaded `.whl` file in the **ComfyUI root folder**, then run:

```powershell
.\python_embeded\python.exe -m pip install .\sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

---

## 5. Enable Sage Attention

Edit both of the following files:

```text
run_nvidia_gpu.bat
advanced\run_nvidia_gpu_disable_api_nodes.bat
```

Append the following flag to the end of the ComfyUI launch command:

```text
--use-sage-attention
```

Example:

```bat
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-sage-attention
```

---

## 6. Verify the Installation

After launching ComfyUI, check the terminal or log output.

If you see the following message, Sage Attention has been enabled successfully:

```text
Using sage attention
```

---

## Troubleshooting

- **`ImportError: DLL load failed while importing libtriton`**: Usually caused by an outdated vcredist. Reinstall [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe) and verify that `vcruntime140.dll` and similar files in the `python_embeded` folder are up to date.
- **`ImportError: DLL load failed while importing cuda_utils`**: First delete the cache folder `C:\Users\<username>\.triton\cache\`, then double-check that the `include` and `libs` folders match your actual Python version (3.13).
- If you update ComfyUI Portable (which may also update Python / PyTorch / CUDA), go back to Steps 2–4 and use the Triton and SageAttention wheels matching the new versions.

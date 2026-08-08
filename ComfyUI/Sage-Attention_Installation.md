# Sage Attention Installation Guide  
**Windows 11 + ComfyUI Portable**

## Environment 

- Python `3.13`
- PyTorch `2.13.0+cu130`

---

## 1. Install Visual Studio Build Tools

Install **Visual Studio Installer**, then install the C++ build tools.

Only select these two individual components:

- `MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)`
- `Windows 11 SDK`

> Other components are not required for this setup.

---

## 2. Install Triton

Open a terminal in the **ComfyUI root folder** and run:

```powershell
.\python_embeded\python.exe -m pip install -U "triton-windows<3.8"
```

---

## 3. Install Python 3.13 Development Files

> This step is required.

Download:

[python_3.13.2_include_libs.zip](https://github.com/woct0rdho/triton-windows/releases/download/v3.0.0-windows.post1/python_3.13.2_include_libs.zip)

Extract the archive. Copy its `include` and `libs` folders into:

```text
F:\Software\ComfyUI Portable\python_embeded\
```

After copying, the structure should look similar to:

```text
F:\Software\ComfyUI Portable\python_embeded\
├── include\
└── libs\
```

---

## 4. Install SageAttention

Download the wheel matching your environment:

```text
sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

Download link:

[SageAttention v2.2.0 Windows Post 6](https://github.com/woct0rdho/SageAttention/releases/download/v2.2.0-windows.post6/sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl)

Place the downloaded `.whl` file in the **ComfyUI root folder**.

Then run:

```powershell
.\python_embeded\python.exe -m pip install .\sageattention-2.2.0+cu130torch2.10.0andhigher.post6-cp310-abi3-win_amd64.whl
```

---

## 5. Enable Sage Attention

Edit both files:

```text
run_nvidia_gpu.bat
advanced\run_nvidia_gpu_disable_api_nodes.bat
```

Add this parameter to the ComfyUI launch command:

```text
--use-sage-attention
```

Example:

```bat
.\python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --use-sage-attention
```

---

## 6. Verify Installation

Start ComfyUI and check the terminal/log output.

If Sage Attention is enabled successfully, you should see:

```text
Using sage attention
```

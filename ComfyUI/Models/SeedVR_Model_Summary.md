# SeedVR Model Summary

## Workflows

-  **[SeedVR2.5+TTP_HQ_Upscale.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/SeedVR2.5%2BTTP_HQ_Upscale.json)**
    - Features advanced high-quality upscaling using the TTP (Tile-based Processing) technique, supporting large scale image enhancement and resolution restoration for video content.

## Models Required for All Workflows

To run the SeedVR related workflows, the following models are required:
- **`seedvr2_ema_7b_sharp_fp16.safetensors`** (Checkpoint / 7B Model)
- **`seedvr2_ema_3b_fp8_e4m3fn.safetensors`** (Checkpoint / 3B Model)
- **`ema_vae_fp16.safetensors`** (VAE for SeedVR series)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching any workflow.

## Download Links and Path Details

| Type | Filename | Model page / direct download | Target folder |
|---|---|---|---|
| Checkpoint | `seedvr2_ema_7b_sharp_fp16.safetensors` | [Hugging Face](https://huggingface.co/ainvfx/SeedVR2-Weights) | `ComfyUI/models/checkpoints` |
| Checkpoint | `seedvr2_ema_3b_fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/ainvfx/SeedVR2-Weights) | `ComfyUI/models/checkpoints` |
| VAE | `ema_vae_fp16.safetensors` | [Hugging Face](https://huggingface.co/ainvfx/SeedVR2-Weights) | `ComfyUI/models/vae` |

## Directory Structure

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   ├── seedvr2_ema_7b_sharp_fp16.safetensors
│   │   └── seedvr2_ema_3b_fp8_e4m3fn.safetensors
│   └── vae/
│       └── ema_vae_fp16.safetensors

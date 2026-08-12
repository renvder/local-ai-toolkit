# LTX Model Summary

## Workflows

1.  **[LTX-2.3_F2V_First-Last.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/LTX-2.3_F2V_First-Last.json)**
    - Features a "First-Last" frame logic, allowing for transitions between two specific images provided as start and end points.

2.  **[LTX-2.3_I2V_Simple.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/LTX-2.3_I2V_Simple.json)**
    - A standard Image-to-Video (I2V) pipeline for generating motion from a single source image.

3.  **[LTX-2.3_I2V_Two-Stage_Upscale.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/LTX-2.3_I2V_Two-Stage_Upscale.json)**
    - Includes a two-stage process incorporating a dedicated latent upscaler to enhance resolution during the generation process.

## Models Required for All Workflows

To run any of the three LTX-related workflows, the following models are required:
- **`ltx-2.3-22b-distilled-fp8.safetensors`** (Checkpoint/Main Model)
- **`LTX23_video_vae_bf16.safetensors`** (VAE for Video)
- **`LTX23_audio_vae_bf16.safetensors`** (VAE for Audio)
- **`gemma-3-12b-it-heretic-v2_fp8_e4m3fn.safetensors`** (Text Encoder 1)
- **`ltx-2.3_text_projection_bf16.safetensors`** (Text Encoder 2)
- **`ltx-2.3-spatial-upscaler-x2-1.1.safetensors`** (Latent Upscale Model - required for the Two-Stage workflow)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching any workflow.

## Download Links and Path Details

| Type | Filename | Model page / direct download | Target folder |
|---|---|---|---|
| Checkpoint | `ltx-2.3-22b-distilled-fp8.safetensors` | [Hugging Face / Source](https://huggingface.co/Lightricks/LTX-2.3-fp8/resolve/main/ltx-2.3-22b-distilled-fp8.safetensors) | `ComfyUI/models/checkpoints` |
| VAE | `LTX23_video_vae_bf16.safetensors` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3_video_vae_bf16.safetensors) | `ComfyUI/models/vae` |
| VAE | `LTX23_audio_vae_bf16.safetensors` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx_audio_vae_bf16.safetensors) | `ComfyUI/models/vae` |
| text_encoders | `gemma-3-12b-it-heretic-v2_fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/ltx-2) | `ComfyUI/models/text_encoders` |
| text_encoders | `ltx-2.3_text_projection_bf16.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/ltx-2) | `ComfyUI/models/text_encoders` |
| latent_upscale_model | `ltx-2.3-spatial-upscaler-x2-1.1.safetensors` | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.1.safetensors) | `ComfyUI/models/latent_upscale_models` |

## Directory Structure

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── ltx-2.3-22b-distilled-fp8.safetensors
│   ├── vae/
│   │   ├── LTX23_video_vae_bf16.safetensors
│   │   └── LTX23_audio_vae_bf16.safetensors
│   ├── text_encoders/
│   │   ├── gemma-3-12b-it-heretic-v2_fp8_e4m3fn.safetensors
│   │   └── ltx-2.3_text_projection_bf16.safetensors
│   └── latent_upscale_models/
│       └── ltx-2.3-spatial-upscaler-x2-1.1.safetensors

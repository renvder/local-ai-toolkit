# Wan 2.1 InfiniTetalk: Single Audio-Driven Video Model Summary

## Workflow

- **[Wan-2.1_InfiniTetalk_Single.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Wan-2.1_InfiniTetalk_Single.json)**
    - **Core Functionality:** Seamlessly generates coherent and infinitely narrative videos based on images (visuals), text (prompts), and audio (speech).
    - **Modality Fusion:** The workflow involves deep integration of four core modalities:
        *   **Image Embedding:** Uses `WanVideoClipVisionEncode` to extract spatio-temporal information from images.
        *   **Text Embedding:** Uses `WanVideoTextEncode` to encode prompts and guide the video content.
        *   **Diffusion (Core Generation):** Utilizes `WanVideoModelLoader` and `WanVideoSampler` to complete final video generation and detail enhancement.
    - **Advanced Controls:** Supports advanced video parameter controls, including:
        *   **Image Resize:** Allows for dimensions adjustment and upscaling before input.
        *   **Audio Cropping:** Precisely controls the start and end times of the audio (`AudioCrop`).
        *   **Model and Parameter Management:** The workflow features multiple built-in loaders and complex calculation nodes to manage various model versions and parameters.

## Required Models for the Workflow

This workflow relies on a series of specialized models for multimedia encoding and inference.

- **Core WAN Model:**
    - `Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors` (For image-to-video generation)
- **Text Encoder (CLIP/T5):**
    - `umt5-xxl-enc-fp8_e4m3fn.safetensors` (For text prompt encoding)
    - `clip_vision_h.safetensors` (For visual feature extraction from images)
- **VAE:**
    - `wan_2.1_vae.safetensors` (Dedicated video/audio VAE encoder)

## Download Links and Directory Paths

| Type | File Name | Model Page / Direct Download | Target Folder |
| :--- | :--- | :--- | :--- |
| Diffusion Models | `Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors) | `ComfyUI/models/diffusion_models/` |
| Text Encoder | `umt5-xxl-enc-fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors) | `ComfyUI/models/text_encoders/` |
| CLIP Vision | `clip_vision_h.safetensors` | [Hugging Face](https://huggingface.co/calcuis/wan-gguf/resolve/f52f5a1f0ba441d50277fb7cdd7c1b36611837f9/clip_vision_h.safetensors) | `ComfyUI/models/clip_vision/` |
| VAE | `wan_2.1_vae.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors) | `ComfyUI/models/vae/` |

## Directory Structure

```text
ComfyUI/
└── models/
    ├── clip_vision/
    │   └── clip_vision_h.safetensors
    ├── diffusion_models/
    │   └── Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors
    ├── text_encoders/
    │   └── umt5-xxl-enc-fp8_e4m3fn.safetensors
    └── vae/
        └── wan_2.1_vae.safetensors

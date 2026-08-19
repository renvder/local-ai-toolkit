# MiniMax H3 Multi-Modal Image to Video Model Summary

## Workflows

1.  **[Minimax-H3_I2V_First-Last.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Minimax-H3_I2V_First-Last.json)**
    - **Core Functionality:** Image-to-Video (I2V) generation. This is a highly advanced, multi-modal workflow that combines **sound, vision, and text** as a single input for generation.
    - **Key Features:**
        *   **Cross-Media Integration:** Generates video with continuous narrative and accompanying soundscapes by combining text (Prompt), a first frame image (`first_frame`), and a last frame image (`last_frame`).
        *   **Native Stereo Audio:** The model generates native stereo audio containing voices, sound effects (SFX), and music, rather than simply layering them afterward.
        *   **Motion Control:** Precise control over video motion and narrative transitions using fixed keyframes (`first_frame` / `last_frame`).
    - **Main Nodes:** `MiniMaxH3ImageToVideo` (Core generation), `VAEDecodeAudio` (Audio decoding), `CreateVideo` (Video synthesis).

## Models Required for All Workflows

This workflow requires specialized models covering the UNET architecture, multi-modal CLIP encoder, and dedicated audio/video encoders.

- **Diffusion Model:**
    - `minimax_h3_fl2va_pruned_int8_convrot.safetensors` (The core UNET model for I2V generation)
- **Text Encoder:**
    - `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` (For processing complex multi-modal prompts)
- **VAE:**
    - `minimax_h3_video_vae_fp16.safetensors` (For video encoding/decoding)
    - `minimax_h3_audio_vae_fp32.safetensors` (For audio encoding/decoding, ensuring high audio fidelity)
- **LoRA:**
    - `minimax_h3_turbo_4step_ema_ckpt500.safetensors` (Used to boost generation quality and detail)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching any workflow.

## Download Links and Path Details

| Type | Filename | Model page / direct download | Target folder |
| :--- | :--- | :--- | :--- |
| diffusion models | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors) | `ComfyUI/models/diffusion_models/` |
| text encoders | `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors) | `ComfyUI/models/text_encoders/` |
| VAE (Video) | `minimax_h3_video_vae_fp16.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors) | `ComfyUI/models/vae/` |
| VAE (Audio) | `minimax_h3_audio_vae_fp32.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors) | `ComfyUI/models/vae/` |
| LoRA | `minimax_h3_turbo_4step_ema_ckpt500.safetensors` | [Hugging Face](https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora/resolve/main/minimax_h3_turbo_4step_ema_ckpt500.safetensors) | `ComfyUI/models/loras/` |

## Directory Structure

```text
ComfyUI/
└── models/
    ├── vae/
    │   ├── minimax_h3_video_vae_fp16.safetensors
    │   └── minimax_h3_audio_vae_fp32.safetensors
    ├── diffusion_models/
    │   └── minimax_h3_fl2va_pruned_int8_convrot.safetensors
    ├── text_encoders/
    │   └── qwen3vl_32b_minimax_h3_int8_convrot.safetensors
    └── loras/
        └── minimax_h3_turbo_4step_ema_ckpt500.safetensors

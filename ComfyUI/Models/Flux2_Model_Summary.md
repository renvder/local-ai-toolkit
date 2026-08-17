# Flux2 Series Workflow Model Summary

## Workflows
1. **[Flux2_Klein_4B_Outpaint.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Klein_4B_Outpaint.json)**
   - **Functionality:** Image Outpainting/Canvas Expansion. Uses the original image and a mask to naturally extend scene content onto a larger canvas.
   - **Unique Needs:** Specifically utilizes the 4B model and professional graphic processing nodes like `ImageScaleToTotalPixels` and `ImagePadKJ` for advanced dimensional and edge handling.

2. **[Flux2_Dual_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Dual_Image_Edit.json)**
   - **Functionality:** Allows users to input two images simultaneously (Image A and Image B) and perform detailed image restoration or style transfer controlled by a text prompt.
   - **Unique Needs:** Handling multiple image input streams (Image A and Image B) and converting them into reference latents for Flux 2 conditioning.

3. **[Flux2_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Image_Edit.json)**
   - **Functionality:** Prompt Combination & Style Editing. Combines separate textual parameters (like "Perspective," "Lighting," and "Style") using multiple `PrimitiveStringMultiline` nodes to generate a single, complex, and highly descriptive composite prompt.
   - **Unique Needs:** Focuses on advanced textual prompt construction capability.

4. **[Flux2_Prompt_Reverse_to_Image.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Prompt_Reverse_to_Image.json)**
   - **Functionality:** Prompt Reverse Engineering. Uses an input image with the `AILab_QwenVL` node to optimize and expand user prompts, generating richer prompt ideas for image generation.
   - **Unique Needs:** Integration of a multi-modal LLM (QwenVL) node for prompt optimization.

## Models Required for All Workflows
This Flux2 workflow series requires multiple versions and components depending on model size and specific task (9B vs 4B).

- **Diffusion Model (Unet):**
    - `flux-2-klein-9b-fp8.safetensors` (9B Model, for complex editing, e.g., Dual-Edit)
    - `flux-2-klein-4b.safetensors` (4B Model, for outpainting/smaller tasks)
- **LoRA:**
    - `LyNiaZ53Tudg0J6sT8Xbx_pytorch_lora_weights_comfy_converted.safetensors` (For 4B model, specifically Outpainting)
- **Text Encoder (CLIP):**
    - `qwen_3_8b_fp8mixed.safetensors` (For 9B model)
    - `qwen_3_4b.safetensors` (For 4B model, specifically Outpainting)
- **VAE:**
    - `flux2-vae.safetensors` (For image encoding/decoding)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching any workflow.

## Download Links and Path Details
| Type | Filename | Model page / direct download | Target folder |
| :--- | :--- | :--- | :--- |
| Diffusion model (9B) | `flux-2-klein-9b-fp8.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/tree/main) | `ComfyUI/models/diffusion_models/` |
| Diffusion model (4B) | `flux-2-klein-4b.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B/resolve/main/flux-2-klein-4b.safetensors) | `ComfyUI/models/diffusion_models/` |
| LoRA | `LyNiaZ53Tudg0J6sT8Xbx_pytorch_lora_weights_comfy_converted.safetensors` | [Hugging Face](https://huggingface.co/fal/flux-2-klein-4B-outpaint-lora/resolve/main/LyNiaZ53Tudg0J6sT8Xbx_pytorch_lora_weights_comfy_converted.safetensors?download=true) | `ComfyUI/models/loras/` |
| Text Encoder (9B) | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors) | `ComfyUI/models/text_encoders/` |
| Text Encoder (4B) | `qwen_3_4b.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-4b/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors) | `ComfyUI/models/text_encoders/` |
| VAE | `flux2-vae.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/flux2-vae.safetensors) | `ComfyUI/models/vae/` |

## Directory Structure
```text
ComfyUI/
├── models/
│   ├── diffusion_models/
│   │   ├── flux-2-klein-9b-fp8.safetensors
│   │   └── flux-2-klein-4b.safetensors
│   ├── loras/
│   │   └── LyNiaZ53Tudg0J6sT8Xbx_pytorch_lora_weights_comfy_converted.safetensors
│   ├── text_encoders/
│   │   ├── qwen_3_8b_fp8mixed.safetensors
│   │   └── qwen_3_4b.safetensors
│   └── vae/
│       └── flux2-vae.safetensors

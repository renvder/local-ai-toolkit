# Qwen Image Edit Inpaint Summary

## Workflows

1.  **[Qwen_Image_Edit_Inpaint.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Qwen_Image_Edit_Inpaint.json)**
    -   Requires `Qwen-Rapid-AIO-NSFW-v23.safetensors` (Checkpoint) and `Qwen-Image-Edit-F2P.safetensors` (LoRA).
    -   Uses specialized nodes `InpaintCrop|LP` and `InpaintStitch|LP` for context-aware inpainting, along with `TextEncodeQwenImageEditPlus` for prompt processing.
    -   Includes `PrimitiveStringMultiline` nodes for constructing separate landscape and document prompts.

## Models Required for All Workflows

To run the provided Qwen Image Inpaint workflow, the following models are required:
-   **`Qwen-Rapid-AIO-NSFW-v23.safetensors`**  (Checkpoint / Diffusion Model)
-   **`Qwen-Image-Edit-F2P.safetensors`**       (LoRA)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching the workflow.

## Download Links and Path Details

| Type | Filename | Model page / direct download | Target folder |
|---|---|---|---|
| Checkpoint | `Qwen-Rapid-AIO-NSFW-v23.safetensors` | [Hugging Face](https://huggingface.co/lllyasviel/Qwen-Image-Edit/resolve/main/Qwen-Rapid-AIO-NSFW-v23.safetensors) | `ComfyUI/models/checkpoints` |
| LoRA | `Qwen-Image-Edit-F2P.safetensors` | [Hugging Face](https://huggingface.co/lllyasviel/Qwen-Image-Edit/resolve/main/Qwen-Image-Edit-F2P.safetensors) | `ComfyUI/models/loras` |

## Directory Structure

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── Qwen-Rapid-AIO-NSFW-v23.safetensors
│   └── loras/
│       └── Qwen-Image-Edit-F2P.safetensors

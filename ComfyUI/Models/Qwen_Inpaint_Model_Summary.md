# Qwen Image Edit Inpaint Summary

## Workflows

-  **[Qwen_Image_Edit_Inpaint.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Qwen_Image_Edit_Inpaint.json)**
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
| Checkpoint | `Qwen-Rapid-AIO-NSFW-v23.safetensors` | [Hugging Face](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/resolve/main/v23/Qwen-Rapid-AIO-NSFW-v23.safetensors) / [Civitai](https://civitai-delivery-worker-prod.5ac0637cfd0766c97916cefa3764fbdf.r2.cloudflarestorage.com/model/9347248/qwenRapidAIONSFWV23.KD08.safetensors?X-Amz-Expires=86400&response-content-disposition=attachment%3B%20filename%3D%22phr00tQwenImageEditRapid_v230.safetensors%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=e01358d793ad6966166af8b3064953ad/20260810/us-east-1/s3/aws4_request&X-Amz-Date=20260810T021127Z&X-Amz-SignedHeaders=host&X-Amz-Signature=5cf7f7147c3a70732c9c79d5e6e44ce64661e5c199981a1e7261dde13e6124aa) | `ComfyUI/models/checkpoints` |
| LoRA | `Qwen-Image-Edit-F2P.safetensors` | [Hugging Face](https://huggingface.co/svjack/Qwen_Image/resolve/main/Qwen-Image-Edit-F2P.safetensors) / [Civitai](https://b2.civitai.com/file/civitai-modelfiles/model/5817430/qwenImageEditF2P.mKwr.safetensors?Authorization=3_20260810190244_c80917a3490d617455976491_6a29ac6503ce2dd20ed2ad8e583e53f94fb93b3b_004_20260810200244_0047_dnld&b2ContentDisposition=attachment%3B+filename%3D%22Qwen-Image-Edit-F2P.safetensors%22) | `ComfyUI/models/loras` |

## Directory Structure

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── Qwen-Rapid-AIO-NSFW-v23.safetensors
│   └── loras/
│       └── Qwen-Image-Edit-F2P.safetensors

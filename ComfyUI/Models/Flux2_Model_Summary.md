# Flux2 Models Summary

## Workflows

1.  **[Flux2_Prompt_Reverse_to_Image.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Prompt_Reverse_to_Image.json)**
    - Requires `qwen_3_8b_fp8mixed.safetensors` and uses an embedded `AILab_QwenVL` node to refine prompts.

2.  **[Flux2_Klein_Outpaint.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Klein_Outpaint.json)**
    - Requires all three models, plus the `layer_utility:ImageScaleByAspectRatioV2`, `color_match`, and `grow_mask_with_blur` nodes for outpainting specific functionality.

3.  **[Flux2_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Image_Edit.json)**
    - Requires all three models, plus a `primitive string multiline` node for constructing prompts from multiple parameters.

4.  **[Flux2_Dual_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Dual_Image_Edit.json)**
    - Requires all three models and two `layer_utility:FluxKontextImageScale` nodes to handle image scaling in the dual-editing context.

## Models Required for All Workflows

To run any of the four provided Flux2 workflows, the following models are required:
- **`flux-2-klein-9b-fp8.safetensors`**  (Unet)
- **`qwen_3_8b_fp8mixed.safetensors`**    (CLIP)
- **`flux2-vae.safetensors`**             (VAE)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching any workflow.

## Download Links and Path Details

| Type | Filename                | Model page / direct download                                     | Target folder                     |
|---|---|---|---|
| Diffusion model | `flux-2-klein-9b-fp8.safetensors` | [Civitai](https://civitai-delivery-worker-prod.5ac0637cfd0766c97916cefa3764fbdf.r2.cloudflarestorage.com/model/1761469/flux2Klein9bFp8.DCTJ.safetensors?X-Amz-Expires=86400&response-content-disposition=attachment%3B%20filename%3D%22flux2Klein9bFp8_fp8.safetensors%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=e01358d793ad6966166af8b3064953ad/20260810/us-east-1/s3/aws4_request&X-Amz-Date=20260810T034019Z&X-Amz-SignedHeaders=host&X-Amz-Signature=bb85f4055caffb6ba752df097099123b4bd869bb8e5ec0e113a83a5635034dff) | `ComfyUI/models/diffusion_models` |
| text_encoders    | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors)  | `ComfyUI/models/text_encoders`     |
| VAE               | `flux2-vae.safetensors`         | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/flux2-vae.safetensors)  | `ComfyUI/models/vae`           |

## Directory Structure

```text
ComfyUI/
├── models/
│   ├── diffusion_models/
│   │   └── flux-2-klein-9b-fp8.safetensors
│   ├── text_encoders/
│   │   └── qwen_3_8b_fp8mixed.safetensors
│   └── vae/
        └── flux2-vae.safetensors
```

# Flux2 Models Summary

## Models Required for All Workflows

The following models are required to run any of the four provided Flux2 workflows:
- **`flux-2-klein-9b-fp8.safetensors`**  (Unet)
- **`qwen_3_8b_fp8mixed.safetensors`**    (CLIP)
- **`flux2-vae.safetensors`**             (VAE)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching any workflow.

## Download Links and Path Details

| Model Name                      | File Type | GitHub Link                                                                     | Local Path                                       |
|---------------------------------|-----------|---------------------------------------------------------------------------------|--------------------------------------------------|
| `flux-2-klein-9b-fp8.safetensors`   | `.safetensors` | https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/models/flux-2-klein-9b-fp8.safetensors  | `ComfyUI/models/flux-2-klein-9b-fp8.safetensors`     |
| `qwen_3_8b_fp8mixed.safetensors`    | `.safetensors` | https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/models/qwen_3_8b_fp8mixed.safetensors  | `ComfyUI/models/qwen_3_8b_fp8mixed.safetensors`      |
| `flux2-vae.safetensors`             | `.safetensors` | https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/models/flux2-vae.safetensors          | `ComfyUI/models/flux2-vae.safetensors`              |

> **Note**: These models are loaded directly from the specified GitHub links for convenience, ensuring they're up-to-date. However, downloading them locally via git or direct download is also possible.

---

## Workflow-Specific Notes (Workflow-specific notes)

All workflows rely on the three shared models above, but they have specific additional requirements:

1.  **Flux2_Prompt_Reverse_to_Image.json**
    - Requires `qwen_3_8b_fp8mixed.safetensors` and uses an embedded `AILab_QwenVL` node to refine prompts.

2.  **Flux2_Klein_Outpaint.json**
    - Requires all three models, plus the `layer_utility:ImageScaleByAspectRatioV2`, `color_match`, and `grow_mask_with_blur` nodes for outpainting specific functionality.

3.  **Flux2_Image_Edit.json**
    - Requires all three models, plus a `primitive string multiline` node for constructing prompts from multiple parameters.

4.  **Flux2_Dual_Image_Edit.json**
    - Requires all three models and two `layer_utility:FluxKontextImageScale` nodes to handle image scaling in the dual-editing context.


## Model Download Verification Steps (下載模型驗證步驟)

To ensure successful execution of these workflows, follow these steps:
1. **Download models** from GitHub or other trusted sources.
2. **Place models in directory**:  Save them into `F:/Bing/Documents/GitHub/ComfyUI/models/`
3. **Restart ComfyUI server** and ensure it can find the newly placed models (if not automatically detected, restart the server).

This summary is based on analyzing the provided workflows as described.

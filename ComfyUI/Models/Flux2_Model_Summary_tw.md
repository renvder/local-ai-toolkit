# Flux2 模型摘要

## 工作流

1.  **[Flux2_Prompt_Reverse_to_Image.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Prompt_Reverse_to_Image.json)**
    - 需要 `qwen_3_8b_fp8mixed.safetensors` ，並使用嵌入式 `AILab_QwenVL` 節點來優化提示詞。

2.  **[Flux2_Klein_Outpaint.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Klein_Outpaint.json)**
    - 需要所有三個模型，加上用於外擴的特定功能節點 `layer_utility:ImageScaleByAspectRatioV2`, `color_match`, 和 `grow_mask_with_blur`。

3.  **[Flux2_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Image_Edit.json)**
    - 需要所有三個模型，再加上用來從多個參數構建提示詞的 `primitive string multiline` 節點。

4.  **[Flux2_Dual_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Dual_Image_Edit.json)**
    - 需要所有三個模型和兩個 `layer_utility:FluxKontextImageScale` 節點，用於處理雙圖編輯中的圖像縮放。

## 工作流需要的模型
要運行提供的任何四個Flux2工作流，需要以下模型:
- **`flux-2-klein-9b-fp8.safetensors`**  (Unet)
- **`qwen_3_8b_fp8mixed.safetensors`**    (CLIP)
- **`flux2-vae.safetensors`**             (VAE)
這些模型必須在啟動任何工作流之前下載並放置在 `ComfyUI/models/` 目錄中。

## 下載連結和路徑細節

| 類型 | 檔案名稱                | 模型頁面 / 直接下載                                     | 目標資料夾                     |
|---|---|---|---|
| Diffusion model | `flux-2-klein-9b-fp8.safetensors` | [Civitai](https://civitai-delivery-worker-prod.5ac0637cfd0766c97916cefa3764fbdf.r2.cloudflarestorage.com/model/1761469/flux2Klein9bFp8.DCTJ.safetensors?X-Amz-Expires=86400&response-content-disposition=attachment%3B%20filename%3D%22flux2Klein9bFp8_fp8.safetensors%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=e01358d793ad6966166af8b3064953ad/20260810/us-east-1/s3/aws4_request&X-Amz-Date=20260810T034019Z&X-Amz-SignedHeaders=host&X-Amz-Signature=bb85f4055caffb6ba752df097099123b4bd869bb8e5ec0e113a83a5635034dff) | `ComfyUI/models/diffusion_models` |
| text_encoders    | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors)  | `ComfyUI/models/text_encoders`     |
| VAE               | `flux2-vae.safetensors`         | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/flux2-vae.safetensors)  | `ComfyUI/models/vae`           |

## 目錄結構

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

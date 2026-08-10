# Flux2 模型摘要

## 所有工作流都需要的模型

要運行提供的任何四個Flux2工作流，需要以下模型:
- **`flux-2-klein-9b-fp8.safetensors`**  (Unet)
- **`qwen_3_8b_fp8mixed.safetensors`**    (CLIP)
- **`flux2-vae.safetensors`**             (VAE)

這些模型必須在啟動任何工作流之前下載並放置在 `ComfyUI/models/` 目錄中。

## 下載連結和路徑細節

| 模型名稱                      | 檔案類型  | GitHub 鏈接                                                                   | 局部路徑                                       |
|---------------------------------|-----------|---------------------------------------------------------------------------------|--------------------------------------------------|
| `flux-2-klein-9b-fp8.safetensors`   | `.safetensors` | https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/models/flux-2-klein-9b-fp8.safetensors  | `ComfyUI/models/flux-2-klein-9b-fp8.safetensors`     |
| `qwen_3_8b_fp8mixed.safetensors`    | `.safetensors` | https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/models/qwen_3_8b_fp8mixed.safetensors  | `ComfyUI/models/qwen_3_25b_fp8mixed.safetensors`      |
| `flux2-vae.safetensors`             | `.safetensors` | https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/models/flux2-vae.safetensors          | `ComfyUI/models/flux2-vae.safetensors`              |

> **注意**: 為了方便和確保模型是最新版，這些模型從指定的 GitHub 鏈接直接載入。不過，您也可以透過 git 或直接下載方式將它們保存到本地。

---

## 工作流特定說明 (Workflow-specific notes)

所有工作流都依賴上面的三個共享模型，但各有額外的特殊需求:

1.  **Flux2_Prompt_Reverse_to_Image.json**
    - 需要 `qwen_3_8b_fp8mixed.safetensors` ，並使用嵌入式 `AILab_QwenVL` 節點來優化提示詞。

2.  **Flux2_Klein_Outpaint.json**
    - 需要所有三個模型，加上用於外擴的特定功能節點 `layer_utility:ImageScaleByAspectRatioV2`, `color_match`, 和 `grow_mask_with_blur`。

3.  **Flux2_Image_Edit.json**
    - 需要所有三個模型，再加上用來從多個參數構建提示詞的 `primitive string multiline` 節點。

4.  **Flux2_Dual_Image_Edit.json**
    - 需要所有三個模型和兩個 `layer_utility:FluxKontextImageScale` 節點，用於處理雙圖編輯中的圖像縮放。

# Flux2 系列工作流模型摘要

## 工作流

1.  **[Flux2_Klein_4B_Outpaint.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Klein_4B_Outpaint.json)**
    - **功能：** 圖像外擴（Outpainting）。利用目標圖片和遮罩，將畫面內容自然地擴展到更大的畫布上。
    - **獨特需求：** 專門使用 4B 模型和專業的圖形處理功能，包括 `ImageScaleToTotalPixels` 和 `ImagePadKJ` 等用於尺寸和邊緣處理的節點。

2.  **[Flux2_Dual_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Dual_Image_Edit.json)**
    - **功能：** 允許用戶同時輸入兩張圖像（Image A 和 Image B），通過提示詞控制，實現精細的圖像修復或風格遷移。
    - **獨特需求：** 處理多個圖像輸入流（Image A 和 Image B），並將它們轉換為參考 latent 以進行 Flux 2 條件控制。

3.  **[Flux2_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Image_Edit.json)**
    - **功能：** 提示詞組合與圖像風格編輯。通過多個 `PrimitiveStringMultiline` 節點，將「觀點」「光照」「風格」等獨立的文本參數組合，生成單一且高複雜度的複合提示詞。
    - **獨特需求：** 強調複雜的文本提示詞構建能力。

4.  **[Flux2_Prompt_Reverse_to_Image.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Prompt_Reverse_to_Image.json)**
    - **功能：** 提示詞反向工程。利用輸入的圖像，通過 `AILab_QwenVL` 節點對用戶的提示詞進行優化和擴展，從而生成更豐富的圖像生成提示。
    - **獨特需求：** 整合了多模態大模型 (QwenVL) 節點進行提示詞優化。

## 工作流程需要的模型

本套 Flux2 工作流系列需要根據模型大小和用途（9B vs 4B）準備多個版本和組件。

- **Diffusion Model (Unet):**
    - `flux-2-klein-9b-fp8.safetensors` (9B 模型，用於複雜編輯，如Dual-Edit)
    - `flux-2-klein-4b.safetensors` (4B 模型，用於外擴/Outpainting)
- **Text Encoder (CLIP):**
    - `qwen_3_8b_fp8mixed.safetensors` (用於9B模型)
    - `qwen_3_4b.safetensors` (用於4B模型，特別是Outpainting)
- **VAE:**
    - `flux2-vae.safetensors` (用於編解碼圖像)

這些模型必須在啟動任何工作流之前下載並放置在 `ComfyUI/models/` 目錄中。

## 下載連結和路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
| :--- | :--- | :--- | :--- |
| Diffusion model (9B) | `flux-2-klein-9b-fp8.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/tree/main) | `ComfyUI/models/diffusion_models/flux2-klein-9b-fp8.safetensors` |
| Diffusion model (4B) | `flux-2-klein-4b.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B/resolve/main/flux-2-klein-4b.safetensors) | `ComfyUI/models/diffusion_models/flux-2-klein-4b.safetensors` |
| Text Encoder (9B) | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors) | `ComfyUI/models/text_encoders/qwen_3_8b_fp8mixed.safetensors` |
| Text Encoder (4B) | `qwen_3_4b.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-4b/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors) | `ComfyUI/models/text_encoders/qwen_3_4b.safetensors` |
| VAE | `flux2-vae.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/flux2-vae.safetensors) | `ComfyUI/models/vae/flux2-vae.safetensors` |

## 目錄結構

```text
ComfyUI/
├── models/
│   ├── diffusion_models/
│   │   ├── flux-2-klein-9b-fp8.safetensors
│   │   └── flux-2-klein-4b.safetensors
│   ├── text_encoders/
│   │   ├── qwen_3_8b_fp8mixed.safetensors
│   │   └── qwen_3_4b.safetensors
│   └── vae/
│       └── flux2-vae.safetensors

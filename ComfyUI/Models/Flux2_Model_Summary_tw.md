# Flux2 系列工作流模型摘要

## 工作流
1. **[Flux2_Klein_4B_Outpaint.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Klein_4B_Outpaint.json)**
   - **功能：** 影像外繪/畫布擴展。使用原始影像和遮罩（Mask）將場景內容自然地擴展到更大的畫布上。
   - **獨特需求：** 特別利用 4B 模型，並使用 `ImageScaleToTotalPixels` 和 `ImagePadKJ` 等專業圖形處理節點，進行進階的尺寸和邊緣處理。

2. **[Flux2_Dual_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Dual_Image_Edit.json)**
   - **功能：** 允許使用者同時輸入兩張影像（Image A 和 Image B），並透過文字提示（Prompt）進行細緻的影像修復或風格轉換。
   - **獨特需求：** 處理多個影像輸入流（Image A 和 Image B），並將它們轉換為用於 Flux 2 條件制式（Conditioning）的參考 Latents。

3. **[Flux2_Image_Edit.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Image_Edit.json)**
   - **功能：** 提示組合與風格編輯。使用多個 `PrimitiveStringMultiline` 節點組合分離的文字參數（如「透視」、「照明」和「風格」），生成單一、複雜且高度描述性的複合提示。
   - **獨特需求：** 專注於進階的文字提示構建能力。

4. **[Flux2_Prompt_Reverse_to_Image.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Flux2_Prompt_Reverse_to_Image.json)**
   - **功能：** 提示反向工程。使用帶有 `AILab_QwenVL` 節點的輸入影像，優化並擴充使用者提示，為影像生成產生更豐富的提示創意。
   - **獨特需求：** 整合多模態大型語言模型（QwenVL）節點來優化提示。

## 工作流程需要的模型
此 Flux2 工作流系列需要根據模型大小和特定任務（9B vs 4B）載入多個版本和組件。

- **Diffusion Model (Unet):**
    - `flux-2-klein-9b-fp8.safetensors` (9B 模型，適用於複雜編輯，例如雙圖編輯)
    - `flux-2-klein-4b.safetensors` (4B 模型，適用於外繪/較小任務)
- **LoRA:**
    - `LyNiaZ53Tudg0J6sT8Xbx_pytorch_lora_weights_comfy_converted.safetensors` (用於 4B 模型，特別是外繪功能)
- **Text Encoder (CLIP):**
    - `qwen_3_8b_fp8mixed.safetensors` (用於 9B 模型)
    - `qwen_3_4b.safetensors` (用於 4B 模型，特別是外繪)
- **VAE:**
    - `flux2-vae.safetensors` (用於影像編碼/解碼)

所有模型必須下載並放置在 `ComfyUI/models/` 目錄下，才能啟動任何工作流。

## 下載連結和路徑細節
| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
| :--- | :--- | :--- | :--- |
| Diffusion model (9B) | `flux-2-klein-9b-fp8.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/tree/main) | `ComfyUI/models/diffusion_models/` |
| Diffusion model (4B) | `flux-2-klein-4b.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B/resolve/main/flux-2-klein-4b.safetensors) | `ComfyUI/models/diffusion_models/` |
| LoRA | `LyNiaZ53Tudg0J6sT8Xbx_pytorch_lora_weights_comfy_converted.safetensors` | [Hugging Face](https://huggingface.co/fal/flux-2-klein-4B-outpaint-lora/resolve/main/LyNiaZ53Tudg0J6sT8Xbx_pytorch_lora_weights_comfy_converted.safetensors?download=true) | `ComfyUI/models/loras/` |
| Text Encoder (9B) | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors) | `ComfyUI/models/text_encoders/` |
| Text Encoder (4B) | `qwen_3_4b.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-4b/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors) | `ComfyUI/models/text_encoders/` |
| VAE | `flux2-vae.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/flux2-vae.safetensors) | `ComfyUI/models/vae/` |

## 目錄結構
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

# LTX 模型摘要

## 工作流

1.  **[LTX-2.3_F2V_First-Last.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/LTX-2.3_F2V_First-Last.json)**
    - 具備「首尾幀」邏輯，允許在提供的兩張特定圖像（起始與結束點）之間進行轉場。

2.  **[LTX-2.3_I2V_Simple.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/LTX-2.3_I2V_Simple.json)**
    - 標準的圖生影（I2V）流程，用於從單一來源圖像生成動態影像。

3.  **[LTX-2.3_I2V_Two-Stage_Upscale.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/LTX-2.3_I2V_Two-Stage_Upscale.json)**
    - 包含兩階段處理流程，在生成過程中加入專用的潛空間縮放器（Latent Upscaler）以提升解析度。

4.  **[LTX-2.3_IA2V_Simple.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/LTX-2.3_IA2V_Simple.json)**
    - 圖生影（Image-to-Video）流程，支援直接從一張圖像 + 音訊生成影片（包含音訊同步）。
    - 包含多階段處理（圖像預處理、潛空間生成、低解析度生成、高解析度生成、音訊處理、視訊合成），同時支援提示詞增強、LoRA 載入、潛空間上縮放及音訊剪輯。

## 工作流需要的模型
運行上述 LTX 系列工作流時，需要以下模型：
- **`ltx-2.3-22b-distilled-fp8.safetensors`** (Checkpoint / 主模型)
- **`LTX23_video_vae_bf16.safetensors`** (用於影片的 VAE)
- **`LTX23_audio_vae_bf16.safetensors`** (用於音訊的 VAE)
- **`gemma-3-12b-it-heretic-v2_fp8_e4m3fn.safetensors`** (文字編碼器 1)
- **`ltx-2.3_text_projection_bf16.safetensors`** (文字編碼器 2)
- **`ltx-2.3-spatial-upscaler-x2-1.1.safetensors`** (潛空間縮放模型，用於「二階段」工作流)
- **`ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors`** (蒸餾動態 LoRA)

這些模型必須在啟動任何工作流之前下載並放置在 `ComfyUI/models/` 目錄中。

## 下載連結與路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
|------|----------|----------|------------|
| Checkpoint | ltx-2.3-22b-distilled-fp8.safetensors | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3-fp8/resolve/main/ltx-2.3-22b-distilled-fp8.safetensors) | `ComfyUI/models/checkpoints` |
| VAE | LTX23_video_vae_bf16.safetensors | [Hugging Face](https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/vae/LTX23_video_vae_bf16.safetensors) | `ComfyUI/models/vae` |
| VAE | LTX23_audio_vae_bf16.safetensors | [Hugging Face](https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/vae/LTX23_audio_vae_bf16.safetensors) | `ComfyUI/models/vae` |
| Text Encoder | gemma-3-12b-it-heretic-v2_fp8_e4m3fn.safetensors | [Hugging Face](https://huggingface.co/DreamFast/gemma-3-12b-it-heretic-v2/resolve/main/comfyui/gemma-3-12b-it-heretic-v2_fp8_e4m3fn.safetensors) | `ComfyUI/models/text_encoders` |
| Text Encoder | ltx-2.3_text_projection_bf16.safetensors | [Hugging Face](https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/text_encoders/ltx-2.3_text_projection_bf16.safetensors) | `ComfyUI/models/text_encoders` |
| Latent Upscaler | ltx-2.3-spatial-upscaler-x2-1.1.safetensors | [Hugging Face](https://huggingface.co/Lightricks/LTX-2.3/resolve/main/ltx-2.3-spatial-upscaler-x2-1.1.safetensors) | `ComfyUI/models/latent_upscale_models` |
| LoRA | ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors | [Hugging Face](https://huggingface.co/Kijai/LTX2.3_comfy/resolve/main/loras/ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors) | `ComfyUI/models/text_encoders` |

## 目錄結構

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── ltx-2.3-22b-distilled-fp8.safetensors
│   ├── vae/
│   │   ├── LTX23_video_vae_bf16.safetensors
│   │   └── LTX23_audio_vae_bf16.safetensors
│   ├── text_encoders/
│   │   ├── gemma-3-12b-it-heretic-v2_fp8_e4m3fn.safetensors
│   │   └── ltx-2.3_text_projection_bf16.safetensors
│   ├── latent_upscale_models/
│   │   └── ltx-2.3-spatial-upscaler-x2-1.1.safetensors
│   └── loras/
│       └── ltx_2.3_22b_distilled_1.1_lora_dynamic_fro09_avg_rank_111_bf16.safetensors

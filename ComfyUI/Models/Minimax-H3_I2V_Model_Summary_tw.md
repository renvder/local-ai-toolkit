# MiniMax H3 跨模態圖像到視頻工作流摘要

## 工作流程

-  **[Minimax-H3_I2V_First-Last.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Minimax-H3_I2V_First-Last.json)**
    - **核心功能：** 圖像到視頻（I2V）生成。這是一個極致的跨模態工作流，它不只處理圖像，還將**聲音、視覺、文字**作為單一輸入進行結合生成。
    - **關鍵特色：**
        *   **跨媒體整合：** 能夠結合文字（Prompt）、第一幀圖像（First Frame）、和最後幀圖像（Last Frame）來生成一段具有連貫敘事和聲音背景的視頻。
        *   **原生立體聲：** 模型能夠原生生成包含人聲、音效（SFX）和音樂的聲音景觀，而非事後疊加。
        *   **運動控制：** 通過固定關鍵幀 (`first_frame` / `last_frame`)，精確控制視頻的運動和敘事轉變。
    - **主要節點：** `MiniMaxH3ImageToVideo` (核心生成)、`VAEDecodeAudio` (音訊解碼)、`CreateVideo` (合成視頻)。

## 工作流程需要的模型

本工作流程需要大量的專用模型，涵蓋了 UNET 結構、多模態 CLIP 編碼器、以及專門的音訊和視頻編解碼器。

- **Diffusion Model (Unet):**
    - `minimax_h3_fl2va_pruned_int8_convrot.safetensors` (核心 UNET 模型，用於I2V生成)
- **Text Encoder (CLIP):**
    - `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` (用於處理複雜的跨模態提示詞)
- **VAE (Video/Audio):**
    - `minimax_h3_video_vae_fp16.safetensors` (用於視頻編碼/解碼)
    - `minimax_h3_audio_vae_fp32.safetensors` (用於音訊編碼/解碼，確保音質)
- **LoRA (Style/Boost):**
    - `minimax_h3_turbo_4step_ema_ckpt500.safetensors` (用來提升生成品質和細節)

這些模型必須在啟動任何工作流之前下載並放置在 `ComfyUI/models/` 目錄中。

## 下載連結和路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
| :--- | :--- | :--- | :--- |
| diffusion models | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors) | `ComfyUI/models/diffusion_models/` |
| text encoders | `qwen3vl_32b_minimax_h3_int8_convrot.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors) | `ComfyUI/models/text_encoders/` |
| VAE (Video) | `minimax_h3_video_vae_fp16.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors) | `ComfyUI/models/vae/` |
| VAE (Audio) | `minimax_h3_audio_vae_fp32.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors) | `ComfyUI/models/vae/` |
| LoRA | `minimax_h3_turbo_4step_ema_ckpt500.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/minimax_h3_turbo_4step_ema_ckpt500.safetensors) | `ComfyUI/models/loras/` |

## 目錄結構

```text
ComfyUI/
└── models/
    ├── vae/
    │   ├── minimax_h3_video_vae_fp16.safetensors
    │   └── minimax_h3_audio_vae_fp32.safetensors
    ├── diffusion_models/
    │   └── minimax_h3_fl2va_pruned_int8_convrot.safetensors
    ├── text_encoders/
    │   └── qwen3vl_32b_minimax_h3_int8_convrot.safetensors
    └── loras/
        └── minimax_h3_turbo_4step_ema_ckpt500.safetensors

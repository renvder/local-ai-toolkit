# SeedVR 模型摘要

## 工作流

1.  **[SeedVR2.5+TTP_HQ_Upscale.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/SeedVR2.5%2BTTP_HQ_Upscale.json)**
    - 採用 TTP（分塊處理）技術進行進階高品質放大，支援大尺寸圖像增強以及針對影片內容的解析度恢復。

## 工作流需要的模型
運行 SeedVR 系列工作流時，需要以下模型：
- **`seedvr2_ema_7b_sharp_fp16.safetensors`** (通用標準版)
- **`seedvr2_ema_7b_fp16.safetensors`** (銳化增強版)
- **`ema_vae_fp16.safetensors`** (SeedVR 系列專用 VAE)

這些模型必須在啟動任何工作流之前下載並放置在 `ComfyUI/models/` 目錄中。

## 下載連結與路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
|---|---|---|---|
| Checkpoint | `seedvr2_ema_7b_sharp_fp16.safetensors` | [Hugging Face](https://huggingface.co/numz/SeedVR2_comfyUI/resolve/main/seedvr2_ema_7b_sharp_fp16.safetensors) | `ComfyUI/models/checkpoints` |
| Checkpoint | `seedvr2_ema_3b_fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/numz/SeedVR2_comfyUI/resolve/main/seedvr2_ema_3b_fp8_e4m3fn.safetensors) | `ComfyUI/models/checkpoints` |
| VAE | `ema_vae_fp16.safetensors` | [Hugging Face](https://huggingface.co/numz/SeedVR2_comfyUI/resolve/main/ema_vae_fp16.safetensors) | `ComfyUI/models/vae` |

## 目錄結構

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   ├── seedvr2_ema_7b_sharp_fp16.safetensors
│   │   └── seedvr2_ema_3b_fp8_e4m3fn.safetensors
│   └── vae/
│       └── ema_vae_fp16.safetensors

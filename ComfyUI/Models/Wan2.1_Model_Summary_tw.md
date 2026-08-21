# Wan 2.1 InfiniTetalk：單人音訊驅動影片 模型摘要

## 工作流

1.  **[Wan-2.1_InfiniTetalk_Single.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Wan-2.1_InfiniTetalk_Single.json)**
    - **核心功能：** 一體化地根據圖像（視覺）、文本（提示詞）和音訊（語音）生成連貫且具有無限敘事感的視頻。
    - **模態融合：** 流程涉及四个核心模態的深度整合：
        *   **Image Embedding (圖像特徵)：** 使用 `WanVideoClipVisionEncode` 提取图像的时空信息。
        *   **Text Embedding (文本特徵)：** 使用 `WanVideoTextEncode` 编码提示词，指导视频内容。
        *   **Audio Embedding (音訊特徵)：** 使用 `AudioSeparation` 和 `MultiTalkWav2VecEmbeds` 从原始音轨中分离并提取人声（Vocals）等关键音源。
        *   **Diffusion (核心生成)：** 利用 `WanVideoModelLoader` 和 `WanVideoSampler` 完成最终的视频生成和细节增强。
    - **高级控制：** 支持高级的视频参数控制，包括：
        *   **Image Resize：** 可以在输入前进行尺寸调整和放大（Upscale）。
        *   **音频裁剪：** 精确控制音频的起止时间（`AudioCrop`）。
        *   **模型和参数管理：** 流程内置了多套加载器和复杂的计算节点，管理着多个版本的模型和参数。

## 工作流程需要的模型

本工作流依赖于一系列用于多媒体编码和推理的专业模型。

- **WAN 核心模型:**
    - `Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors` (核心 UNET 结构，用于图像到视频的生成)
- **Text Encoder (CLIP/T5):**
    - `umt5-xxl-enc-fp8_e4m3fn.safetensors` (用于文本提示的编码)
    - `clip_vision_h.safetensors` (用于图像视觉特徵提取)
- **Audio Model:**
    - `TencentGameMate/chinese-wav2vec2-base` (用于音訊的波形编码器，实现音源分离)
- **VAE:**
    - `wan_2.1_vae.safetensors` (专用的视频/音訊 VAE 編碼器)

## 下載連結和路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
| :--- | :--- | :--- | :--- |
| UNet | `Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors` | [ComfyUI-WanVideoWrapper](placeholder-for-wan2-1-i2v-14b) | `ComfyUI/models/diffusion_models/` |
| Text Encoder | `umt5-xxl-enc-fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-Music-3/resolve/main/text_encoders/minimax_music3_text_encoder_pruned_int8_convrot.safetensors) | `ComfyUI/models/text_encoders/` |
| CLIP Vision | `clip_vision_h.safetensors` | [Placeholder](placeholder-for-clip-vision) | `ComfyUI/models/clip_vision/` |
| Audio Encoder | `TencentGameMate/chinese-wav2vec2-base` | [Placeholder](placeholder-for-wav2vec2) | `ComfyUI/models/wav2vec_models/` |
| VAE | `wan_2.1_vae.safetensors` | [Placeholder](placeholder-for-wan-vae) | `ComfyUI/models/vae/` |

## 目錄結構

```text
ComfyUI/
└── models/
    ├── audio_encoders/
    │   └── chinese-wav2vec2-base
    ├── clip_vision/
    │   └── clip_vision_h.safetensors
    ├── diffusion_models/
    │   └── Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors
    ├── text_encoders/
    │   └── umt5-xxl-enc-fp8_e4m3fn.safetensors
    └── vae/
        └── wan_2.1_vae.safetensors

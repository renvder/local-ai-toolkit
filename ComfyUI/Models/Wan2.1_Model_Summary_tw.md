# Wan 2.1 InfiniTetalk：單人音訊驅動影片 模型摘要

## 工作流

-  **[Wan-2.1_InfiniTetalk_Single.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Wan-2.1_InfiniTetalk_Single.json)**
    - **核心功能：** 一體化地根據圖像（視覺）、文本（提示詞）和音訊（語音）生成連貫且具有無限敘事感的視頻。
    - **模態融合：** 流程涉及四个核心模態的深度整合：
        *   **Image Embedding (圖像特徵)：** 使用 `WanVideoClipVisionEncode` 提取图像的时空信息。
        *   **Text Embedding (文本特徵)：** 使用 `WanVideoTextEncode` 编码提示词，指导视频内容。
        *   **Diffusion (核心生成)：** 利用 `WanVideoModelLoader` 和 `WanVideoSampler` 完成最终的视频生成和细节增强。
    - **高级控制：** 支持高级的视频参数控制，包括：
        *   **Image Resize：** 可以在输入前进行尺寸调整和放大（Upscale）。
        *   **音频裁剪：** 精确控制音频的起止时间（`AudioCrop`）。
        *   **模型和参数管理：** 流程内置了多套加载器和复杂的计算节点，管理着多个版本的模型和参数。

## 工作流程需要的模型

本工作流依赖于一系列用于多媒体编码和推理的专业模型。

- **WAN 核心模型:**
    - `Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors` (用于图像到视频的生成)
- **Text Encoder (CLIP/T5):**
    - `umt5-xxl-enc-fp8_e4m3fn.safetensors` (用于文本提示的编码)
    - `clip_vision_h.safetensors` (用于图像视觉特徵提取)
- **VAE:**
    - `wan_2.1_vae.safetensors` (专用的视频/音訊 VAE 編碼器)

## 下載連結和路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
| :--- | :--- | :--- | :--- |
| Diffusion Models | `Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors) | `ComfyUI/models/diffusion_models/` |
| Text Encoder | `umt5-xxl-enc-fp8_e4m3fn.safetensors` | [Hugging Face](https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors) | `ComfyUI/models/text_encoders/` |
| CLIP Vision | `clip_vision_h.safetensors` | [Hugging Face](https://huggingface.co/calcuis/wan-gguf/resolve/f52f5a1f0ba441d50277fb7cdd7c1b36611837f9/clip_vision_h.safetensors) | `ComfyUI/models/clip_vision/` |
| VAE | `wan_2.1_vae.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors) | `ComfyUI/models/vae/` |

## 目錄結構

```text
ComfyUI/
└── models/
    ├── clip_vision/
    │   └── clip_vision_h.safetensors
    ├── diffusion_models/
    │   └── Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors
    ├── text_encoders/
    │   └── umt5-xxl-enc-fp8_e4m3fn.safetensors
    └── vae/
        └── wan_2.1_vae.safetensors

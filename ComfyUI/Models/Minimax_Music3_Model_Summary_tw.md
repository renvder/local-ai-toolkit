# MiniMax Music 3：文本生成音訊 模型摘要

## 工作流

-  **[Minimax_Music3.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Minimax_Music3.json)**
    - **核心功能：** 根據複雜的文字提示詞（包含流派、情緒、歌詞、場景描述），生成高保真、結構化和原生的音樂音訊。
    - **关键特色：**
        *   **多層次提示词：** 提示词输入可以包含多个维度（如`Global Metadata`、`Vocal Details`、`Arrangement`），指导生成音乐的宏观结构和情感基调。
        *   **音频时空感知：** 能够理解并生成复杂的声景（Soundscape），如声效、人声和乐器之间的空间关系。
        *   **专业编解码：** 流程使用了专业的瓦片式（Tiled）和标准音频编解码器，确保了音质的稳定输出。
    - **流程组成：** 流程包含提示词编码 $\rightarrow$ 模型推理 $\rightarrow$ 潜在音訊編碼 $\rightarrow$ 瓦片式音訊解碼 $\rightarrow$ 音訊保存。

## 工作流程需要的模型

本音訊工作流需要專門的音訊模型，用於將高維度的文本信息轉換為可生成的音訊特徵。

- **CLIP Text Encoder:**
    - `minimax_music3_text_encoder_pruned_int8_convrot.safetensors` (將复杂的文本描述转换为音訊模型可理解的向量)
- **Diffusion Model:**
    - `minimax_music3_dit_fp16.safetensors` (核心 UNET 模型，專門用於音樂的生成)
- **VAE:**
    - `minimax_music3_dav.safetensors` (專用於音訊的編解碼器，確保音訊的時域和頻域完整性)

這些模型必須在啟動任何工作流之前下載並放置在 `ComfyUI/models/` 目錄中。

## 下載連結和路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
| :--- | :--- | :--- | :--- |
| Text Encoder | `minimax_music3_text_encoder_pruned_int8_convrot.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-Music-3/resolve/main/text_encoders/minimax_music3_text_encoder_pruned_int8_convrot.safetensors) | `ComfyUI/models/text_encoders/` |
| Diffusion Models | `minimax_music3_dit_fp16.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-Music-3/resolve/main/diffusion_models/minimax_music3_dit_fp16.safetensors) | `ComfyUI/models/diffusion_models/` |
| VAE | `minimax_music3_dav.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-Music-3/resolve/main/vae/minimax_music3_dav.safetensors) | `ComfyUI/models/vae/` |

## 目錄結構

```text
ComfyUI/
└── models/
    ├── diffusion_models/
    │   └── minimax_music3_dit_fp16.safetensors
    ├── text_encoders/
    │   └── minimax_music3_text_encoder_pruned_int8_convrot.safetensors
    └── vae/
        └── minimax_music3_dav.safetensors

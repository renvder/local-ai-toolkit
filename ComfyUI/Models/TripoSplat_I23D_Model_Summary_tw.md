# TripoSplat：2D 圖像到 3D 模型摘要

## 工作流程

-  **[TripoSplat_I23D.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/TripoSplat_I23D.json)**
    - **核心功能：** 將單張 2D 圖像提升為 3D 幾何結構（Gaussian Splat），實現從平面到空間的轉換。
    - **核心管線：** 流程高度模組化，可執行三種獨立的輸出：
        1.  **3D Gaussian Splat (.spz)：** 核心的稀疏點雲數據，用於重建點陣結構。
        2.  **3D Mesh (.glb)：** 透過點雲數據轉換為傳統的網格模型，適用於遊戲或渲染引擎。
        3.  **Orbit Preview Video：** 循環環繞拍攝的視頻預覽，用於在視圖器中驗證 3D 重建效果。
    - **关键前置步骤：** 流程包含複雜的背景移除（BiRefNet）和圖像掩碼操作，確保 3D 重建的準確性和純淨度。
    - **适用场景：** 最適合處理風格化、具有明確邊界或產品的靜物圖像。

## 工作流程需要的模型

本流程的模型組件分工極為明確，必須搭配使用各個模型才能完整運行。

- **Gaussian Splat UNet:**
    - `triposplat_fp16.safetensors` (用於 3D 點雲的分割和編碼核心模型)
- **Text Encoder (CLIP):**
    - `dino_v3_vit_h.safetensors` (用於提供圖像的視覺特徵向量)
- **VAE:**
    - `triposplat_vae_decoder_fp16.safetensors` (專用於點雲的 VAE 編解碼器)
    - `flux2-vae.safetensors` (作為備用或輔助的 VAE 編碼器)
- **Background Removal:**
    - `birefnet.safetensors` (用於從圖像中精確分離前景和背景，提供高品質掩碼)

## 下載連結和路徑細節

| 類型 | 檔案名稱 | 模型頁面 / 直接下載 | 目標資料夾 |
| :--- | :--- | :--- | :--- |
| UNet (Splat) | `triposplat_fp16.safetensors` | [VAST-AI/TripoSplat](https://huggingface.co/VAST-AI/TripoSplat) | `ComfyUI/models/diffusion_models/` |
| CLIP Vision | `dino_v3_vit_h.safetensors` | [VAST-AI/TripoSplat](https://huggingface.co/VAST-AI/TripoSplat) | `ComfyUI/models/clip_vision/` |
| VAE (Splat) | `triposplat_vae_decoder_fp16.safetensors` | [VAST-AI/TripoSplat](https://huggingface.co/VAST-AI/TripoSplat) | `ComfyUI/models/vae/` |
| VAE (Fallback) | `flux2-vae.safetensors` | [VAST-AI/TripoSplat](https://huggingface.co/VAST-AI/TripoSplat) | `ComfyUI/models/vae/` |
| Background Remover | `birefnet.safetensors` | [Comfy-Org/BiRefNet](https://huggingface.co/Comfy-Org/BiRefNet) | `ComfyUI/models/background_removal/` |

## 目錄結構

```text
ComfyUI/
└── models/
    ├── background_removal/
    │   └── birefnet.safetensors
    ├── clip_vision/
    │   └── dino_v3_vit_h.safetensors
    ├── diffusion_models/
    │   └── triposplat_fp16.safetensors
    └── vae/
        ├── triposplat_vae_decoder_fp16.safetensors
        └── flux2-vae.safetensors

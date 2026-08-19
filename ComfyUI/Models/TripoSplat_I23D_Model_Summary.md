# TripoSplat: 2D Image to 3D Gaussian Model Summary

## Workflows

1.  **[TripoSplat_I23D.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/TripoSplat_I23D.json)**
    - **Core Functionality:** Elevates a single 2D image into a 3D geometric structure (Gaussian Splat), achieving the transformation from a flat plane to space.
    - **Pipeline Structure:** The workflow is highly modular, supporting three distinct output types:
        1.  **3D Gaussian Splat (.spz):** The core sparse point cloud data for volumetric reconstruction.
        2.  **3D Mesh (.glb):** Converts the point cloud into a traditional mesh model, suitable for game engines or rendering pipelines.
        3.  **Orbit Preview Video：** A circular preview video, used to validate the 3D reconstruction effect in a viewer.
    - **Key Preprocessing:** The workflow includes complex background removal and masking operations, ensuring the accuracy and purity of the 3D reconstruction.
    - **Best Use Cases:** Optimal for stylized, product, or still-life images with distinct boundaries.

## Models Required for All Workflows

The components of this pipeline are highly specialized. Multiple models must be used together for complete operation.

- **Gaussian Splat UNet:**
    - `triposplat_fp16.safetensors` (Core model for segmentation and encoding the 3D point cloud)
- **Text Encoder (CLIP):**
    - `dino_v3_vit_h.safetensors` (Used to provide visual feature vectors for the image)
- **VAE:**
    - `triposplat_vae_decoder_fp16.safetensors` (VAE Decoder specialized for point cloud decoding)
    - `flux2-vae.safetensors` (Fallback/Auxiliary VAE Encoder)
- **Background Removal:**
    - `birefnet.safetensors` (Used for accurate foreground/background separation, providing a high-quality mask)

## Download Links and Path Details

| Type | Filename | Model page / direct download | Target folder |
| :--- | :--- | :--- | :--- |
| Diffusion Models | `triposplat_fp16.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/diffusion_models/triposplat_fp16.safetensors) | `ComfyUI/models/diffusion_models/` |
| CLIP Vision | `dino_v3_vit_h.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/clip_vision/dino_v3_vit_h.safetensors) | `ComfyUI/models/clip_vision/` |
| VAE (Splat) | `triposplat_vae_decoder_fp16.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/triposplat_vae_decoder_fp16.safetensors) | `ComfyUI/models/vae/` |
| VAE (Fallback) | `flux2-vae.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/flux2-vae.safetensors) | `ComfyUI/models/vae/` |
| Background Remover | `birefnet.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/background_removal/birefnet.safetensors) | `ComfyUI/models/background_removal/` |

## Directory Structure

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

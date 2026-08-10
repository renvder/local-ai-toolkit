# Flux2 Prompt Reverse to Image — Model Sources

| Type | Filename | Model page / direct download | Target folder | Notes |
|---|---|---|---|---|
| Checkpoint | `flux-2-klein-9b-fp8.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/tree/main) / [Civitai](https://civitai-delivery-worker-prod.5ac0637cfd0766c97916cefa3764fbdf.r2.cloudflarestorage.com/model/1761469/flux2Klein9bFp8.DCTJ.safetensors?X-Amz-Expires=86400&response-content-disposition=attachment%3B%20filename%3D%22flux2Klein9bFp8_fp8.safetensors%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=e01358d793ad6966166af8b3064953ad/20260810/us-east-1/s3/aws4_request&X-Amz-Date=20260810T034019Z&X-Amz-SignedHeaders=host&X-Amz-Signature=bb85f4055caffb6ba752df097099123b4bd869bb8e5ec0e113a83a5635034dff) | `ComfyUI/models/checkpoints` | Flux 2 Klein 9B FP8 |
| Text Encoder | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors) / [Civitai](https://...) | `ComfyUI/models/text_encoders` | Qwen3 CLIP mixed precision |
| VAE | `flux2-vae.safetensors` | [Hugging Face](https://huggingface.co/...) / [Civitai](https://...) | `ComfyUI/models/vae` | Flux 2 VAE |
| LoRA | `Qwen-Image-Edit-F2P.safetensors` | [Hugging Face](https://huggingface.co/svjack/Qwen_Image/resolve/main/Qwen-Image-Edit-F2P.safetensors) / [Civitai](https://b2.civitai.com/file/civitai-modelfiles/model/5817430/qwenImageEditF2P.mKwr.safetensors?Authorization=...) | `ComfyUI/models/loras` | Qwen Image Edit LoRA (Strength: 0.4) |

---

### 📂 Directory Structure

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── flux-2-klein-9b-fp8.safetensors
│   ├── clip/
│   │   └── qwen_3_8b_fp8mixed.safetensors
│   ├── vae/
│   │   └── flux2-vae.safetensors
│   └── loras/
│       └── Qwen-Image-Edit-F2P.safetensors
```

### ⚙️ Workflow Node Requirements
* **Custom Nodes:**
  * `rgthree-comfy` (Image Comparer (rgthree))
  * `comfyui-levelpixel` (InpaintCrop|LP, InpaintStitch|LP)
  * `ComfyUI_essentials` (MaskBlur+, MaskPreview+)
  * `ComfyUI_JPS-Nodes` (Text Concatenate (JPS))
  * `ComfyUI_LayerStyle` (LayerUtility: PurgeVRAM V2)

---

### 🧠 Model Specifications
* **Checkpoint**: Flux 2 Klein 9B FP8 — core diffusion model for image generation
* **Text Encoder**: Qwen3 CLIP mixed precision — text-to-image understanding
* **VAE**: Flux 2 VAE — latent space to image decoding
* **LoRA**: Qwen Image Edit F2P LoRA — fine-tuned editing capabilities with strength 0.4

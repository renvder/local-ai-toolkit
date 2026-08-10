# Flux2 Prompt Reverse to Image — Model Sources

| Type | Filename | Model page / direct download | Target folder | Notes |
|---|---|---|---|---|
| Checkpoint | `flux-2-klein-9b-fp8.safetensors` | [Hugging Face](https://huggingface.co/...) / [Civitai](https://...) | `ComfyUI/models/checkpoints` | Flux 2 Klein 9B FP8 |
| Text Encoder | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/...) / [Civitai](https://...) | `ComfyUI/models/text_encoders` | Qwen3 CLIP mixed precision |
| VAE | `flux2-vae.safetensors` | [Hugging Face](https://huggingface.co/...) / [Civitai](https://...) | `ComfyUI/models/vae` | Flux 2 VAE |
| LoRA | `Qwen-Image-Edit-F2P.safetensors` | [Hugging Face](https://huggingface.co/svjack/Qwen_Image/resolve/main/Qwen-Image-Edit-F2P.safetensors) / [Civitai](https://b2.civitai.com/file/civitai-modelfiles/model/5817430/qwenImageEditF2P.mKwr.safetensors?Authorization=...) | `ComfyUI/models/loras` | Qwen Image Edit LoRA (Strength: 0.4) |

---

### 📂 Directory Structure

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── flux-2-klein-9b-fp8.safetensors
│   ├── text_encoders/
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
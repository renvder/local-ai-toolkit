# Flux2 Dual Image Edit — Model Sources

| Type | Filename | Model page / direct download | Target folder | Notes |
|---|---|---|---|---|
| Diffusion model | `flux-2-klein-9b-fp8.safetensors` | [Hugging Face](https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/resolve/main/flux-2-klein-9b-fp8.safetensors) | `ComfyUI/models/diffusion_models` | FLUX.2 Klein 9B (FP8 Quantized) |
| Text encoder | `qwen_3_8b_fp8mixed.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors) | `ComfyUI/models/text_encoders` | Qwen3 8B Text Encoder (FP8 Mixed) |
| VAE | `flux2-vae.safetensors` | [Hugging Face](https://huggingface.co/VAST-AI/TripoSplat/resolve/main/vae/flux2-vae.safetensors) | `ComfyUI/models/vae` | FLUX.2 Native VAE |

---

### 📂 Directory Structure

```text
ComfyUI/
├── models/
│   ├── diffusion_models/
│   │   └── flux-2-klein-9b-fp8.safetensors
│   ├── text_encoders/
│   │   └── qwen_3_8b_fp8mixed.safetensors
│   └── vae/
│       └── flux2-vae.safetensors

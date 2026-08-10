# Qwen Image Edit Inpaint — Model Sources

| Type | Filename | Model page / direct download | Target folder | Notes |
|---|---|---|---|---|
| Checkpoint | `Qwen-Rapid-AIO-NSFW-v23.safetensors` | [Hugging Face](https://huggingface.co) / [Civitai](https://civitai.com) | `ComfyUI/models/checkpoints` | Qwen Rapid AIO Base Model |
| LoRA | `Qwen-Image-Edit-F2P.safetensors` | [Hugging Face](https://huggingface.co) / [Civitai](https://civitai.com) | `ComfyUI/models/loras` | Qwen Image Edit LoRA (Strength: 0.4) |

---

### 📂 Directory Structure

```text
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── Qwen-Rapid-AIO-NSFW-v23.safetensors
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

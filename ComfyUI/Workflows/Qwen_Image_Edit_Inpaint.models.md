# Qwen Image Edit Inpaint — Model Sources

| Type | Filename | Model page / direct download | Target folder | Notes |
|---|---|---|---|---|
| Checkpoint | `Qwen-Rapid-AIO-NSFW-v23.safetensors` | [Hugging Face](https://huggingface.co/Phr00t/Qwen-Image-Edit-Rapid-AIO/resolve/main/v23/Qwen-Rapid-AIO-NSFW-v23.safetensors) / [Civitai](https://civitai-delivery-worker-prod.5ac0637cfd0766c97916cefa3764fbdf.r2.cloudflarestorage.com/model/9347248/qwenRapidAIONSFWV23.KD08.safetensors?X-Amz-Expires=86400&response-content-disposition=attachment%3B%20filename%3D%22phr00tQwenImageEditRapid_v230.safetensors%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=e01358d793ad6966166af8b3064953ad/20260810/us-east-1/s3/aws4_request&X-Amz-Date=20260810T021127Z&X-Amz-SignedHeaders=host&X-Amz-Signature=5cf7f7147c3a70732c9c79d5e6e44ce64661e5c199981a1e7261dde13e6124aa) | `ComfyUI/models/checkpoints` | Qwen Rapid AIO Base Model |
| LoRA | `Qwen-Image-Edit-F2P.safetensors` | [Hugging Face](https://huggingface.co) / [Civitai](https://b2.civitai.com/file/civitai-modelfiles/model/5817430/qwenImageEditF2P.mKwr.safetensors?Authorization=3_20260810021643_6057db222ef2d6bb834d8c5c_7623308f500ae4f30dc65ad1c8a4ae6d9fd80c07_004_20260810031643_0047_dnld&b2ContentDisposition=attachment%3B+filename%3D%22Qwen-Image-Edit-F2P.safetensors%22) | `ComfyUI/models/loras` | Qwen Image Edit LoRA (Strength: 0.4) |

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

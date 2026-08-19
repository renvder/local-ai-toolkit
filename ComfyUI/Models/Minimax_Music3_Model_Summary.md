# MiniMax Music 3: Text-to-Audio Model Summary

## Workflows

-  **[Minimax_Music3.json](https://github.com/renvder/local-ai-toolkit/blob/main/ComfyUI/Workflows/Minimax_Music3.json)**
    - **Core Functionality:** Generates high-fidelity, structured, and native musical audio based on complex textual prompts (including genre, mood, lyrics, and scene descriptions).
    - **Key Features:**
        *   **Multi-Layered Prompting:** Prompts can input multiple dimensions (e.g., `Global Metadata`, `Vocal Details`, `Arrangement`), guiding the macro-structure and emotional tone of the generated music.
        *   **Acoustic Awareness:** The model can understand and generate complex soundscapes, including spatial relationships between sound effects, vocals, and instruments.
        *   **Professional Decoding:** The workflow utilizes specialized Tiled and standard audio decoders, ensuring stable and high-quality audio output.
    - **Process Steps:** The pipeline includes Prompt Encoding $\rightarrow$ Model Inference $\rightarrow$ Latent Audio Encoding $\rightarrow$ Tiled Audio Decoding $\rightarrow$ Audio Saving.

## Models Required for All Workflows

This audio workflow requires specialized audio models designed to translate high-dimensional text information into generatable audio features.

- **CLIP Text Encoder:**
    - `minimax_music3_text_encoder_pruned_int8_convrot.safetensors` (Converts complex text descriptions into vectors understandable by the audio model)
- **Diffusion Model (Unet):**
    - `minimax_music3_dit_fp16.safetensors` (The core UNET model specialized for music generation)
- **VAE:**
    - `minimax_music3_dav.safetensors` (Dedicated Audio VAE Decoder, ensuring temporal and frequency integrity of the audio)

These models must be downloaded and placed in the `ComfyUI/models/` directory before launching any workflow.

## Download Links and Path Details

| Type | Filename | Model page / direct download | Target folder |
| :--- | :--- | :--- | :--- |
| Text Encoder | `minimax_music3_text_encoder_pruned_int8_convrot.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-Music-3/resolve/main/text_encoders/minimax_music3_text_encoder_pruned_int8_convrot.safetensors) | `ComfyUI/models/text_encoders/` |
| Diffusion Models | `minimax_music3_dit_fp16.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-Music-3/resolve/main/diffusion_models/minimax_music3_dit_fp16.safetensors) | `ComfyUI/models/diffusion_models/` |
| VAE | `minimax_music3_dav.safetensors` | [Hugging Face](https://huggingface.co/Comfy-Org/MiniMax-Music-3/resolve/main/vae/minimax_music3_dav.safetensors) | `ComfyUI/models/vae/` |

## Directory Structure

```text
ComfyUI/
├── models/
│   ├── diffusion_models/
│   │   └── minimax_music3_dit_fp16.safetensors
│   ├── text_encoders/
│   │   └── minimax_music3_text_encoder_pruned_int8_convrot.safetensors
│   └── vae/
│       └── minimax_music3_dav.safetensors

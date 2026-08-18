# Why Vision Models Don't Work in llama-server Router Mode (and How to Fix It)

## The Problem

If you're running `llama-server` in **router mode** (started with `--models-dir`, which is what one-click launchers typically use for hot-swapping between models), a vision/multimodal GGUF model will silently fall back to **text-only** unless it's set up correctly. There's no error message — the server just won't accept images, and `/props` will report `"modalities": { "vision": false }` for that model.

This is **not a bug in the launcher script**. It's how llama-server's router mode is designed to discover multimodal projector files.

## Root Cause

A vision-capable model in llama.cpp is actually **two separate GGUF files**:

1. The main language model (e.g. `Qwen3-VL-8B-Q4_K_M.gguf`)
2. A multimodal projector, or **mmproj**, file that encodes images into embeddings (e.g. `mmproj-Qwen3-VL-8B-F16.gguf`)

In router mode, llama-server scans the `models` directory and pairs these two files together automatically — **but only if both conditions are met**:

- The model file and its mmproj file are placed **together in their own dedicated subfolder** (not loose in the root of `models`, and not mixed together with other models' files)
- The projector file's name **starts with `mmproj`**

If either condition isn't met, the mmproj file is either ignored or picked up as an unrelated, unusable "model" of its own — and the actual language model loads as text-only.

## Correct Directory Structure

```
models/
├─ Qwen3-14B-Instruct-Q4_K_M.gguf              ← plain text model: fine directly in the root
│
├─ Qwen3.8-27B/                                  ← vision model: needs its own folder
│  ├─ Qwen3.8-27B-Q4_K_M.gguf
│  └─ mmproj-Qwen3.8-27B-F16.gguf
│
└─ Qwen3-VL-8B/                                  ← another vision model, its own folder too
   ├─ Qwen3-VL-8B-Q4_K_M.gguf
   └─ mmproj-Qwen3-VL-8B-F16.gguf
```

## Common Mistakes

| Mistake | Result |
|---|---|
| Model `.gguf` and `mmproj-*.gguf` both dropped loose in `models/` root | Not paired — model loads text-only |
| Multiple models' mmproj files sharing one folder | Router pairs the mmproj with whichever model file it finds first — may attach to the wrong model |
| Projector file renamed to something that doesn't start with `mmproj` (e.g. `vision-encoder.gguf`) | Not recognized as a projector at all |
| Model and mmproj files in separate subfolders | No pairing across folders — router only looks *within* the same folder |

## How to Verify It Worked

1. Restart the server and watch the startup log for messages about custom presets / discovered models.
2. Once the model is loaded, check the router's `/props` (or `/props?model=<name>`) endpoint — look for:
   ```json
   "modalities": { "vision": true }
   ```
3. In the web UI, an image-upload / attachment icon should appear next to the chat input once a vision-capable model is selected. If it's missing, the pairing failed.

## Quick Checklist

- [ ] Each vision model has its **own subfolder** under `models/`
- [ ] The subfolder contains **exactly** the model file + its mmproj file (no other model's files mixed in)
- [ ] The projector filename **starts with `mmproj`**
- [ ] After restarting, `/props` shows `"vision": true` for that model

# AI Training

> **Phase**: 4 — Workflow (AI Profile)
> **Prerequisites**: [Inference (llama.cpp)](./inference.md), [GPU (NVIDIA)](../../phase-1-base-system/07-gpu-nvidia.md)
> **Packages**: TBD
> **Status**: 🚧 Planned — not yet implemented

---

## Overview

Fine-tune, train, and customize AI models locally using your GPU. This module will cover tools for LoRA/QLoRA fine-tuning, dataset preparation, and model evaluation.

> [!NOTE]
> This module is a **placeholder** for future content. The sections below outline the planned scope — actual install steps will be added when the tooling is finalized.

## Planned Scope

### Fine-Tuning Frameworks

| Tool | Description |
|------|-------------|
| [Unsloth](https://github.com/unslothai/unsloth) | Fast LoRA/QLoRA fine-tuning (2x faster, 60% less VRAM) |
| [Axolotl](https://github.com/axolotl-ai-cloud/axolotl) | Multi-method fine-tuning framework |
| [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | Web UI for fine-tuning 100+ LLMs |
| [torchtune](https://github.com/pytorch/torchtune) | PyTorch-native fine-tuning |

### Dataset Tools

| Tool | Description |
|------|-------------|
| [Argilla](https://github.com/argilla-io/argilla) | Data labeling and curation |
| [distilabel](https://github.com/argilla-io/distilabel) | Synthetic dataset generation |

### Evaluation

| Tool | Description |
|------|-------------|
| [lm-eval-harness](https://github.com/EleutherAI/lm-evaluation-harness) | Standardized LLM benchmarks |
| [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) | Benchmark comparison |

### Model Conversion & Export

| Tool | Description |
|------|-------------|
| `llama-quantize` | Convert models to GGUF quantization formats (already installed with llama.cpp) |
| [GGUF conversion scripts](https://github.com/ggml-org/llama.cpp/tree/master/convert) | Convert HF models to GGUF |

## Prerequisites (When Ready)

These packages will likely be needed:
```bash
# Python ML stack
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers datasets accelerate peft bitsandbytes
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CUDA out of memory during training | Use QLoRA (4-bit), reduce batch size, or use gradient checkpointing |
| `bitsandbytes` errors | Ensure CUDA toolkit version matches PyTorch CUDA version |
| Slow training | Verify GPU is being used: `nvidia-smi` should show python process |

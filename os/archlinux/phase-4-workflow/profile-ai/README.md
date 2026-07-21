# AI Profile

> Full local AI stack — inference, coding harnesses, IDE integration, autonomous agents, and training.

## Modules

| # | Module | Required | Depends On | Notes |
|---|--------|----------|------------|-------|
| 1 | [Inference (llama.cpp)](./inference.md) | ⚡ Recommended | NVIDIA + AUR | llama-server, CUDA, OpenAI-compatible API |
| 2 | [AI Harness Tools](./harness.md) | ⚡ Recommended | Inference | Pi Agent, Kilo Code, OpenCode, Claude Code, Gemini CLI |
| 3 | [IDE Integration](./ide-integration.md) | ⚡ Recommended | Inference | AI plugins for Neovim, VS Code, Antigravity |
| 4 | [Autonomous Agents](./agents.md) | 💡 Optional | Inference | Hermes, Claude Desktop |
| 5 | [Training](./training.md) | 💡 Optional | Inference + NVIDIA | Fine-tuning, LoRA, datasets (future) |

> [!TIP]
> Start with **Inference** to get a local AI backend running, then layer on harness tools, IDE plugins, and agents as needed. Everything in this profile talks to the same local (or remote) model endpoints.

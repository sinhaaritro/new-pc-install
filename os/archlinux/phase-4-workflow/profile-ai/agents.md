# Autonomous Agents

> **Phase**: 4 — Workflow (AI Profile)
> **Prerequisites**: [Inference (llama.cpp)](./inference.md) or external API key
> **Packages**: varies per agent (see below)

---

## Overview

Autonomous AI agents run multi-step tasks with minimal human intervention — they can plan, execute commands, browse the web, write code, and self-correct. This module covers setting up agent frameworks and desktop apps that go beyond single-turn chat.

> [!NOTE]
> Some agents run local models (via your llama-server), some require external API keys, and some support both. Each section notes the requirements.

## Reference

- [Hermes (NousResearch)](https://nousresearch.com/) — Function-calling fine-tuned models
- [Claude Desktop (Anthropic)](https://claude.ai/download) — Desktop app with MCP tool use
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) — Open protocol for tool use

---

## Hermes

NousResearch's **Hermes** series are fine-tuned models optimized for function calling, structured output, and agentic behavior. They run on your local llama-server.

### Download a Hermes Model

```bash
# Download a Hermes GGUF (check HuggingFace for latest)
cd ~/models
wget "https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF/resolve/main/Hermes-3-Llama-3.1-8B.Q4_K_M.gguf"
```

### Run with llama-server

```bash
llama-server \
  -m ~/models/Hermes-3-Llama-3.1-8B.Q4_K_M.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 99
```

> [!TIP]
> Hermes models support the **tool/function calling** format natively. Any harness tool (OpenCode, Claude Code, etc.) that uses OpenAI-compatible function calling will benefit from Hermes over a base model.

### Systemd Service (Optional)

Create a separate service or modify your existing `llama-server.service` to swap the model path:

```bash
# Quick-swap alias
alias llama-hermes='llama-server -m ~/models/Hermes-3-Llama-3.1-8B.Q4_K_M.gguf --host 0.0.0.0 --port 8080 -ngl 99'
```

---

## Claude Desktop

Claude Desktop is Anthropic's native desktop application with **MCP (Model Context Protocol)** support — enabling Claude to use local tools, read files, query databases, and interact with your system.

### Install

```bash
# Check AUR for Claude Desktop package
yay -S claude-desktop
# Or download the .deb/.AppImage from https://claude.ai/download and convert
```

> [!NOTE]
> Claude Desktop on Linux may require an AppImage or manual install. Check the [official download page](https://claude.ai/download) for the latest Linux support status.

### MCP Configuration

Claude Desktop uses MCP servers to extend its capabilities. Configure in `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/username/projects"]
    }
  }
}
```

This gives Claude Desktop access to read/write files in your projects directory.

> [!WARNING]
> MCP servers grant Claude tool access to your system. Only configure servers you trust, and limit filesystem access to specific directories.

### Additional MCP Servers

| Server | Purpose | Install |
|--------|---------|---------|
| `server-filesystem` | File read/write | `npx @modelcontextprotocol/server-filesystem` |
| `server-github` | GitHub API access | `npx @modelcontextprotocol/server-github` |
| `server-sqlite` | SQLite queries | `npx @modelcontextprotocol/server-sqlite` |
| `server-brave-search` | Web search | `npx @modelcontextprotocol/server-brave-search` |

See the [MCP server registry](https://github.com/modelcontextprotocol/servers) for the full list.

---

## Verification

```bash
# Verify Hermes model is downloaded
ls -lh ~/models/Hermes-*.gguf

# Test Hermes with function calling
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "hermes",
    "messages": [{"role": "user", "content": "What time is it?"}],
    "tools": [{"type": "function", "function": {"name": "get_time", "description": "Get current time"}}]
  }'

# Verify Claude Desktop is installed
which claude-desktop 2>/dev/null || echo "Claude Desktop not found (may be AppImage)"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hermes model OOM | Use a smaller quant (Q3_K_M) or model (7B instead of 8B) |
| Function calling not working | Ensure you're using a Hermes/function-calling model, not a base model |
| Claude Desktop won't launch | Check Wayland compatibility, try with `--ozone-platform=wayland` flag |
| MCP server errors | Verify `npx` is available (Node.js installed), check server logs |

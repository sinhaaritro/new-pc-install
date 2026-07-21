# AI Harness Tools

> **Phase**: 4 — Workflow (AI Profile)
> **Prerequisites**: [Inference (llama.cpp)](./inference.md) or external API key
> **Packages**: varies per tool (see below)

---

## Overview

AI harness tools are **CLI-based coding assistants** that connect to a local or remote AI backend and give you agentic coding capabilities directly in your terminal. They can read files, propose edits, run commands, and iterate on codebases — all from the shell.

This module covers installing and configuring each tool to work with your local llama-server (from the [Inference](./inference.md) module) or with external APIs (Anthropic, Google, OpenAI).

> [!NOTE]
> Most of these tools support the OpenAI-compatible API format, which means they work out of the box with your local `llama-server` endpoint (`http://127.0.0.1:8080/v1`).

## Reference

- [Pi Agent (GitHub)](https://github.com/pi-agi/pi-agent)
- [Kilo Code (GitHub)](https://github.com/kilocode/kilocode)
- [OpenCode (GitHub)](https://github.com/opencode-ai/opencode)
- [Claude Code (Anthropic)](https://docs.anthropic.com/en/docs/claude-code)
- [Gemini CLI (Google)](https://github.com/google-gemini/gemini-cli)

---

## Pi Agent [PLANNED]

Pi Agent is an autonomous AI agent with a CLI interface.

```bash
# TODO: Add install instructions once package source is confirmed
# Check AUR or pip/npm for latest install method
```

Configure the API endpoint:
```bash
# Point to local llama-server
export PI_AGENT_API_BASE="http://127.0.0.1:8080/v1"
```

> [!NOTE]
> Verify the exact package name and install method — Pi Agent packaging may change. Check the [official repo](https://github.com/pi-agi/pi-agent) for current instructions.

---

## Kilo Code [PLANNED]

Kilo Code is an open-source AI coding assistant.

```bash
# Install via npm (check for latest method)
npm install -g kilocode
```

Configure for local inference:
```bash
# Point to local llama-server
export KILOCODE_API_BASE="http://127.0.0.1:8080/v1"
export KILOCODE_MODEL="local"
```

---

## OpenCode

OpenCode is a terminal-based AI coding tool.

### Install

```bash
# Install via official script
curl -fsSL https://opencode.ai/install | bash

# Or install via Arch Linux package / AUR
sudo pacman -S opencode
# Or via AUR helper: yay -S opencode
```

### Configure

Create `opencode.json` at the project base (or global config directory):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "llamacpp": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "llama.cpp Local Server",
      "options": {
        "baseURL": "http://localhost:8080/v1",
        "headers": {
          "Authorization": "Bearer not-needed"
        }
      },
      "models": {
        "unsloth/gemma-4-12b-it-GGUF": {
          "name": "Gemma 4 12B"
        },
        "HauhauCS/Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive": {
          "name": "Qwen 3.6 35B Aggressive"
        },
        "deepreinforce-ai/Ornith-1.0-35B-GGUF": {
          "name": "Ornith 1.0 35B"
        },
        "deepreinforce-ai/Ornith-1.0-9B-GGUF": {
          "name": "Ornith 1.0 9B"
        }
      }
    }
  },
  "agent": {
    "plan": {
      "model": "llamacpp/deepreinforce-ai/Ornith-1.0-35B-GGUF",
      "description": "Planning agent running on Ornith 35B"
    },
    "build": {
      "model": "llamacpp/deepreinforce-ai/Ornith-1.0-9B-GGUF",
      "description": "Execution agent running on Ornith 9B"
    }
  },
  "default_agent": "plan",
  "lsp": true
}
```

---

## Claude Code [PLANNED]

Claude Code is Anthropic's agentic CLI tool. Requires an Anthropic API key (does not support local OpenAI-compatible endpoints natively).

```bash
# Install via npm
npm install -g @anthropic-ai/claude-code
```

Configure:
```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

> [!IMPORTANT]
> Claude Code requires an **Anthropic API key** — it does not connect to local llama-server. Use it alongside your local stack for tasks that benefit from Claude's capabilities.

---

## Gemini CLI [PLANNED]

Google's official Gemini CLI for terminal-based AI interaction.

```bash
# Install via npm
npm install -g @anthropic-ai/gemini-cli
# Or check Google's official install docs for the latest method
```

Configure:
```bash
# Authenticate with Google
gemini auth login
```

> [!IMPORTANT]
> Gemini CLI uses **Google's API** — it does not connect to local llama-server. Requires a Google account with Gemini API access.

---

## Shell Integration

Add to `~/.config/zsh/aliases.zsh`:

```bash
# Harness tool aliases
alias oc='opencode'
alias cc='claude'
alias gc='gemini'
```

## Verification

```bash
# Verify each tool is installed
pi-agent --version 2>/dev/null && echo "✓ Pi Agent" || echo "✗ Pi Agent"
kilocode --version 2>/dev/null && echo "✓ Kilo Code" || echo "✗ Kilo Code"
opencode --version 2>/dev/null && echo "✓ OpenCode" || echo "✗ OpenCode"
claude --version 2>/dev/null && echo "✓ Claude Code" || echo "✗ Claude Code"
gemini --version 2>/dev/null && echo "✓ Gemini CLI" || echo "✗ Gemini CLI"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tool can't connect to local API | Verify `llama-server` is running: `curl http://127.0.0.1:8080/v1/models` |
| `npm: command not found` | Install Node.js first — see [Language Runtimes](../profile-dev/languages.md) |
| `go: command not found` | Install Go first — see [Language Runtimes](../profile-dev/languages.md) |
| API key errors (Claude/Gemini) | These tools require external API keys, not local inference |

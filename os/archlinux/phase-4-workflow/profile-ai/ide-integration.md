# IDE Integration

> **Phase**: 4 — Workflow (AI Profile)
> **Prerequisites**: [Inference (llama.cpp)](./inference.md) or external API key, target IDE installed
> **Packages**: varies per IDE (see below)

---

## Overview

Connect your local AI backend (or external APIs) directly into your editor for inline completions, chat, code actions, and agentic workflows. This module covers AI plugin setup for each IDE in the stack.

> [!NOTE]
> All plugins that support the OpenAI-compatible API can point to your local `llama-server` at `http://127.0.0.1:8080/v1`. External-only tools (Copilot, Antigravity) require their own authentication.

## Reference

- [avante.nvim](https://github.com/yetone/avante.nvim) — Cursor-like AI in Neovim
- [codecompanion.nvim](https://github.com/olimorris/codecompanion.nvim) — AI chat + actions for Neovim
- [copilot.lua](https://github.com/zbirenbaum/copilot.lua) — GitHub Copilot in Neovim
- [Continue (VS Code)](https://continue.dev/) — Open-source AI assistant extension
- [Cline (VS Code)](https://github.com/cline/cline) — Agentic AI extension
- [Antigravity IDE](https://deepmind.google/) — Google DeepMind's Gemini-powered IDE agent

---

## Neovim [PLANNED]

AI plugins for Neovim integrate via the built-in LSP client or as standalone Lua plugins.

### avante.nvim (Recommended)

Cursor-like AI experience in Neovim — inline chat, code generation, and diff-based edits.

Add to your plugin manager (e.g., lazy.nvim):
```lua
{
  "yetone/avante.nvim",
  event = "VeryLazy",
  opts = {
    provider = "openai-compatible",
    openai = {
      endpoint = "http://127.0.0.1:8080/v1",
      model = "local",
      api_key = "not-needed",  -- llama-server doesn't require a key
    },
  },
}
```

### codecompanion.nvim

Multi-provider AI chat and code actions:
```lua
{
  "olimorris/codecompanion.nvim",
  opts = {
    strategies = {
      chat = { adapter = "openai_compatible" },
      inline = { adapter = "openai_compatible" },
    },
    adapters = {
      openai_compatible = function()
        return require("codecompanion.adapters").extend("openai_compatible", {
          env = {
            url = "http://127.0.0.1:8080",
            api_key = "not-needed",
          },
          schema = {
            model = { default = "local" },
          },
        })
      end,
    },
  },
}
```

### copilot.lua (External)

GitHub Copilot — requires a **GitHub Copilot subscription**:
```lua
{
  "zbirenbaum/copilot.lua",
  cmd = "Copilot",
  event = "InsertEnter",
  opts = {
    suggestion = { enabled = true, auto_trigger = true },
    panel = { enabled = true },
  },
}
```

> [!NOTE]
> Copilot uses GitHub's cloud API — it does not connect to local inference. Use alongside your local stack.

---

## VSCodium (Codium)

VSCodium (`codium`) is the telemetry-free binary release of VS Code used in this setup.

### Continue

Open-source AI assistant extension, used primarily for **autocomplete** (powered by a low-end model) with optional primary chat/edit support.

#### 1. Schema Validation (Codium User Settings)

Add the YAML schema definition to your VSCodium user settings (`~/.config/VSCodium/User/settings.json`):

```json
"yaml.schemas": {
    "file:///home/aritro/.vscode-oss/extensions/continue.continue-2.0.0-linux-x64/config-yaml-schema.json": [
        ".continue/**/*.yaml"
    ]
}
```

#### 2. Continue Configuration (`~/.continue/config.yaml`)

Set up `~/.continue/config.yaml`:

```yaml
name: Main Config
version: 1.0.0
schema: v1
models:
  # 1. Primary Chat / Edit (Ornith 9B on Port 8080) (Optional, can use the main harness to do things)
  - name: "Ornith 1.0 9B"
    provider: "openai"
    model: "deepreinforce-ai/Ornith-1.0-9B-GGUF"
    apiBase: "http://127.0.0.1:8080/v1"
    roles:
      - chat
      - edit
      - apply

  # 2. Autocomplete (Gemma 4 E2B on Port 8080)
  - name: "Gemma 4 E2B Base"
    provider: "openai"
    model: "ggml-org/gemma-4-E2B-GGUF" # Matches the preset name in config.ini exactly
    apiBase: "http://127.0.0.1:8080/v1"
    roles:
      - autocomplete
    autocompleteOptions:
      debounceDelay: 150
      maxPromptTokens: 512
      modelTimeout: 1500
    promptTemplates:
      autocomplete: |
        <|fim_prefix|>{{{prefix}}}<|fim_suffix|>{{{suffix}}}<|fim_middle|>
```

### Cline [PLANNED]

Agentic AI extension with file editing, terminal commands, and browser control:

1. Install from Open VSX / marketplace: search **"Cline"**
2. Configure API provider in Cline settings:
   - Provider: **OpenAI Compatible**
   - Base URL: `http://127.0.0.1:8080/v1`
   - Model: `local`

### Kilo Code (Extension) [PLANNED]

Kilo Code also has a VSCodium extension in addition to its CLI:

1. Install from marketplace: search **"Kilo Code"**
2. Configure to point to local inference endpoint.

---

## Antigravity [PLANNED]

Antigravity is Google DeepMind's Gemini-powered IDE agent. It runs as a standalone IDE or as an extension.

> [!NOTE]
> Antigravity uses **Google's Gemini API** natively — it does not connect to local llama-server. It is included here as part of the full AI-assisted development stack.

Setup:
1. Install Antigravity IDE (check [official distribution](https://deepmind.google/) for latest install method)
2. Sign in with your Google account
3. The agent is ready — it has built-in tool use, file editing, terminal access, and browser control

---

## Verification

```bash
# Neovim: check plugins loaded
nvim --headless -c "lua print(vim.inspect(require('lazy').plugins()))" -c "qa" 2>&1 | grep -i avante

# VSCodium: list installed extensions
codium --list-extensions | grep -iE "continue|cline|kilo"

# Verify local endpoint is accessible from all tools
curl -s http://127.0.0.1:8080/v1/models | python -m json.tool
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plugin can't connect to local API | Verify `llama-server` is running on port 8080 |
| Neovim plugin not loading | Check lazy.nvim sync: `:Lazy sync` |
| VS Code extension not finding provider | Verify `apiBase` URL includes `/v1` path |
| Copilot / Antigravity not working | These require external accounts (GitHub / Google) |
| Slow completions from local model | Try a smaller model or increase `-ngl` layers |

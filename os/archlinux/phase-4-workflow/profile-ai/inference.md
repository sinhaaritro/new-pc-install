# Local Inference (llama.cpp)

> **Phase**: 4 — Workflow (AI Profile)
> **Prerequisites**: [NVIDIA Drivers](../../phase-2-system-hardening/nvidia-drivers.md), [AUR Helper](../../phase-2-system-hardening/aur-helper.md)
> **Packages**: `cuda llama-cpp-cuda` (AUR)

---

## Overview

Run local AI models natively on your GPU using **llama.cpp** — managed cleanly via a single master configuration file (`~/models/config.ini`). A unified `llama-server` process loads all defined model classes (Autocomplete, Fast Developer, Uncensored Heavy Lifter, Reasoning), automatically switching models on demand while keeping VRAM usage strictly bounded.

The `config.ini` file acts as the **single source of truth** for all models, upstream HuggingFace repository sources, remote/local file names, vision projectors (`mmproj`), draft models (`model-draft`), context limits, and sampling parameters.

---

## Reference

- [Arch Wiki: llama.cpp](https://wiki.archlinux.org/title/Llama.cpp)
- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [llama-server Preset & Server Documentation](https://github.com/ggml-org/llama.cpp/blob/master/examples/server/README.md)

---

## Steps

### Step 1: Install CUDA Toolkit

The CUDA toolkit is required for GPU-accelerated inference:

```bash
sudo pacman -S cuda
```

Verify the installation:
```bash
nvcc --version
nvidia-smi
```

> [!IMPORTANT]
> If `nvidia-smi` does not show your GPU, complete the [NVIDIA Drivers](../../phase-2-system-hardening/nvidia-drivers.md) module first.

### Step 2: Install llama.cpp (CUDA Build)

Install the AUR package compiled with CUDA support:

```bash
yay -S llama-cpp-cuda
```

This provides the following binaries:

| Binary | Purpose |
|--------|---------|
| `llama-server` | HTTP server with OpenAI-compatible API and built-in web UI |
| `llama-cli` | Interactive CLI chat for quick testing |
| `llama-quantize` | Convert/quantize models to different GGUF formats |

Verify the install:
```bash
llama-server --version
```

### Step 3: Create Model Directory

Create the main directory where all models, vision projectors, draft models, and configuration files will reside:

```bash
mkdir -p ~/models
```

### Step 4: Create Master Configuration File (`~/models/config.ini`)

Create `~/models/config.ini`. This configuration defines global defaults under `[*]` and registers each model class along with its HuggingFace source metadata, local file paths, speculative decoding draft models, vision projectors, and sampling parameters.

> [!NOTE]
> The model classes and configurations in `config.ini` below are reference examples demonstrating autocomplete, generalist, multimodal vision, and speculative decoding draft setups. Customize or swap model sections as needed for your specific workflow.

```ini
# Command:
# llama-server   --models-preset /home/aritro/models/config.ini   --fit off   --models-max 1   --host 0.0.0.0   --port 8080

[*]
# Global configurations inherited by all model classes
host = 0.0.0.0
port = 8080
ctx-size = 32768
flash-attn = true
cache-type-k = q4_0
cache-type-v = q4_0
stop-timeout = 600

# ==========================================
# Class 4: Ultra Fast Autocomplete 
# ==========================================
[ggml-org/gemma-4-E2B-GGUF]
# Base Model Source: https://huggingface.co/ggml-org/gemma-4-E2B-GGUF
# Base Model Remote Name: gemma-4-E2B-Q8_0.gguf
# Base Model Local Name: /home/aritro/models/gemma-4-E2B-Q8_0.gguf
model = /home/aritro/models/gemma-4-E2B-Q8_0.gguf

ngl = 99
ctx-size = 32768

# Autocomplete-specific sampling parameters
temp = 0.0
top-p = 0.95
min-p = 0.05
repeat-penalty = 1.0


# ==========================================
# Class 1: Uncensored Heavy Lifter Planner
# ==========================================
[deepreinforce-ai/Ornith-1.0-35B-GGUF]
# Base Model Source: https://huggingface.co/deepreinforce-ai/Ornith-1.0-35B-GGUF
# Base Model Remote Name: ornith-1.0-35b-Q6_K.gguf
# Base Model Local Name: /home/aritro/models/ornith-1.0-35b-Q6_K.gguf
model = /home/aritro/models/ornith-1.0-35b-Q6_K.gguf

# Vision Projector Source: https://huggingface.co/SC117/Ornith-1.0-35B-MTP-APEX-GGUF
# Vision Projector Remote Name: mmproj-F16.gguf
# Vision Projector Local Name: /home/aritro/models/ornith-1.0-35b-mmproj-F16.gguf
mmproj = /home/aritro/models/ornith-1.0-35b-mmproj-F16.gguf

# Draft Model Source: https://huggingface.co/williamliao/Qwen3.6-35B-A3B-DFlash-GGUF
# Draft Model Remote Name: Qwen3.6-35B-A3B-DFlash-Q4_K_M.gguf
# Draft Model Local Name: /home/aritro/models/ornith-1.0-35b-dflash-Q4_K_M.gguf
# Note: This file is a local copy of Qwen3.6-35B-A3B-Uncensored-HauhauCS-Aggressive-dflash-Q4_K_M.gguf to provide post-merge 'dflash' compatibility
model-draft = /home/aritro/models/ornith-1.0-35b-dflash-Q4_K_M.gguf

spec-type = draft-dflash
spec-draft-n-max = 4

ngl = 8
ctx-size = 100000

jinja = true
temp = 0.6
top-p = 0.95
top-k = 20
min-p = 0.05
repeat-penalty = 1.05
```

### Step 5: Download Model Files (`wget`)

Using `config.ini` as the single source of truth, download your required model files (base models, vision projectors, draft models) using `wget`. Use `-O` to save files with the exact local names specified in your `config.ini` file (examples shown below):

```bash
cd ~/models
wget -c "https://huggingface.co/ggml-org/gemma-4-E2B-GGUF/resolve/main/gemma-4-E2B-Q8_0.gguf" \
  -O ~/models/gemma-4-E2B-Q8_0.gguf

# Base Model
wget -c "https://huggingface.co/unsloth/gemma-4-12b-it-GGUF/resolve/main/gemma-4-12b-it-UD-Q6_K_XL.gguf" \
  -O ~/models/gemma-4-12b-it-UD-Q6_K_XL.gguf

# Vision Projector
wget -c "https://huggingface.co/unsloth/gemma-4-12b-it-GGUF/resolve/main/mmproj-BF16.gguf" \
  -O ~/models/gemma-4-12B-it-mmproj-BF16.gguf

# Draft Model
wget -c "https://huggingface.co/williamliao/gemma-4-12B-it-DFlash-GGUF/resolve/main/gemma4-12B-it-DFlash-Q4_K_M.gguf" \
  -O ~/models/gemma-4-12B-it-DFlash-Q4_K_M.gguf
```

### Step 6: Start Server with Single Unified Command

Run `llama-server` with the master preset configuration file:

```bash
llama-server \
  --models-preset ~/models/config.ini \
  --fit off \
  --models-max 1
```

> [!TIP]
> Since `host = 0.0.0.0` and `port = 8080` are defined globally in `config.ini` under `[*]`, you do **not** need to pass `--host` or `--port` on the command line. Passing them on the command line is only necessary if you want to temporarily override the `.ini` settings (e.g. `--host 127.0.0.1` for local-only testing).

| Parameter | Function |
|-----------|----------|
| `--models-preset ~/models/config.ini` | Loads all registered model classes, global parameters (`host`, `port`, `ctx-size`), and individual sampling settings |
| `--fit off` | Prevents automatic context fitting; respects explicitly defined model context limits |
| `--models-max 1` | Retains at most 1 model in VRAM at a time (automatically unloads idle models when switching) |

### Step 7: Systemd Service (On-Demand / Auto-Start)

Create `~/.config/systemd/user/llama-server.service` to manage the preset server as a background service:

```ini
[Unit]
Description=llama.cpp OpenAI-Compatible Preset Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/llama-server \
    --models-preset %h/models/config.ini \
    --fit off \
    --models-max 1
Restart=on-failure
RestartSec=10s

Environment=CUDA_VISIBLE_DEVICES=0

[Install]
WantedBy=default.target
```

Reload user systemd daemon:
```bash
systemctl --user daemon-reload
```

Choose one of the two paths below based on how this machine is used:

#### Path A: On-Demand (Shared Desktop + AI Machine)

```bash
# Start server
systemctl --user start llama-server.service

# Stop server (releases VRAM for desktop tasks)
systemctl --user stop llama-server.service

# Monitor status and logs
systemctl --user status llama-server.service
journalctl --user -u llama-server.service -f
```

#### Path B: Auto-Start at Boot (Dedicated AI Server)
```bash
systemctl --user enable --now llama-server.service
sudo loginctl enable-linger $USER
```

> [!NOTE]
> `enable-linger` allows user services to start at boot even before you log in.

To revert to on-demand later:
```bash
systemctl --user disable llama-server.service
```

### Step 8: Network & Firewall Setup

If `ufw` is active, open TCP port 8080:

```bash
sudo ufw allow 8080/tcp comment "llama.cpp server"
sudo ufw reload
```

Display host IP address:
```bash
ip -brief addr show | grep UP
```

### Step 9: Shell Aliases & Helper Function

Add to `~/.config/zsh/aliases.zsh` (or `~/.bashrc`):

```bash
# Start preset server in foreground
alias llama-start='llama-server --models-preset ~/models/config.ini --fit off --models-max 1'

# Helper function to send prompts to specific model classes
function llm() {
  local model="${1:-ggml-org/gemma-4-E2B-GGUF}"
  shift
  local prompt="${*}"
  curl -s http://127.0.0.1:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"${model}\",\"messages\":[{\"role\":\"user\",\"content\":\"${prompt}\"}]}" \
    | python -m json.tool
}
```

---

## Verification

```bash
# Check service status
systemctl --user status llama-server.service

# Verify GPU VRAM utilization
nvidia-smi

# List registered models from preset config via OpenAI API endpoint
curl -s http://127.0.0.1:8080/v1/models | python -m json.tool

# Test inference request against specific model class
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ggml-org/gemma-4-E2B-GGUF",
    "messages": [{"role": "user", "content": "Hello world!"}]
  }'
```

---

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| `config.ini not found` | Path mismatch | Ensure file exists at `~/models/config.ini` and paths in INI match `/home/aritro/models/` |
| `File not found: model.gguf` | Filename mismatch | Check `wget` commands used exact `-O` filenames corresponding to `config.ini` |
| Out of VRAM error | Multiple models remaining loaded | Ensure `--models-max 1` is passed to `llama-server` |
| Speculative draft error | Missing draft GGUF | Re-run draft model `wget` / `cp` download steps |
| Cannot connect from LAN | Firewall blocking / default binding | Ensure `--host 0.0.0.0` and `sudo ufw allow 8080/tcp` |

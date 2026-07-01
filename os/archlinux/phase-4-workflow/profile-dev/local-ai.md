# Local AI Models

> **Phase**: 4 — Workflow (Developer Profile)
> **Prerequisites**: [Containers](./containers.md), [NVIDIA Drivers](../../phase-2-system-hardening/nvidia-drivers.md)
> **Packages**: `nvidia-container-toolkit`

---

## Overview

Run local AI models (Ollama) inside Podman containers with NVIDIA GPU acceleration, accessible via a web UI.

## Steps

### Step 1: Install NVIDIA Container Toolkit

```bash
sudo pacman -Syu nvidia-container-toolkit
```

Verify:
```bash
nvidia-ctk --version
```

### Step 2: Generate CDI Config

> [!IMPORTANT]
> This must be re-run **every time NVIDIA drivers are updated**.

```bash
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
nvidia-ctk cdi list
```

### Step 3: (Optional) Verify GPU Access in Containers

```bash
podman pull ubuntu
podman run --privileged --rm --gpus all ubuntu nvidia-smi
```

You should see `nvidia-smi` output with your GPU name. The process list should be empty (running from inside the container).

### Step 4: Install Ollama

```bash
podman pull docker.io/ollama/ollama
mkdir -p ~/LocalModels
```

Run the Ollama container:
```bash
podman run --name ollama --rm --detach --privileged --gpus all \
  -p 11434:11434 \
  -v $PWD/LocalModels/:/root/.ollama \
  ollama/ollama
```

Check logs:
```bash
podman logs -f ollama
```

It should mention your NVIDIA GPU name.

### Step 5: Shell Aliases

Add to `~/.config/zsh/aliases.zsh` (or `~/.bashrc`):

```bash
# Alias to run ollama commands inside the container
alias ollama='podman exec ollama ollama'

# Start Open WebUI on a custom or default port
function start-webui() {
  local port="${1:-11435}"
  echo "Starting Open WebUI on host port: ${port}"
  podman run \
    -d \
    --name open-webui \
    --rm \
    -p "${port}:8080" \
    -e OLLAMA_BASE_URL=http://host.containers.internal:11434 \
    -e WEBUI_AUTH=false \
    ghcr.io/open-webui/open-webui:main
}
```

### Step 6: Setup Models

```bash
ollama pull deepseek-r1
```

### Step 7: Web UI

```bash
podman pull ghcr.io/open-webui/open-webui:main
start-webui
```

Open [http://127.0.0.1:11435](http://127.0.0.1:11435) in your browser.

## Verification

```bash
ollama list    # Should show downloaded models
podman ps      # Should show ollama container running
```

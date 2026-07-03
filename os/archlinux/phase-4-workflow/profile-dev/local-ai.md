# Local AI (llama.cpp)

> **Phase**: 4 — Workflow (Developer Profile)
> **Prerequisites**: [NVIDIA Drivers](../../phase-2-system-hardening/nvidia-drivers.md), [AUR Helper](../../phase-2-system-hardening/aur-helper.md)
> **Packages**: `cuda llama-cpp-cuda` (AUR)

---

## Overview

Run local AI models natively on your GPU using **llama.cpp** — no containers required. The `llama-server` binary provides an OpenAI-compatible API endpoint and a built-in web chat UI, accessible to any device on your local network.

> [!NOTE]
> Model selection and customization are out of scope for this guide. We use the [Gemma 4 E2B IT QAT Q4_0 GGUF](https://huggingface.co/google/gemma-4-E2B-it-qat-q4_0-gguf) model as the reference — a lightweight quantized model suitable for quick validation. Swap the model path for any other GGUF model as needed.

## Reference

- [Arch Wiki: llama.cpp](https://wiki.archlinux.org/title/Llama.cpp)
- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [llama-server documentation](https://github.com/ggml-org/llama.cpp/blob/master/examples/server/README.md)
- [Gemma 4 E2B GGUF (Hugging Face)](https://huggingface.co/google/gemma-4-E2B-it-qat-q4_0-gguf)

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

Install the AUR package with CUDA support:

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

```bash
mkdir -p ~/models
```

### Step 4: Download a Model

Use `llama-server`'s built-in Hugging Face downloader to fetch the model. The `-hf` flag downloads and caches the GGUF files automatically.

By default, `-hf` stores files under `~/.cache/huggingface/` in a repo-specific subfolder (e.g. `gemma-4-E2B-it-qat-q4_0-gguf/`). To keep everything in `~/models` instead, set the `LLAMA_CACHE` environment variable:

```bash
LLAMA_CACHE=~/models llama-server \
  -hf google/gemma-4-E2B-it-qat-q4_0-gguf \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl 99
```

This downloads the model files into `~/models/` on first run and starts serving immediately.

> [!TIP]
> To make this permanent, export the variable in your shell profile:
> ```bash
> echo 'export LLAMA_CACHE=~/models' >> ~/.config/zsh/.zshenv
> ```
> After that, plain `llama-server -hf ...` commands will use `~/models` automatically.

Alternatively, download the GGUF file manually with `curl` or `wget` into `~/models/`:

```bash
# Example: download manually (check HuggingFace for exact filename)
cd ~/models
wget "https://huggingface.co/google/gemma-4-E2B-it-qat-q4_0-gguf/resolve/main/gemma-4-E2B-it-qat-q4_0.gguf"
```

### Step 5: Quick Test (Local Only)

Run the server locally to verify everything works:

```bash
llama-server \
  -m ~/models/gemma-4-E2B-it-qat-q4_0.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl 99
```

| Flag | Purpose |
|------|---------|
| `-m` | Path to the GGUF model file |
| `--host 127.0.0.1` | Listen on localhost only (for testing) |
| `--port 8080` | HTTP port for the API and web UI |
| `-ngl 99` | Offload all model layers to the GPU (use `-1` for "all") |

Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser — you should see the built-in chat UI.

Test the OpenAI-compatible API:
```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4-E2B",
    "messages": [{"role": "user", "content": "Hello, who are you?"}]
  }'
```

### Step 6: Serve Across the Local Network

Once the local test passes, bind to all interfaces:

```bash
llama-server \
  -m ~/models/gemma-4-E2B-it-qat-q4_0.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 99
```

> [!WARNING]
> `--host 0.0.0.0` exposes the server to your entire LAN. `llama-server` has **no built-in authentication**. Only use this on a trusted local network.

If you have ufw enabled ([Firewall](../../phase-2-system-hardening/firewall.md)), allow the port:

```bash
sudo ufw allow 8080/tcp comment "llama.cpp server"
sudo ufw reload
```

Other devices on the network can now access:
- **Web UI**: `http://<your-ip>:8080`
- **API**: `http://<your-ip>:8080/v1/chat/completions`

Find your IP address:
```bash
ip -brief addr show | grep UP
```

### Step 7: Systemd Service (On-Demand)

Create a user-level systemd service to manage the server cleanly — but **do not enable it at boot**. Since this machine is also used for desktop work, you decide when to give up VRAM for inference.

Create the service file:
```bash
mkdir -p ~/.config/systemd/user
nvim ~/.config/systemd/user/llama-server.service
```

Paste the following:
```ini
[Unit]
Description=llama.cpp OpenAI-Compatible Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment=LLAMA_CACHE=%h/models
ExecStart=/usr/bin/llama-server \
    -m %h/models/gemma-4-E2B-it-qat-q4_0.gguf \
    --host 0.0.0.0 \
    --port 8080 \
    -ngl 99
Restart=on-failure
RestartSec=10s

# Resource limits
Environment=CUDA_VISIBLE_DEVICES=0

[Install]
WantedBy=default.target
```

> [!NOTE]
> `%h` expands to the user's home directory in systemd unit files. Adjust the model path if you use a different model.

Load the service (one-time):
```bash
systemctl --user daemon-reload
```

Choose one of the two paths below based on how this machine is used:

#### Path A: On-Demand (Shared Desktop + AI Machine)

Start and stop the server manually when you need it. This keeps VRAM free for desktop work when not doing inference.

```bash
# Start the server
systemctl --user start llama-server.service

# Stop the server (frees VRAM for other work)
systemctl --user stop llama-server.service

# Check status / follow logs
systemctl --user status llama-server.service
journalctl --user -u llama-server.service -f
```

#### Path B: Auto-Start at Boot (Dedicated AI Server)

If this machine is a dedicated inference server, enable the service to start automatically on boot:

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

### Step 8: Shell Aliases

Add to `~/.config/zsh/aliases.zsh` (or `~/.bashrc`):

```bash
# Quick-start llama server (foreground, for testing)
alias llama-start='llama-server -m ~/models/gemma-4-E2B-it-qat-q4_0.gguf --host 0.0.0.0 --port 8080 -ngl 99'

# Quick chat via API
function llm() {
  local prompt="${*}"
  curl -s http://127.0.0.1:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"local\",\"messages\":[{\"role\":\"user\",\"content\":\"${prompt}\"}]}" \
    | python -m json.tool
}
```

## Verification

```bash
# Check the service is running
systemctl --user status llama-server.service

# Verify GPU is being used
nvidia-smi    # Should show llama-server process using VRAM

# Test the API
curl -s http://127.0.0.1:8080/v1/models | python -m json.tool

# Test from another machine on the network
curl http://<server-ip>:8080/v1/models
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `llama-server: command not found` | Ensure `llama-cpp-cuda` is installed: `yay -S llama-cpp-cuda` |
| `CUDA error` / no GPU detected | Verify `nvidia-smi` works, reinstall `cuda` package |
| Slow inference (CPU fallback) | Check `-ngl 99` flag is set, ensure CUDA build (not CPU-only) |
| OOM (out of memory) | Model too large for VRAM — try a smaller quantization or reduce context with `-c 4096` |
| Cannot connect from LAN | Check `--host 0.0.0.0` is set, verify `ufw allow 8080/tcp` |
| Service won't start at boot | Enable lingering: `sudo loginctl enable-linger $USER` |
| Model download fails (HF) | Check network, or download `.gguf` file manually with `wget` |

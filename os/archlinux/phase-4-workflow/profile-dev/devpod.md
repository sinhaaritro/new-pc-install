# DevPod

> **Phase**: 4 — Workflow (Developer Profile)
> **Prerequisites**: [Containers](./containers.md)
> **Packages**: None (installed via curl)

---

## Overview

**DevPod** creates reproducible dev environments using containers. The GUI doesn't work on Wayland, so we use the CLI with Podman as the provider.

## TODO

- [ ] Create custom devpod environment
- [ ] Create custom features
- [ ] Configure devpod to write code inside devpod using SSH and NeoVim installed on host
- [ ] Configure devpod with remote NeoVim setup on host machine

## Steps

### Step 1: Install DevPod CLI

```bash
curl -L -o devpod "https://github.com/loft-sh/devpod/releases/latest/download/devpod-linux-amd64" \
  && sudo install -c -m 0755 devpod /usr/local/bin \
  && rm -f devpod
```

### Step 2: Add Docker Provider

```bash
devpod provider add docker
```

Verify:
```bash
devpod provider list
```

### Step 3: Configure for Podman

Point the Docker provider to Podman:
```bash
devpod provider set-options docker -o DOCKER_PATH=/usr/bin/podman
```

### Step 4: Test with a Sample Environment

```bash
devpod up github.com/microsoft/vscode-remote-try-node --ide openvscode
```

This opens a Node.js dev environment in your browser.

## Verification

```bash
devpod list    # Should show running workspaces
```

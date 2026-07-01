# Containers (Podman)

> **Phase**: 4 — Workflow (Developer Profile)
> **Prerequisites**: [First Reboot](../../phase-1-base-system/08-first-reboot.md)
> **Packages**: `podman`

---

## Overview

Set up **Podman** as a rootless, daemonless container runtime (Docker alternative). Includes `lazydocker` integration via podman socket.

> [!NOTE]
> `lazydocker` doesn't natively support Podman, but works via the Podman Docker-compatible socket.

## Steps

### Step 1: Install Podman

```bash
sudo pacman -S podman
```

### Step 2: Configure User Namespaces

Create subuid/subgid files if they don't exist (usually pre-configured):

```bash
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 USERNAME
```

*(Replace `USERNAME` with your actual username)*

Run migration:
```bash
podman system migrate
```

### Step 3: Configure Podman with lazydocker

Install lazydocker (via AUR):
```bash
yay -S lazydocker
```

Enable the Podman socket service:
```bash
systemctl --user enable --now podman.socket
```

Add an alias to your shell config (`~/.zshrc` or `~/.bashrc`):
```bash
alias lazypodman='DOCKER_HOST=unix:///run/user/1000/podman/podman.sock lazydocker'
```

### Step 4: Test

```bash
podman run --rm hello-world
lazypodman
```

## Verification

```bash
podman info
podman ps
```

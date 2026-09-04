# Dotfiles (GNU Stow)

> **Phase**: 3 — Desktop
> **Prerequisites**: [SSH & Git](../phase-2-system-hardening/ssh.md)
> **Packages**: `stow`

---

## Overview

Use **GNU Stow** to manage dotfiles as symlinks from a central git repository. This makes your configuration portable, version-controlled, and easy to restore on a fresh install.

The dotfiles repo is **private** and lives at `git@github.com:sinhaaritro/dotfiles.git`. It is fetched over SSH with the end user's key (the one created by the [SSH & Git](../phase-2-system-hardening/ssh.md) module) and checked out to `~/dotfiles`.

This module (Phase 3) **installs stow and bootstraps `~/dotfiles`**. The actual clone + `stow` application is performed by the **[Desktop Config](./hyprland/01-install.md)** module, which runs last in the desktop play.

> **Moved from Phase 4 to Phase 3.** Dotfiles were originally the shared Phase 4 module. Because `desktop-config` stows the compositor config from `~/dotfiles`, the dotfiles setup is a desktop dependency and now belongs in Phase 3.

## How it works (automation)

- **`dotfiles-backup` role** — installs `stow`; ensures `~/dotfiles` exists as a git repo (creates it only if absent; never re-inits over an existing repo).
- **`desktop-config` role** — the last step of the desktop play. It clones the private repo over SSH (or `git pull`s if already present) and runs `stow <pkg>` for every top-level stow package in the repo, as the end user.

**Graceful degradation:** `desktop-config` runs last, so an SSH/auth failure does **not** fail the play. If the repo can't be fetched (key not registered, or no network), it prints a "register your key / re-run" message and skips. Once the key is registered, re-run:

```bash
ansible-playbook 30-desktop.yml --tags desktop-config
```

## Manual steps (reference)

### Install

```bash
sudo pacman -S stow
```

### Fetch the private repo (over SSH)

```bash
# your key must be registered on the repo first
git clone git@github.com:sinhaaritro/dotfiles.git ~/dotfiles
cd ~/dotfiles
git pull --ff-only
```

### Apply every stow package

```bash
cd ~/dotfiles
for pkg in */; do stow "${pkg%/}"; done
```

## Naming Convention

```
[type]_[name]_[variant]
```

| Type | Meaning | Example |
|------|---------|---------|
| `p` | Package-specific config | `p_kitty`, `p_neovim` |
| `s` | Style (groups multiple packages) | `s_dark_theme` |

Example layout:

```
~/dotfiles/
├── p_hyprland/.config/hypr/
├── p_kitty/.config/kitty/
├── p_waybar/.config/waybar/
├── p_rofi/.config/rofi/
├── p_zsh/.zshrc (and .config/zsh/)
├── p_neovim/.config/nvim/
└── p_swaync/.config/swaync/
```

> [!WARNING]
> `stow --adopt <pkg>` moves existing files INTO the stow directory, potentially overwriting your repo versions. If you adopt, run `git checkout -- .` afterwards to restore the repo's versions.

## Verification

```bash
# stow installed
stow --version

# repo present and current
ls -la ~/dotfiles/.git

# a stowed config is a symlink back into the repo
ls -la ~/.config/hypr/
```

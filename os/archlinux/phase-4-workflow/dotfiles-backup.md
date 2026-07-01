# Dotfiles Backup (GNU Stow)

> **Phase**: 4 — Workflow (shared across all profiles)
> **Prerequisites**: [SSH & Git](../phase-2-system-hardening/ssh.md)
> **Packages**: `stow`

---

## Overview

Use **GNU Stow** to manage dotfiles as symlinks from a central git repository. This makes your configuration portable, version-controlled, and easy to restore on a fresh install.

## Naming Convention

```
[type]_[name]_[variant]
```

| Type | Meaning | Example |
|------|---------|---------|
| `p` | Package-specific config | `p_kitty`, `p_neovim` |
| `s` | Style (groups multiple packages) | `s_dark_theme` |

## Steps

### Step 1: Install

```bash
sudo pacman -S stow
```

### Step 2: Create Dotfiles Repository

```bash
mkdir ~/dotfiles
cd ~/dotfiles
git init
```

### Step 3: Move Existing Configs

Example for Kitty:
```bash
mkdir -p ~/dotfiles/p_kitty/.config/kitty
mv ~/.config/kitty/* ~/dotfiles/p_kitty/.config/kitty/
```

### Step 4: Stow (Create Symlinks)

```bash
cd ~/dotfiles
stow p_kitty
```

This creates symlinks from `~/dotfiles/p_kitty/.config/kitty/*` → `~/.config/kitty/*`.

### Step 5: Adopt Existing Configs

If configs already exist at the target location:
```bash
stow --adopt p_kitty
git checkout -- .  # Reset to git version (overrides adopted files)
```

> [!WARNING]
> `--adopt` moves existing files INTO the stow directory, potentially overwriting your repo versions. Always `git checkout` afterwards to restore the repo's versions.

### Suggested Stow Packages

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

## Verification

```bash
ls -la ~/.config/kitty/
# Should show symlinks pointing to ~/dotfiles/p_kitty/.config/kitty/
```

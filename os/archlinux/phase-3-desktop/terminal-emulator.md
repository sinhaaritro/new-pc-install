# Terminal Emulator

> **Phase**: 3 — Desktop
> **Prerequisites**: [Fonts](./fonts.md)
> **Packages**: `kitty`

---

## Overview

Install a terminal emulator — the GUI window that renders your shell. This module is **WM-independent**: both the shell (zsh, via the [Shell & Terminal](./shell-and-terminal.md) module) and the window manager open in it, so it installs **before** [Window Manager](./hyprland/01-install.md).

`kitty` is the default (GPU-accelerated, Wayland-native, fast font rendering). The module is built to expand — adding `alacritty`, `ghostty`, or another emulator is a data-only change (add the package to the manifest + `group_vars/<distro>.yml`); no role rewrite.

## Steps

### Step 1: Install Kitty

```bash
sudo pacman -S kitty
```

| Package | Purpose |
|---------|---------|
| `kitty` | GPU-accelerated Wayland terminal emulator |

> [!NOTE]
> Configuration (`~/.config/kitty/kitty.conf`) is owned by the user's stow package (ADR-011) — this module only installs the binary. Fonts must be installed first (the [Fonts](./fonts.md) module) or Kitty renders glyph boxes.

### Step 2: Verify from the TTY

Before launching a compositor, confirm the emulator works standalone:

```bash
kitty --version
kitty   # opens a terminal window; type a command, then 'exit' to close
```

## Expanding to Other Emulators

To swap or add an emulator later:

1. Add the package to the `terminal-emulator` module in `os/archlinux/manifest.yaml`.
2. Add it to `distro_packages.terminal_emulator` in `ansible/inventory/group_vars/archlinux.yml`.
3. Re-run `make run-phase3` (the universal install loop picks it up — no role change).

Candidates: `alacritty` (Vulkan, minimal), `ghostty` (fast, built-in ligatures), `st` (static, hackable).

## Verification

- [ ] `kitty --version` prints a version
- [ ] Launching `kitty` from the TTY opens a terminal window
- [ ] A shell prompt appears and accepts input
- [ ] Fonts render correctly (no glyph boxes) — requires the Fonts module

## Reference

- [Kitty Docs](https://sw.kovidgoyal.net/kitty/)
- [Kitty Config](https://sw.kovidgoyal.net/kitty/conf/)

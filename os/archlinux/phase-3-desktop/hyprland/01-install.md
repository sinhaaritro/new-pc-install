# Window Manager

> **Phase**: 3 — Desktop
> **Module**: `desktop-install` (WM-agnostic id; the concrete compositor is selected by `wm_vendor`, hyprland today)
> **Prerequisites**: [GPU (NVIDIA)](../../phase-1-base-system/07-gpu-nvidia.md), [Terminal Emulator](../terminal-emulator.md)
> **Packages**: `wayland hyprland xdg-desktop-portal-hyprland qt5-wayland qt6-wayland firefox`

---

## Overview

Install the window manager (Hyprland, via `wm_vendor`) and launch into a graphical environment for the first time. The terminal emulator (Kitty) is installed by the [Terminal Emulator](../terminal-emulator.md) module, which runs before this one.

## Steps

### Step 1: Install Wayland

```bash
sudo pacman -S wayland
```

### Step 2: Install the Window Manager and Essentials

```bash
sudo pacman -S hyprland xdg-desktop-portal-hyprland qt5-wayland qt6-wayland firefox
```

| Package | Purpose |
|---------|---------|
| `hyprland` | Tiling Wayland compositor |
| `xdg-desktop-portal-hyprland` | Screen sharing, file picker portals |
| `qt5-wayland` / `qt6-wayland` | Qt app Wayland support |
| `firefox` | Web browser |

> [!NOTE]
> The terminal emulator and file manager are separate modules: [Terminal Emulator](../terminal-emulator.md) and [File Manager](../file-manager.md).

### Step 3: Launch Hyprland

From the TTY (after login), run:
```bash
Hyprland
```

You should see a tiled desktop. The default keybinds:
- `SUPER + Q` — Open Kitty terminal
- `SUPER + C` — Close focused window
- `SUPER + M` — Exit Hyprland
- `SUPER + 1-9` — Switch workspaces
- `SUPER + Arrow Keys` — Move focus

> [!NOTE]
> Hyprland creates a default config at `~/.config/hypr/hyprland.conf` on first launch. Customization is covered in [Core Config](./02-core-config.md).

## Reference

- [Hyprland Wiki](https://wiki.hyprland.org/)
- [Hyprland Configuring](https://wiki.hyprland.org/Configuring/Variables/#input)
- [hyprdots](https://github.com/prasanthrangan/hyprdots) — Popular Hyprland dotfile collection

## Verification

- [ ] Hyprland launches from TTY without errors
- [ ] Kitty terminal (installed by the Terminal Emulator module) opens with `SUPER + Q`
- [ ] Firefox launches from terminal
- [ ] `SUPER + M` exits Hyprland cleanly back to TTY

# Install Hyprland

> **Phase**: 3 — Desktop
> **Prerequisites**: [NVIDIA Drivers](../../phase-2-system-hardening/nvidia-drivers.md)
> **Packages**: `wayland hyprland xdg-desktop-portal-hyprland kitty qt5-wayland qt6-wayland firefox yazi`

---

## Overview

Install the Hyprland Wayland compositor, Kitty terminal, and launch into a graphical environment for the first time.

## Steps

### Step 1: Install Wayland

```bash
sudo pacman -S wayland
```

### Step 2: Install Hyprland and Essentials

```bash
sudo pacman -S hyprland xdg-desktop-portal-hyprland kitty qt5-wayland qt6-wayland firefox yazi
```

| Package | Purpose |
|---------|---------|
| `hyprland` | Tiling Wayland compositor |
| `xdg-desktop-portal-hyprland` | Screen sharing, file picker portals |
| `kitty` | GPU-accelerated terminal (Hyprland's default) |
| `qt5-wayland` / `qt6-wayland` | Qt app Wayland support |
| `firefox` | Web browser |
| `yazi` | TUI file manager |

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
- [ ] Kitty terminal opens with `SUPER + Q`
- [ ] Firefox launches from terminal
- [ ] `SUPER + M` exits Hyprland cleanly back to TTY

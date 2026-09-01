# Phase 3: Desktop

> **Milestone**: Full graphical desktop environment with Hyprland, status bar, launcher, and essential GUI tools.
> **Prerequisite**: [GPU (NVIDIA)](../phase-1-base-system/07-gpu-nvidia.md) from Phase 1.

## Window Manager

Currently, this guide covers **Hyprland**. The structure supports adding alternatives (e.g., Niri, Sway) as additional `wm-*/` subdirectories in the future.

### Hyprland Modules (Sequential)

| # | Module | Required | Depends On | Notes |
|---|--------|----------|------------|-------|
| 1 | [Install Hyprland](./hyprland/01-install.md) | ✅ Required | NVIDIA Drivers | Wayland, Hyprland, Kitty, first launch |
| 2 | [Core Config](./hyprland/02-core-config.md) | ✅ Required | #1 | Keybinds, monitors, window rules |
| 3 | [Lock & Idle](./hyprland/03-lock-idle.md) | ⚡ Recommended | #2 | hyprlock, hypridle |
| 4 | [Wallpaper](./hyprland/04-wallpaper.md) | 💡 Optional | #2 | swww animated wallpapers |
| 5 | [Screen Sharing](./hyprland/05-screen-sharing.md) | ⚡ Recommended | #2, Sound | For video calls |

## Shared Desktop Modules (Order Flexible)

These work with any window manager:

| # | Module | Required | Depends On | Notes |
|---|--------|----------|------------|-------|
| 6 | [Shell & Terminal](./shell-and-terminal.md) | ⚡ Recommended | #1 | zsh, oh-my-zsh, fzf, zoxide |
| 7 | [App Launcher](./app-launcher.md) | ⚡ Recommended | #1 | rofi-wayland |
| 8 | [Status Bar](./status-bar.md) | ⚡ Recommended | #1 | waybar |
| 9 | [Notifications](./notifications.md) | ⚡ Recommended | #1 | swaync |
| 10 | [Display Manager](./display-manager.md) | 💡 Optional | #1 | greetd + tuigreet |
| 11 | [Clipboard](./clipboard.md) | ⚡ Recommended | #1 | wl-clipboard, clipse |
| 12 | [Screenshots](./screenshots.md) | 💡 Optional | #1 | grim, slurp, swappy |
| 13 | [File Manager](./file-manager.md) | ⚡ Recommended | #1 | yazi, thunar |
| 14 | [Fonts](./fonts.md) | ⚡ Recommended | #1 | Nerd Fonts, Noto |

## What's Next

After your desktop is functional, proceed to [Phase 4: Workflow](../phase-4-workflow/README.md) to install tools for your use case (Dev / Gaming / Creative).

# System Overview

> **Phase**: 0 — Pre-Install
> **Prerequisites**: None
> **Packages**: None

---

## Overview

This guide installs **Arch Linux** as a modular, phased system. Each phase builds on the previous one, producing a usable system at every milestone.

## System Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| **Distro** | Arch Linux | Rolling release, minimal base |
| **Boot Loader** | GRUB | With os-prober for dual-boot Windows detection |
| **Filesystem** | Btrfs | Flat subvolume layout optimized for Snapper snapshots |
| **GPU Driver** | nvidia-open | Open kernel module for Turing+ (RTX 4070 Ti Super) |
| **Display Protocol** | Wayland | Via Hyprland compositor |
| **Window Manager** | Hyprland | Tiling Wayland compositor |
| **Terminal** | Kitty | GPU-accelerated terminal emulator |
| **Shell** | zsh + oh-my-zsh | With fzf, zoxide enhancements |
| **Config Backup** | GNU Stow | Symlink-based dotfile management |
| **Display Manager** | greetd + tuigreet | Minimal TUI login screen |
| **Lock Screen** | hyprlock | Hyprland-native lock screen |
| **App Launcher** | rofi-wayland | Search-driven application launcher |
| **File Manager (TUI)** | yazi | Terminal file manager with preview |
| **File Manager (GUI)** | Thunar | GTK file manager for drag-and-drop |
| **Status Bar** | waybar | Highly customizable status bar |
| **Wallpaper** | swww | Animated wallpaper daemon |
| **Notifications** | swaync | Notification center (Action Center equivalent) |
| **Process Viewer** | btop | TUI system monitor with GPU support |
| **Text Editor** | NeoVim | Modal editor with LSP, treesitter |
| **Media Player** | mpv | CLI-first video player |
| **Clipboard** | wl-clipboard + clipse | Clipboard with history |
| **Screenshots** | grim + slurp + swappy | Screen capture + annotation |
| **Screen Sharing** | xdg-desktop-portal-hyprland | PipeWire-based portal |
| **Audio** | PipeWire + WirePlumber | Modern audio stack replacing PulseAudio + JACK |
| **Containers** | Podman | Rootless, daemonless containers |

## Phase Map

| Phase | Milestone | What You Get |
|-------|-----------|-------------|
| **Phase 0** | Ready to install | USB prepared, BIOS configured |
| **Phase 1** | Bootable CLI system | TTY login, networking, GRUB dual-boot |
| **Phase 2** | Hardened system | GPU drivers, snapshots, audio, SSH |
| **Phase 3** | Graphical desktop | Hyprland + full desktop environment |
| **Phase 4** | Productive workflow | Dev tools / Gaming / Creative (pick any) |

## References

- [Arch Wiki](https://wiki.archlinux.org/)
- [Hyprland Wiki](https://wiki.hyprland.org/)
- [hyprdots](https://github.com/prasanthrangan/hyprdots)
- [Feature Parity Reference](../reference/feature-parity.md) — Windows → Linux equivalents lookup table

## Verification

If you can read this file, you're ready to proceed to the [Pre-Flight Checklist](./pre-flight-checklist.md).

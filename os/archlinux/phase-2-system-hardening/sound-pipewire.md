# Sound (PipeWire)

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/08-first-reboot.md)
> **Packages**: `pipewire wireplumber pipewire-alsa pipewire-pulse pipewire-jack helvum playerctl mpv-mpris`

---

## Overview

**PipeWire** is a modern multimedia framework that replaces both PulseAudio and JACK, providing a unified audio (and video) pipeline. **WirePlumber** is its session manager.

## The Linux Audio Stack

| Layer | Component | Role |
|-------|-----------|------|
| **Kernel** | ALSA | Low-level hardware drivers, direct sound card access |
| **Server** | PipeWire | Unified audio/video server (replaces PulseAudio + JACK) |
| **Session** | WirePlumber | Manages audio routing, device selection, policy |
| **Compat** | pipewire-pulse | PulseAudio API compatibility for legacy apps |
| **Compat** | pipewire-jack | JACK API compatibility for pro audio apps |
| **Compat** | pipewire-alsa | ALSA routing through PipeWire |
| **GUI** | helvum | GTK patchbay for visual audio routing |

## Steps

### Step 1: Install Packages

```bash
sudo pacman -S pipewire wireplumber pipewire-alsa pipewire-pulse pipewire-jack helvum playerctl mpv-mpris
```

### Step 2: Enable Services

PipeWire runs as a **user service** (not system):

```bash
systemctl --user enable --now pipewire.socket
systemctl --user enable --now pipewire-pulse.socket
systemctl --user enable --now wireplumber.service
```

### Step 3: Media Key Control (playerctl)

`playerctl` lets you control media playback from keybinds (useful for Hyprland):

```bash
# Pause Firefox audio
playerctl --player=firefox pause

# Toggle play/pause for mpv
playerctl --player=mpv play-pause

# Next track
playerctl next
```

> [!TIP]
> `mpv-mpris` is needed for `playerctl` to control mpv. Install it alongside playerctl.

## Verification

```bash
# Check PipeWire is running
systemctl --user status pipewire

# List audio devices
wpctl status

# Play a test sound
speaker-test -c 2
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No sound output | Run `wpctl status` and check the default sink |
| `wpctl` shows no devices | Ensure WirePlumber is running: `systemctl --user restart wireplumber` |
| Need advanced audio routing | Launch `helvum` for a visual patchbay |

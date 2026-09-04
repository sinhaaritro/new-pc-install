# Clipboard

> **Phase**: 3 — Desktop
> **Prerequisites**: [Window Manager](./hyprland/01-install.md)
> **Packages**: `wl-clipboard clipse`

---

## Overview

Set up a clipboard history manager in Wayland using **wl-clipboard** (for low-level copy/paste) and **clipse** (a TUI-based clipboard history listener and selector).

## Steps

### Step 1: Install Packages

```bash
sudo pacman -S wl-clipboard clipse
```

| Package | Purpose |
|---------|---------|
| `wl-clipboard` | Command line copy/paste utilities (`wl-copy` and `wl-paste`) |
| `clipse` | TUI clipboard manager with clipboard history and terminal selector |

### Step 2: Configure Clipse Daemon Autostart

`clipse` needs to run as a background daemon to listen to copy events and keep track of clipboard history.

Add the following to your Hyprland configuration (`~/.config/hypr/hyprland.conf`):

```text
exec-once = clipse -listen # Run clipboard history daemon
```

### Step 3: Configure Clipse Keyboard Shortcut

To open the history selection menu inside a floating terminal window, define a keybind in your Hyprland configuration.

Add this keybind (e.g., using `SUPER + V`):

```text
# Open clipboard history in a floating window
bind = SUPER, V, exec, kitty --class clipse -e clipse
windowrulev2 = float, class:^(clipse)$
windowrulev2 = size 622 352, class:^(clipse)$
```

## Usage

1. **Copy text** normally from any app (browser, editor, terminal).
2. **Press `SUPER + V`** to open the floating terminal clipboard manager.
3. Use the arrow keys or `j`/`k` to navigate your history.
4. Press **Enter** to select and put the active item back into your clipboard.
5. Press **Esc** or **q** to close the window.

## Verification

```bash
# Verify wl-clipboard works
echo "Testing Clipboard" | wl-copy
wl-paste # Should output: Testing Clipboard
```

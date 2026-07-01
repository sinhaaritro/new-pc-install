# Wi-Fi & Bluetooth

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/08-first-reboot.md)
> **Packages**: `iwd impala bluez bluez-utils bluetui wl-clipboard clipse`

---

## Overview

Configure Wi-Fi via `iwd` (backend for NetworkManager) and Bluetooth via `bluez` with a TUI interface.

## Wi-Fi

### Step 1: Install Packages

```bash
sudo pacman -S iwd impala
```

### Step 2: Configure iwd as NetworkManager Backend

Create the configuration file:
```bash
sudo nvim /etc/NetworkManager/conf.d/wifi_backend.conf
```

Add:
```ini
[device]
wifi.backend=iwd
```

Restart NetworkManager:
```bash
sudo systemctl restart NetworkManager
```

### Step 3: Connect via iwctl

```bash
iwctl
```

Inside the interactive prompt:
```
device list
device DEVICE_NAME set-property Powered on
station DEVICE_NAME scan
station DEVICE_NAME get-networks
station DEVICE_NAME connect SSID
```

> [!TIP]
> `impala` provides a TUI for Wi-Fi management as an alternative to `iwctl`.

---

## Bluetooth

### Step 1: Install Packages

```bash
sudo pacman -S bluez bluez-utils bluetui
```

### Step 2: Enable Bluetooth Service

```bash
sudo systemctl enable --now bluetooth.service
```

### Step 3: Pair and Connect Devices

Using `bluetoothctl`:
```bash
bluetoothctl
```

Inside the interactive prompt:
```
power on
scan on
pair MAC_ADDRESS
trust MAC_ADDRESS
connect MAC_ADDRESS
scan off
```

To disconnect:
```
disconnect MAC_ADDRESS
power off
```

> [!TIP]
> `bluetui` provides a TUI interface for Bluetooth management. Just run `bluetui` for a visual device list.

---

## Clipboard

### Install

```bash
sudo pacman -S wl-clipboard clipse
```

| Package | Purpose |
|---------|---------|
| `wl-clipboard` | `wl-copy` and `wl-paste` commands for Wayland clipboard |
| `clipse` | TUI clipboard history manager |

---

## Volume & Power

*(These are configured via Hyprland keybinds and waybar modules in [Phase 3](../phase-3-desktop/README.md))*

## Verification

```bash
# Wi-Fi
nmcli device status

# Bluetooth
bluetoothctl show

# Clipboard
echo "test" | wl-copy
wl-paste
```

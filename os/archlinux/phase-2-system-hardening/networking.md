# Wi-Fi, Ethernet & Bluetooth

> **Phase**: 2 — System Hardening
> **Prerequisites**: [AUR Helper (yay)](./aur-helper.md)
> **Packages**: `bluez bluez-utils bluetui` (and `wlctl-bin` via AUR)

---

## Overview

Configure networking (Wi-Fi, Ethernet, VPN) using **wlctl** (a terminal user interface that directly manages NetworkManager) and Bluetooth using **bluez** with the **bluetui** TUI.

Using `wlctl` eliminates the need to configure `iwd` or rewrite NetworkManager backends, preserving stability and default system configs.

---

## Wi-Fi, Ethernet & VPN (wlctl)

### Step 1: Install wlctl

Since `wlctl` is in the Arch User Repository, install it using `yay`:

```bash
yay -S wlctl-bin
```

### Step 2: Manage Connections

Launch the interactive TUI:

```bash
wlctl
```

#### Keybindings & Controls

- **Arrow keys** or **j/k** to navigate connections.
- **Enter** to connect/disconnect.
- **Tab** to switch between adapters or panels.
- **v** to view detailed properties.
- **q** to quit.

#### Diagnostics

Run the built-in diagnostic doctor to verify hardware, rfkill, driver, and IP status:

```bash
wlctl doctor
```

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

## Verification

```bash
# Wi-Fi & Ethernet
wlctl doctor
nmcli device status

# Bluetooth
bluetoothctl show
```

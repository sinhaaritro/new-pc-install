# Verify Boot Mode & Network Connection

> **Phase**: 1 — Base System
> **Prerequisites**: [Pre-Flight Checklist](../phase-0-pre-install/pre-flight-checklist.md)
> **Packages**: None (live environment)

---

## Overview

Before partitioning, confirm you're booted in UEFI mode (not Legacy/CSM) and have an active internet connection. Both are required for the installation to succeed.

## Steps

### Step 1: Verify UEFI Boot Mode

Check that the EFI variables directory exists:

```bash
ls /sys/firmware/efi/efivars
```

If this directory exists and lists files, you are in **UEFI mode**. If you get an error, you booted in Legacy mode — reboot and select the UEFI entry for your USB.

Alternatively, check the firmware platform size:
```bash
cat /sys/firmware/efi/fw_platform_size
```
- `64` = 64-bit UEFI ✅
- `32` = 32-bit UEFI (rare, may limit bootloader options)

### Step 2: Connect to the Internet

**Option A: Ethernet (recommended)**
Wired connections work automatically. Verify with:
```bash
ip link
```
Look for `UP` on your Ethernet interface (e.g., `enp5s0`).

**Option B: Wi-Fi via iwctl**
```bash
iwctl
```
Inside the `iwctl` interactive prompt:
```
device list
station wlan0 scan
station wlan0 get-networks
station wlan0 connect YOUR_SSID
quit
```
Enter the Wi-Fi password when prompted.

**Verify connectivity:**
```bash
ping -c 3 archlinux.org
```

### Step 3: Synchronize the System Clock

Enable NTP time synchronization:
```bash
timedatectl set-ntp true
```

Verify:
```bash
timedatectl
```
The output should show `NTP service: active` and the correct UTC time.

## Verification

- [ ] `ls /sys/firmware/efi/efivars` lists files (UEFI mode confirmed)
- [ ] `ping archlinux.org` succeeds (internet connected)
- [ ] `timedatectl` shows NTP active

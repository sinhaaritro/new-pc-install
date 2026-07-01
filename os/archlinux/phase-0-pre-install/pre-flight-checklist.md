# Pre-Flight Checklist

> **Phase**: 0 — Pre-Install
> **Prerequisites**: [System Overview](./overview.md)
> **Packages**: None (done from Windows / BIOS)

---

## Overview

Before booting the Arch live USB, complete these steps to ensure a smooth installation. Skipping these can cause boot failures or data corruption on your Windows partition.

## Steps

### Step 1: Disable Secure Boot

1. Reboot your PC and enter the **BIOS/UEFI settings** (usually `DEL` or `F2` during POST).
2. Navigate to **Security** → **Secure Boot**.
3. Set Secure Boot to **Disabled**.
4. Save and exit.

> [!NOTE]
> Secure Boot can be re-enabled later after enrolling custom keys, but it's simpler to leave it off for a Hyprland setup.

### Step 2: Disable Fast Startup (Windows)

Fast Startup causes Windows to hibernate instead of fully shutting down, which leaves NTFS partitions in a dirty state. This can corrupt data if Linux tries to mount them.

1. In Windows, open **Control Panel** → **Power Options** → **Choose what the power buttons do**.
2. Click **Change settings that are currently unavailable**.
3. Uncheck **Turn on fast startup (recommended)**.
4. Click **Save changes**.

### Step 3: Prepare the USB Installer

1. Download the latest Arch Linux ISO from [archlinux.org/download](https://archlinux.org/download/).
2. Flash it to a USB drive using one of:
   - **Ventoy** (recommended) — Flash Ventoy once, then copy ISOs as files. Supports multiple ISOs on one USB.
   - **Rufus** (Windows) — Use **DD mode** (not ISO mode) when prompted.
   - **dd** (Linux/macOS) — `dd if=archlinux.iso of=/dev/sdX bs=4M status=progress`

> [!WARNING]
> **Rufus in ISO mode** can cause boot issues with Arch. Always select **DD mode** when Rufus asks.

### Step 4: Boot the USB in UEFI Mode

1. Reboot and enter the **boot menu** (usually `F12`, `F8`, or `F11` during POST).
2. Select the USB drive under the **UEFI** boot entries (not Legacy/CSM).
3. Select **Arch Linux install medium** from the bootloader menu.
4. You should land at a `root@archiso ~ #` prompt.

> [!IMPORTANT]
> If you only see Legacy/CSM entries for the USB, check that:
> - Secure Boot is disabled
> - CSM/Legacy Support is disabled in BIOS (force UEFI-only)
> - The USB was flashed correctly

### Step 5: Identify Your Drives

Before proceeding, note which drive is which:

```bash
lsblk -o NAME,SIZE,MODEL
```

For this guide's hardware:
| Drive | Role | Example Device |
|-------|------|---------------|
| **Samsung SSD** | Arch Linux installation target | `/dev/nvme1n1` |
| **WD SSD** | Windows (DO NOT TOUCH) | `/dev/nvme0n1` |

> [!CAUTION]
> **Write down your drive identifiers now.** Partitioning the wrong drive will destroy your Windows installation. Throughout this guide, replace `nvmeXn1` with your Samsung SSD's actual device name.

## Verification

You're ready when:
- [ ] Secure Boot is disabled
- [ ] Fast Startup is disabled in Windows
- [ ] USB is flashed and boots to the Arch live environment
- [ ] You know which drive is your Samsung SSD and which is your WD SSD

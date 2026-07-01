# Install Base Packages

> **Phase**: 1 — Base System
> **Prerequisites**: [Filesystems & Btrfs](./03-filesystems-and-btrfs.md)
> **Packages**: `base base-devel linux linux-headers linux-firmware amd-ucode btrfs-progs nano git`

---

## Overview

Install the base Arch Linux system onto the mounted partitions using `pacstrap`. This includes the kernel, firmware, AMD microcode, and essential tools.

## Steps

### Step 1: Select Mirrors (Optional but Recommended)

Update the mirror list for faster downloads using `reflector`:
```bash
reflector --country India --latest 5 --sort rate --save /etc/pacman.d/mirrorlist
```
*(Replace `India` with your country for optimal speeds)*

### Step 2: Upgrade Keyring

Ensure the latest package signing keys:
```bash
pacman -Sy archlinux-keyring
```

### Step 3: Install Essential Packages

```bash
pacstrap -K /mnt base base-devel linux linux-headers linux-firmware amd-ucode btrfs-progs nano git
```

#### Package Breakdown

| Package | Purpose |
|---------|---------|
| `base` | Minimal Arch Linux base (filesystem, systemd, glibc, etc.) |
| `base-devel` | Build tools (gcc, make, etc.) — needed for AUR packages later |
| `linux` | The Linux kernel |
| `linux-headers` | Kernel headers — needed for DKMS modules (NVIDIA) |
| `linux-firmware` | Firmware blobs for hardware devices |
| `amd-ucode` | AMD CPU microcode updates (Ryzen 9 9950X) |
| `btrfs-progs` | Btrfs filesystem utilities |
| `nano` | Simple text editor for configuration |
| `git` | Version control — needed for AUR and dotfiles |

> [!NOTE]
> Intel users would use `intel-ucode` instead of `amd-ucode`.

## Verification

The `pacstrap` command will download and install packages. It should complete without errors. If it fails, check your internet connection and mirror list.

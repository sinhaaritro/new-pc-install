# External Drives & NTFS

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/09-first-reboot.md)
> **Packages**: `ntfs-3g udisks2 udiskie`

---

## Overview

Mount NTFS drives (Windows partitions, external HDDs) and configure auto-mounting for removable media.

## Steps

### Step 1: Install Packages

```bash
sudo pacman -S ntfs-3g udisks2 udiskie
```

| Package | Purpose |
|---------|---------|
| `ntfs-3g` | NTFS read/write support |
| `udisks2` | Daemon for storage device management |
| `udiskie` | Auto-mount daemon for removable devices |

### Step 2: Identify Drives

```bash
lsblk -f
```

Note the UUID and filesystem type of each drive you want to mount.

### Step 3: Create Mount Points

Use `/mnt` for permanent mounts and `/media` for removable drives:

```bash
sudo mkdir /mnt/FOLDER_NAME
```

### Step 4: Configure fstab for Permanent Mounts

```bash
sudo nvim /etc/fstab
```

Add entries in the format:
```text
UUID=YOUR_UUID  /mnt/FOLDER_NAME  ntfs  defaults  0 0
```

Example:
```text
UUID=123456  /mnt/windows-data  ntfs  defaults  0 0
```

### Step 5: Configure Auto-Mount for Removable Media

Add `udiskie` to your Hyprland autostart (covered in [Phase 3: Hyprland Config](../phase-3-desktop/hyprland/02-core-config.md)):

```text
exec-once = udiskie &
```

### Step 6: Reboot

```bash
sudo reboot
```

## Verification

```bash
lsblk -f
# Permanent mounts should show mount points
# Plug in a USB drive — it should auto-mount under /media or /run/media
```

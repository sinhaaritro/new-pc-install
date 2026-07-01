# System Configuration

> **Phase**: 1 — Base System
> **Prerequisites**: [Install Base Packages](./04-install-base.md)
> **Packages**: `networkmanager`

---

## Overview

Generate the filesystem table, chroot into the new system, and configure timezone, locale, hostname, and networking.

## Steps

### Step 1: Generate fstab

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

Verify the entries are correct:
```bash
cat /mnt/etc/fstab
```

You should see entries for:
- 1 × EFI partition (`/boot/efi`)
- 1 × Swap (if created)
- 5 × Btrfs subvolumes (`/`, `/home`, `/.snapshots`, `/var/log`, `/var/cache/pacman/pkg`)

> [!IMPORTANT]
> Check that all subvolume entries include the correct mount options (`noatime,compress=zstd:3,ssd,space_cache=v2`). If any are wrong, edit the file manually before continuing.

### Step 2: Chroot into the New System

```bash
arch-chroot /mnt
```

You are now operating inside your new Arch installation.

### Step 3: Set Timezone

```bash
ln -sf /usr/share/zoneinfo/Region/City /etc/localtime
hwclock --systohc
```

*(Replace `Region/City` with your timezone. List available zones with `ls /usr/share/zoneinfo/`)*

### Step 4: Configure Locale

Edit the locale configuration:
```bash
nano /etc/locale.gen
```

Uncomment your preferred locale (e.g., find and uncomment `en_US.UTF-8 UTF-8`).

Generate the locales:
```bash
locale-gen
```

Set the system language:
```bash
echo "LANG=en_US.UTF-8" > /etc/locale.conf
```

### Step 5: Set Hostname

```bash
echo "archlinux" > /etc/hostname
```

*(Replace `archlinux` with your preferred hostname)*

### Step 6: Install and Enable NetworkManager

```bash
pacman -S networkmanager
systemctl enable NetworkManager
```

> [!NOTE]
> NetworkManager will handle both wired and wireless connections after reboot. Wi-Fi can be configured post-install via `nmcli` or a TUI tool.

## Verification

```bash
cat /etc/locale.conf   # Should show LANG=en_US.UTF-8
cat /etc/hostname       # Should show your hostname
systemctl is-enabled NetworkManager  # Should show "enabled"
```

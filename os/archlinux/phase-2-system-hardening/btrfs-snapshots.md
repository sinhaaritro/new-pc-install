# Btrfs Snapshots & Recovery

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/08-first-reboot.md)
> **Packages**: `snapper snap-pac grub-btrfs btrfs-assistant rsync`

---

## Overview

Configure **Snapper** for automatic pre/post upgrade snapshots, **grub-btrfs** for booting into snapshots from the GRUB menu, and a **pacman hook** to back up `/boot` before kernel updates.

This builds on the flat Btrfs subvolume layout created in [Phase 1: Filesystems](../phase-1-base-system/03-filesystems-and-btrfs.md).

## Reference

- [Arch Wiki: Snapper](https://wiki.archlinux.org/title/Snapper)
- [Arch Wiki: Btrfs](https://wiki.archlinux.org/title/Btrfs)

## Steps

### Step 1: Install Packages

```bash
sudo pacman -S snapper snap-pac grub-btrfs btrfs-assistant rsync
```

| Package | Purpose |
|---------|---------|
| `snapper` | Snapshot management daemon |
| `snap-pac` | Auto-creates pre/post snapshots on every `pacman` transaction |
| `grub-btrfs` | Adds snapshot entries to the GRUB boot menu |
| `btrfs-assistant` | GUI for managing Btrfs subvolumes and Snapper |
| `rsync` | Used by the boot backup hook |

### Step 2: Configure Snapper for Root (`/`)

Because we already mounted a custom `@snapshots` subvolume at `/.snapshots`, we need to configure Snapper to use it instead of creating its own.

```bash
# Unmount the existing subvolume temporarily
sudo umount /.snapshots

# Remove the empty mount point directory
sudo rmdir /.snapshots

# Generate a new Snapper configuration for root
sudo snapper -c root create-config /
```

> [!CAUTION]
> Snapper creates its own `.snapshots` subvolume during `create-config`. We need to delete it and remount our `@snapshots` subvolume instead.

```bash
# Delete Snapper's auto-created subvolume
sudo btrfs subvolume delete /.snapshots

# Recreate the mount point and remount from fstab
sudo mkdir /.snapshots
sudo mount -a

# Set correct permissions
sudo chmod 750 /.snapshots
```

> [!WARNING]
> Verify that `/.snapshots` is correctly mounted from fstab. Run `findmnt /.snapshots` — it should show the `@snapshots` subvolume.

### Step 3: Configure Snapper Permissions & Retention Policy

Edit the Snapper configuration:
```bash
sudo nvim /etc/snapper/configs/root
```

Modify or add the following settings:

```text
# Allow your user to access snapshots
ALLOW_USERS="username"

# Allow users of these groups to operate on this config and view snapshots
ALLOW_GROUPS="wheel"

# Sync ACLs so these groups have read access to the .snapshots directory
SYNC_ACL="yes"

# Retention policy (reduce from defaults to save space)
TIMELINE_MIN_AGE="1800"
TIMELINE_LIMIT_HOURLY="5"
TIMELINE_LIMIT_DAILY="7"
TIMELINE_LIMIT_WEEKLY="0"
TIMELINE_LIMIT_MONTHLY="0"
TIMELINE_LIMIT_YEARLY="0"
```

*(Replace `username` with your actual username)*

#### Granting Group Access (Alternative & Details)

By default, only root can access and manage snapper configurations. To grant access to users in specific system groups (like `sudo` or `wheel`), configure `ALLOW_GROUPS` and `SYNC_ACL`.

- **Command Line Alternative**:
  Instead of editing the file, you can apply these settings safely from the command line:
  ```bash
  sudo snapper -c root set-config "ALLOW_GROUPS=wheel sudo" SYNC_ACL="yes"
  ```
  *(Note: Group names are space-separated. For Arch Linux, `wheel` is typical; for Debian/Ubuntu, `sudo` is standard. Including both is safe).*

- **Why `SYNC_ACL="yes"` is necessary**:
  Setting `ALLOW_GROUPS` permits group members to run `snapper` commands (like listing snapshots). However, they won't be able to browse the physical `/.snapshots` directory to retrieve individual files unless `SYNC_ACL="yes"` is enabled. This setting instructs Snapper to automatically synchronize standard POSIX Access Control Lists (ACLs) onto the `/.snapshots` directory so that permitted groups can read the files within them.


### Step 4: Enable Snapper Timers

```bash
sudo systemctl enable --now snapper-timeline.timer
sudo systemctl enable --now snapper-cleanup.timer
```

| Timer | Purpose |
|-------|---------|
| `snapper-timeline.timer` | Creates hourly snapshots |
| `snapper-cleanup.timer` | Deletes old snapshots based on retention policy |

### Step 5: Enable Read-Write Snapshot Booting

To boot into snapshots as read-write (so you can actually fix things), add `grub-btrfs-overlay` to mkinitcpio hooks.

```bash
sudo nvim /etc/mkinitcpio.conf
```

Find the `HOOKS=(...)` line and add `grub-btrfs-overlayfs` at the end:
```text
HOOKS=(base udev autodetect microcode modconf keyboard keymap consolefont block filesystems fsck grub-btrfs-overlayfs)
```

Regenerate initramfs:
```bash
sudo mkinitcpio -P
```

### Step 6: Create Boot Backup Hook

This pacman hook backs up `/boot` before any kernel update, so you can recover even if a kernel update breaks boot.

```bash
sudo mkdir -p /etc/pacman.d/hooks
sudo nvim /etc/pacman.d/hooks/50-bootbackup.hook
```

Paste the following:
```ini
[Trigger]
Operation=Install
Operation=Upgrade
Operation=Remove
Type=Path
Target=boot/*

[Action]
Depends=rsync
Description=Backing up /boot
When=PreTransaction
Exec=/usr/bin/rsync -a --delete /boot /.bootbackup
```

## How Snapshots Work Now

1. **Before and After Upgrades**: `snap-pac` automatically creates a "pre" and "post" snapshot every time you run `sudo pacman -S` or `sudo pacman -Syu`.
2. **Hourly Timeline Snapshots**: `snapper-timeline.timer` creates hourly snapshots, cleaned up by the retention policy.
3. **GRUB Boot Menu**: `grub-btrfs` adds an "Arch Linux Snapshots" submenu to GRUB. If an update breaks your system, reboot → select a snapshot → boot into it → rollback.
4. **Boot Backup**: The `50-bootbackup.hook` rsyncs `/boot` to `/.bootbackup` before kernel updates.

## Verification

```bash
# List snapshots
sudo snapper -c root list

# Check timers are active
systemctl status snapper-timeline.timer
systemctl status snapper-cleanup.timer

# Verify boot backup location exists after next pacman transaction
ls /.bootbackup
```

## Recovery Usage

When you need to rollback:

1. Reboot and select **Arch Linux Snapshots** from GRUB
2. Choose the snapshot to boot into
3. Once booted into the snapshot, use Snapper to rollback:
   ```bash
   sudo snapper -c root undochange SNAPSHOT_NUMBER..0
   ```
4. Reboot normally

> [!TIP]
> `btrfs-assistant` provides a GUI for browsing and restoring snapshots if you prefer a visual interface.

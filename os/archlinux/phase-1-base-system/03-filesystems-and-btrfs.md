# Filesystems & Btrfs Subvolumes

> **Phase**: 1 — Base System
> **Prerequisites**: [Partitioning](./02-partitioning.md)
> **Packages**: `btrfs-progs` (installed via pacstrap in the next step)

---

## Overview

Format your partitions and create a **flat Btrfs subvolume layout** optimized for Snapper snapshots. This layout prevents snapshots from nesting recursively and keeps logs, caches, and package files separate from rollback-able system data.

## Steps

### Step 1: Format the EFI Partition

```bash
mkfs.fat -F 32 /dev/nvmeXn1p1
```

### Step 2: Initialize Swap (if created)

If you created a swap partition:
```bash
mkswap /dev/nvmeXn1p2
swapon /dev/nvmeXn1p2
```

### Step 3: Format the Root Partition to Btrfs

```bash
mkfs.btrfs -L ARCH /dev/nvmeXn1pN
```
*(Replace `pN` with `p2` if no swap, or `p3` if swap was created)*

### Step 4: Create Btrfs Subvolumes

Mount the root Btrfs filesystem temporarily:
```bash
mount /dev/nvmeXn1pN /mnt
```

Create the flat subvolume layout:
```bash
btrfs subvolume create /mnt/@
btrfs subvolume create /mnt/@home
btrfs subvolume create /mnt/@snapshots
btrfs subvolume create /mnt/@var_log
btrfs subvolume create /mnt/@pkg
```

> [!TIP]
> **Short forms:** `btrfs su cr` = `btrfs subvolume create`, `btrfs su li` = `btrfs subvolume list`

Verify the subvolumes:
```bash
btrfs subvolume list /mnt
```

Unmount:
```bash
umount /mnt
```

#### Subvolume Purposes

| Subvolume | Mount Point | Why Separate |
|-----------|-------------|-------------|
| `@` | `/` | Main root — snapshotted by Snapper |
| `@home` | `/home` | User data — excluded from root snapshots |
| `@snapshots` | `/.snapshots` | Snapper snapshot storage |
| `@var_log` | `/var/log` | Logs — excluded (would bloat snapshots) |
| `@pkg` | `/var/cache/pacman/pkg` | Package cache — excluded (large, re-downloadable) |

### Step 5: Mount Subvolumes with Optimal Options

Mount the root subvolume first:
```bash
mount -o noatime,compress=zstd:3,ssd,space_cache=v2,subvol=@ /dev/nvmeXn1pN /mnt
```

Create mount point directories:
```bash
mkdir -p /mnt/{boot/efi,home,.snapshots,var/log,var/cache/pacman/pkg}
```

Mount the remaining subvolumes:
```bash
mount -o noatime,compress=zstd:3,ssd,space_cache=v2,subvol=@home /dev/nvmeXn1pN /mnt/home
mount -o noatime,compress=zstd:3,ssd,space_cache=v2,subvol=@snapshots /dev/nvmeXn1pN /mnt/.snapshots
mount -o noatime,compress=zstd:3,ssd,space_cache=v2,subvol=@var_log /dev/nvmeXn1pN /mnt/var/log
mount -o noatime,compress=zstd:3,ssd,space_cache=v2,subvol=@pkg /dev/nvmeXn1pN /mnt/var/cache/pacman/pkg
```

Mount the EFI partition:
```bash
mount /dev/nvmeXn1p1 /mnt/boot/efi
```

#### Mount Options Explained

| Option | Purpose |
|--------|---------|
| `noatime` | Don't update access times — reduces SSD writes |
| `compress=zstd:3` | Transparent ZSTD compression (level 3) — saves space, extends SSD lifespan |
| `ssd` | Enables SSD-specific optimizations in Btrfs |
| `space_cache=v2` | Improved free-space tracking for performance |

## Verification

```bash
lsblk
```

You should see all subvolumes mounted at their correct locations, plus the EFI partition at `/mnt/boot/efi`.

```bash
findmnt -t btrfs
```

This should show 5 Btrfs mount entries with the correct subvolume names and mount options.

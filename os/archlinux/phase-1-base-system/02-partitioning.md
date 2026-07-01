# Partitioning

> **Phase**: 1 — Base System
> **Prerequisites**: [Verify Boot & Network](./01-verify-boot-and-network.md)
> **Packages**: None (gdisk is included in the live environment)

---

## Overview

Partition your **Samsung SSD** for Arch Linux. This creates an EFI System Partition and a root partition. Swap is optional but recommended.

> [!CAUTION]
> **Do NOT partition your WD SSD** — that contains Windows. Double-check drive identifiers with `lsblk` before proceeding.

## Steps

### Step 1: Identify Your Target Drive

```bash
lsblk -o NAME,SIZE,MODEL
```

Locate your Samsung SSD (e.g., `/dev/nvme1n1`). Throughout this guide, replace `/dev/nvmeXn1` with your actual device name.

### Step 2: Open gdisk

```bash
gdisk /dev/nvmeXn1
```

Key commands inside `gdisk`:
- **`p`**: Print current partition table
- **`o`**: Create a new empty GPT partition table
- **`n`**: Create a new partition
- **`d`**: Delete a partition
- **`w`**: Write changes and exit

### Step 3: Create Partition Table

Type `o` and press Enter to create a new GPT partition table.

> [!WARNING]
> This erases all existing partitions on the drive. Confirm you have the right device.

### Step 4: Create EFI System Partition

Type `n` to create a new partition:
- **Partition number**: `1`
- **First sector**: Press Enter (default)
- **Last sector**: `+2G` (2 GB — recommended for dual-boot with multiple kernels)
- **Hex code**: `ef00` (EFI System Partition)

### Step 5: Create Swap Partition (Optional, Recommended)

> [!NOTE]
> **Swap sizing**: Match your RAM size (e.g., `+64G` for 64 GB RAM). Needed for hibernation. On systems with 64GB+ RAM, swap is optional for normal use — you may skip this step.

Type `n` to create a new partition:
- **Partition number**: `2`
- **First sector**: Press Enter (default)
- **Last sector**: `+64G` (or your RAM size, or skip this step entirely)
- **Hex code**: `8200` (Linux swap)

### Step 6: Create Root Partition

Type `n` to create a new partition:
- **Partition number**: `3` (or `2` if you skipped swap)
- **First sector**: Press Enter (default)
- **Last sector**: Press Enter (uses all remaining space)
- **Hex code**: `8300` (Linux filesystem)

### Step 7: Verify and Write

Type `p` to verify your partition layout looks correct:

**With swap:**
| # | Size | Type | Code |
|---|------|------|------|
| 1 | 2 GB | EFI System | EF00 |
| 2 | 64 GB | Linux swap | 8200 |
| 3 | Remaining | Linux filesystem | 8300 |

**Without swap:**
| # | Size | Type | Code |
|---|------|------|------|
| 1 | 2 GB | EFI System | EF00 |
| 2 | Remaining | Linux filesystem | 8300 |

Type `w` to write changes to disk and exit.

## Verification

```bash
lsblk
```

You should see your Samsung SSD with 2 or 3 partitions matching the layout above.

> [!TIP]
> Note down your partition names (e.g., `nvmeXn1p1`, `nvmeXn1p2`, `nvmeXn1p3`). You'll need them in the next step.

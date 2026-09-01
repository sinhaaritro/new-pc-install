# Phase 1: Base System

> **Milestone**: Bootable CLI-only Arch Linux with dual-boot GRUB, Btrfs subvolumes, and user account.
> **Prerequisite**: Complete [Phase 0: Pre-Install](../phase-0-pre-install/README.md).

## Modules (Sequential — Follow in Order)

| # | Module | Required | Depends On | Notes |
|---|--------|----------|------------|-------|
| 1 | [Verify Boot & Network](./01-verify-boot-and-network.md) | ✅ Required | Phase 0 | UEFI check, internet, clock |
| 2 | [Partitioning](./02-partitioning.md) | ✅ Required | #1 | EFI + optional swap + root |
| 3 | [Filesystems & Btrfs](./03-filesystems-and-btrfs.md) | ✅ Required | #2 | Subvolumes + mount options |
| 4 | [Install Base](./04-install-base.md) | ✅ Required | #3 | pacstrap base system |
| 5 | [System Config](./05-system-config.md) | ✅ Required | #4 | fstab, chroot, locale, hostname |
| 6 | [Users & Sudo](./06-users-and-sudo.md) | ✅ Required | #5 | User account + wheel group |
| 7 | [GPU (NVIDIA)](./07-gpu-nvidia.md) | ⚡ Recommended | #6 | NVIDIA driver in chroot (KMS, mkinitcpio, hook) — must precede #8 |
| 8 | [Bootloader (GRUB)](./08-bootloader-grub.md) | ✅ Required | #7 | GRUB + os-prober dual-boot |
| 9 | [First Reboot](./09-first-reboot.md) | ✅ Required | #8 | Exit chroot, reboot, verify |

> [!IMPORTANT]
> Phase 1 is strictly sequential. Follow modules 1 through 8 in order.

## What's Next

After first reboot, proceed to [Phase 2: System Hardening](../phase-2-system-hardening/README.md).

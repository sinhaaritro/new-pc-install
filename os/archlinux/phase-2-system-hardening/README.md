# Phase 2: System Hardening

> **Milestone**: Stable system with automatic snapshots, audio, and network tools.
> **Prerequisite**: Complete [Phase 1: Base System](../phase-1-base-system/README.md) (specifically, [First Reboot](../phase-1-base-system/09-first-reboot.md)).
>
> The NVIDIA driver is installed in Phase 1 ([GPU (NVIDIA)](../phase-1-base-system/07-gpu-nvidia.md)), in the chroot.

## Modules (Flexible Order — Unless Noted)

| # | Module | Required | Depends On | Notes |
|---|--------|----------|------------|-------|
| 1 | [Btrfs Snapshots](./btrfs-snapshots.md) | ⚡ Recommended | First Reboot | Snapper + snap-pac + grub-btrfs |
| 2 | [AUR Helper (yay)](./aur-helper.md) | ⚡ Recommended | First Reboot | Needed for AUR packages in later phases |
| 3 | [Sound (PipeWire)](./sound-pipewire.md) | ⚡ Recommended | First Reboot | Audio stack — needed for screen sharing later |
| 4 | [Wi-Fi & Bluetooth](./networking.md) | 💡 Optional | First Reboot | Skip if using only Ethernet |
| 5 | [Clock Sync](./clock-sync.md) | 💡 Optional | First Reboot | Only needed for dual-boot systems |
| 6 | [Firewall](./firewall.md) | 💡 Optional | First Reboot | ufw basic rules |
| 7 | [External Drives](./external-drives.md) | 💡 Optional | First Reboot | NTFS, auto-mount |
| 8 | [SSH & Git](./ssh.md) | ⚡ Recommended | First Reboot | SSH keys, GitHub, git config |

> [!TIP]
> Recommended order: **Snapshots → AUR → Sound → SSH**, then optional modules as needed.

## What's Next

After setting up snapshots and an AUR helper (at minimum), proceed to [Phase 3: Desktop](../phase-3-desktop/README.md).

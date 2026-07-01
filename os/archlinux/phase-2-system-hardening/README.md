# Phase 2: System Hardening

> **Milestone**: Stable system with GPU drivers, automatic snapshots, audio, and network tools.
> **Prerequisite**: Complete [Phase 1: Base System](../phase-1-base-system/README.md) (specifically, [First Reboot](../phase-1-base-system/08-first-reboot.md)).

## Modules (Flexible Order — Unless Noted)

| # | Module | Required | Depends On | Notes |
|---|--------|----------|------------|-------|
| 1 | [NVIDIA Drivers](./nvidia-drivers.md) | ⚡ Recommended | First Reboot | **Do this first** — needed for Phase 3 (Hyprland) |
| 2 | [Btrfs Snapshots](./btrfs-snapshots.md) | ⚡ Recommended | First Reboot | Snapper + snap-pac + grub-btrfs |
| 3 | [AUR Helper (yay)](./aur-helper.md) | ⚡ Recommended | First Reboot | Needed for AUR packages in later phases |
| 4 | [Sound (PipeWire)](./sound-pipewire.md) | ⚡ Recommended | First Reboot | Audio stack — needed for screen sharing later |
| 5 | [Wi-Fi & Bluetooth](./networking.md) | 💡 Optional | First Reboot | Skip if using only Ethernet |
| 6 | [Clock Sync](./clock-sync.md) | 💡 Optional | First Reboot | Only needed for dual-boot systems |
| 7 | [Firewall](./firewall.md) | 💡 Optional | First Reboot | ufw basic rules |
| 8 | [External Drives](./external-drives.md) | 💡 Optional | First Reboot | NTFS, auto-mount |
| 9 | [SSH & Git](./ssh.md) | ⚡ Recommended | First Reboot | SSH keys, GitHub, git config |

> [!TIP]
> Recommended order: **NVIDIA → Snapshots → AUR → Sound → SSH**, then optional modules as needed.

## What's Next

After setting up NVIDIA drivers (at minimum), proceed to [Phase 3: Desktop](../phase-3-desktop/README.md).

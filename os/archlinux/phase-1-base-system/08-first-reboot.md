# First Reboot

> **Phase**: 1 — Base System
> **Prerequisites**: [Bootloader (GRUB)](./07-bootloader-grub.md)
> **Packages**: None

---

## Overview

Exit the chroot environment, unmount all partitions, and reboot into your new Arch Linux installation. After this, Phase 1 is complete — you have a **bootable CLI-only Arch Linux system**.

## Steps

### Step 1: Exit Chroot

```bash
exit
```

### Step 2: Unmount All Partitions

```bash
umount -R /mnt
```

### Step 3: Reboot

```bash
reboot
```

**Remove your USB installer** when the system powers off / during POST.

### Step 4: GRUB Menu

You should see the GRUB boot menu with:
- **Arch Linux** (default)
- **Windows Boot Manager**

Select **Arch Linux** and press Enter.

### Step 5: Log In

Log in with your **user account** (the one created in [Users & Sudo](./06-users-and-sudo.md)), not root.

```
archlinux login: username
Password: ********
```

### Step 6: Verify System State

```bash
# Verify internet
ping -c 3 archlinux.org

# If no internet, start NetworkManager manually (should be enabled):
sudo systemctl start NetworkManager
nmcli device status

# Verify Btrfs subvolumes are mounted
findmnt -t btrfs

# Verify UEFI boot
ls /sys/firmware/efi
```

## Verification

✅ **Phase 1 Complete** — You have a bootable Arch Linux system with:
- [x] UEFI boot via GRUB
- [x] Dual-boot with Windows
- [x] Btrfs root with flat subvolume layout
- [x] User account with sudo access
- [x] NetworkManager for connectivity
- [x] AMD microcode loaded

**Next**: Proceed to [Phase 2: System Hardening](../phase-2-system-hardening/README.md)

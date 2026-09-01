# GPU (NVIDIA)

> **Phase**: 1 — Base System
> **Prerequisites**: [Users & Sudo](./06-users-and-sudo.md) — but must be completed **before** [Bootloader (GRUB)](./08-bootloader-grub.md) (the GRUB cmdline edit must land before `grub-mkconfig` runs)
> **Packages**: `nvidia-open nvidia-utils lib32-nvidia-utils nvidia-settings` (base driver selected by `nvidia_driver`: `nvidia-open` for Turing+ / `nvidia` for Maxwell–Pascal)

---

## Overview

Install the NVIDIA open kernel module (`nvidia-open`) for your RTX 4070 Ti Super (Ada Lovelace), enable Kernel Mode Setting (KMS) for Wayland/Hyprland, and set up automatic initramfs regeneration via a pacman hook.

> [!IMPORTANT]
> This module runs **inside the chroot on the live USB**, between Users & Sudo and the Bootloader. Every command below is prefixed with `arch-chroot /mnt` — you are configuring the new system while still on the installer.

> [!NOTE]
> `nvidia-open` is NVIDIA's open-source kernel module, recommended for Turing (RTX 20xx) and newer. It is **not** the same as `nouveau` (the community reverse-engineered driver).

## Reference

- [Arch Wiki: NVIDIA](https://wiki.archlinux.org/title/NVIDIA)
- [NVIDIA Driver Table (CodeNames)](https://nouveau.freedesktop.org/CodeNames.html)

## Steps

### Step 1: Enable multilib Repository

The 32-bit compatibility libraries (`lib32-nvidia-utils`) are in the `[multilib]` repository, which is disabled by default.

```bash
arch-chroot /mnt nano /etc/pacman.conf
```

Find and uncomment both lines:
```text
[multilib]
Include = /etc/pacman.d/mirrorlist
```

> [!NOTE]
> No `pacman -Syu` is needed here — the chroot database is fresh from `pacstrap`, and the next step installs directly.

### Step 2: Install Driver Packages

```bash
arch-chroot /mnt pacman -S --noconfirm nvidia-open nvidia-utils lib32-nvidia-utils nvidia-settings
```

#### Driver Selection Reference

| GPU Generation | Kernel | Base Driver | OpenGL | OpenGL (multilib) |
|---|---|---|---|---|
| **Turing (RTX 20xx) and newer** | linux | `nvidia-open` | `nvidia-utils` | `lib32-nvidia-utils` |
| **Turing and newer** | any other kernel | `nvidia-open-dkms` | `nvidia-utils` | `lib32-nvidia-utils` |
| **Maxwell–Ada Lovelace** | linux | `nvidia` | `nvidia-utils` | `lib32-nvidia-utils` |
| **Maxwell–Ada Lovelace** | any other kernel | `nvidia-dkms` | `nvidia-utils` | `lib32-nvidia-utils` |

### Step 3: Add NVIDIA Parameters to GRUB Cmdline

To enable early Kernel Mode Setting (KMS) and improve framebuffer TTY support, append the NVIDIA parameters to `GRUB_CMDLINE_LINUX_DEFAULT`.

1. Open `/etc/default/grub` in the new system:
   ```bash
   arch-chroot /mnt nano /etc/default/grub
   ```

2. Find the `GRUB_CMDLINE_LINUX_DEFAULT` line and append the parameters:
   ```text
   GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet nvidia_drm.modeset=1 nvidia_drm.fbdev=1"
   ```

> [!NOTE]
> Do **not** run `grub-mkconfig` here — the Bootloader module (next) generates `grub.cfg` after this cmdline edit, so the parameters are picked up automatically.

### Step 4: Early Loading of NVIDIA Modules

Edit `mkinitcpio.conf` in the new system:
```bash
arch-chroot /mnt nano /etc/mkinitcpio.conf
```

**4a.** Find the `MODULES=()` line and add the NVIDIA modules:
```text
MODULES=(... nvidia nvidia_modeset nvidia_uvm nvidia_drm ...)
```

**4b.** Find the `HOOKS=(...)` line and **remove** the word `kms`:
```text
# Before:
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block filesystems fsck)

# After:
HOOKS=(base udev autodetect microcode modconf keyboard keymap consolefont block filesystems fsck)
```

> [!IMPORTANT]
> Removing `kms` from HOOKS prevents the default (non-NVIDIA) KMS from loading, which would conflict with the NVIDIA early-load modules.

**4c.** Regenerate the initramfs:
```bash
arch-chroot /mnt mkinitcpio -P
```

### Step 5: Add Pacman Hook for Automatic Initramfs Rebuild

When NVIDIA drivers or the kernel are updated later, the initramfs must be regenerated. This hook automates that.

Create the hooks directory in the new system:
```bash
arch-chroot /mnt mkdir -p /etc/pacman.d/hooks/
```

Create the hook file:
```bash
arch-chroot /mnt nano /etc/pacman.d/hooks/nvidia.hook
```

Paste the following:
```ini
[Trigger]
Operation=Install
Operation=Upgrade
Operation=Remove
Type=Package
# Match your base driver package
Target=nvidia-open
# Match your kernel package
Target=linux

[Action]
Description=Update Nvidia module in initcpio
Depends=mkinitcpio
When=PostTransaction
NeedsTargets
Exec=/bin/sh -c 'while read -r trg; do case $trg in linux) exit 0; esac; done; /usr/bin/mkinitcpio -P'
```

## Verification

The driver cannot be verified until the first boot (no GPU access from the live USB for the installed system). After the first reboot, verify:

```bash
nvidia-smi
```

You should see your RTX 4070 Ti Super listed with the correct driver version.

```bash
lsmod | grep nvidia
```

Should show `nvidia`, `nvidia_modeset`, `nvidia_uvm`, `nvidia_drm` loaded.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `nvidia-smi` shows "command not found" | `nvidia-utils` not installed — `sudo pacman -S nvidia-utils` |
| Black screen after reboot | Boot from USB, chroot, check `mkinitcpio.conf` for typos |
| `nvidia-smi` shows "No devices found" | Check `MODULES` array in `mkinitcpio.conf`, re-run `mkinitcpio -P` |
| Screen tearing | Verify `nvidia_drm.modeset=1` is in GRUB cmdline |

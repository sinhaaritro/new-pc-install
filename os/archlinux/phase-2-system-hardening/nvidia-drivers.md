# NVIDIA Drivers

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/08-first-reboot.md)
> **Packages**: `nvidia-open nvidia-utils lib32-nvidia-utils nvidia-settings`

---

## Overview

Install the proprietary NVIDIA open kernel module (`nvidia-open`) for your RTX 4070 Ti Super (Ada Lovelace), enable Kernel Mode Setting (KMS) for Wayland/Hyprland, and set up automatic initramfs regeneration via a pacman hook.

> [!NOTE]
> `nvidia-open` is NVIDIA's open-source kernel module, recommended for Turing (RTX 20xx) and newer. It is **not** the same as `nouveau` (the community reverse-engineered driver).

## Reference

- [Arch Wiki: NVIDIA](https://wiki.archlinux.org/title/NVIDIA)
- [NVIDIA Driver Table (CodeNames)](https://nouveau.freedesktop.org/CodeNames.html)

## Steps

### Step 1: Enable multilib Repository

The 32-bit compatibility libraries (`lib32-nvidia-utils`) are in the `[multilib]` repository, which is disabled by default.

```bash
sudo nvim /etc/pacman.conf
```

Find and uncomment both lines:
```text
[multilib]
Include = /etc/pacman.d/mirrorlist
```

Update the package database:
```bash
sudo pacman -Syu
```

### Step 2: Install Driver Packages

```bash
sudo pacman -S nvidia-open nvidia-utils lib32-nvidia-utils nvidia-settings
```

#### Driver Selection Reference

| GPU Generation | Kernel | Base Driver | OpenGL | OpenGL (multilib) |
|---|---|---|---|---|
| **Turing (RTX 20xx) and newer** | linux | `nvidia-open` | `nvidia-utils` | `lib32-nvidia-utils` |
| **Turing and newer** | any other kernel | `nvidia-open-dkms` | `nvidia-utils` | `lib32-nvidia-utils` |
| **Maxwell–Ada Lovelace** | linux | `nvidia` | `nvidia-utils` | `lib32-nvidia-utils` |
| **Maxwell–Ada Lovelace** | any other kernel | `nvidia-dkms` | `nvidia-utils` | `lib32-nvidia-utils` |

### Step 3: Configure Kernel Parameters (GRUB)

To enable early Kernel Mode Setting (KMS) and improve framebuffer TTY support, add the NVIDIA parameters to your GRUB configuration:

1. Open `/etc/default/grub` in your editor:
   ```bash
   sudo nvim /etc/default/grub
   ```

2. Find the `GRUB_CMDLINE_LINUX_DEFAULT` line and append the parameters:
   ```text
   GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 quiet nvidia_drm.modeset=1 nvidia_drm.fbdev=1"
   ```

3. Regenerate the GRUB configuration:
   
   > [!WARNING]
   > Since your Windows installation is on a separate drive (the WD SSD), **you must temporarily mount the Windows EFI partition before running `grub-mkconfig`**. Refer to [Phase 1 Bootloader: Step 3](../phase-1-base-system/07-bootloader-grub.md#step-3-mount-windows-efi-partition-for-os-prober) for the exact mounting steps. If you do not mount it, `os-prober` will not detect Windows, and you will lose the Windows entry in your GRUB menu.

   ```bash
   # Mount the Windows EFI partition first (see Phase 1 Bootloader: Step 3), then run:
   sudo grub-mkconfig -o /boot/grub/grub.cfg
   ```

### Step 4: Early Loading of NVIDIA Modules

Edit `mkinitcpio.conf`:
```bash
sudo nvim /etc/mkinitcpio.conf
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
sudo mkinitcpio -P
```

### Step 5: Add Pacman Hook for Automatic Initramfs Rebuild

When NVIDIA drivers or the kernel are updated, the initramfs must be regenerated. This hook automates that.

Create the hooks directory:
```bash
sudo mkdir -p /etc/pacman.d/hooks/
```

Create the hook file:
```bash
sudo nvim /etc/pacman.d/hooks/nvidia.hook
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

### Step 6: Reboot

```bash
sudo reboot
```

## Verification

After reboot, verify the driver is loaded:

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

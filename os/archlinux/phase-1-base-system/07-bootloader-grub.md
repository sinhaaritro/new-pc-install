# Bootloader (GRUB) & Dual-Boot

> **Phase**: 1 — Base System
> **Prerequisites**: [Users & Sudo](./06-users-and-sudo.md)
> **Packages**: `grub efibootmgr os-prober mtools dosfstools`

---

## Overview

Install GRUB as the bootloader and configure `os-prober` to detect your Windows installation for a dual-boot setup. The EFI partition is mounted at `/boot/efi`, keeping kernel images on the Btrfs root (snapshotable by Snapper).

## Steps

### Step 1: Install GRUB Packages

```bash
pacman -S grub efibootmgr os-prober mtools dosfstools
```

### Step 2: Configure GRUB for Dual-Boot

Open `/etc/default/grub` in your editor:
```bash
nano /etc/default/grub
```

Enable `os-prober` to detect your Windows installation. Find and uncomment (or add) this line at the bottom of the file:
```text
GRUB_DISABLE_OS_PROBER=false
```

Save and exit.

### Step 3: Mount Windows EFI Partition (for os-prober)

To allow `os-prober` to detect your Windows installation, its EFI partition must be mounted when generating the GRUB config.

Identify the Windows EFI partition on your WD SSD:
```bash
lsblk -o NAME,FSTYPE,SIZE,LABEL
```

It's typically a small FAT32 partition (~100–500 MB) on your WD SSD (e.g., `/dev/nvme0n1p1`).

Mount it temporarily:
```bash
mkdir -p /tmp/win_efi
mount /dev/nvmeYn1pX /tmp/win_efi
```

*(Replace `/dev/nvmeYn1pX` with your Windows EFI partition)*

### Step 4: Install GRUB to the EFI Partition

```bash
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --removable
```

| Flag | Purpose |
|------|---------|
| `--target=x86_64-efi` | Install for 64-bit UEFI |
| `--efi-directory=/boot/efi` | Location of the EFI System Partition |
| `--bootloader-id=GRUB` | Name shown in BIOS boot menu |
| `--removable` | Creates a fallback bootloader payload (highly recommended for UEFI portability/stability) |

### Step 5: Generate GRUB Configuration

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

**Check the output for both:**
- `Found Linux image: /boot/vmlinuz-linux` ✅
- `Found Windows Boot Manager on /dev/nvmeYn1pX` ✅

> [!WARNING]
> If Windows is not detected:
> 1. Verify the Windows EFI partition is mounted (`mount | grep win_efi`)
> 2. Verify `GRUB_DISABLE_OS_PROBER=false` is set in `/etc/default/grub`
> 3. Re-run `grub-mkconfig -o /boot/grub/grub.cfg`

### Step 6: Clean Up

Unmount the Windows EFI partition:
```bash
umount /tmp/win_efi
```

## Verification

```bash
cat /boot/grub/grub.cfg | grep -i windows
```

This should show a `menuentry` for Windows Boot Manager.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| GRUB doesn't appear at boot | Enter BIOS, change boot order to prioritize `GRUB` |
| Windows not in GRUB menu | Re-mount Windows EFI, re-run `grub-mkconfig` |
| `grub-install` fails with "cannot find EFI directory" | Verify `/boot/efi` is mounted (`mount | grep efi`) |

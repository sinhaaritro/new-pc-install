# Arch Linux Installation Guide

# Pre-installation

## Setup and Boot to Live Environment

1. **Download the ISO**:
   - Visit [Arch Linux Download](https://archlinux.org/download/) and download the latest **ISO file**.
2. **Flash the ISO**:
   - Use tools like **memtest86's ISO burner** to flash the ISO to a USB.
3. **Restart the PC**:
   - Boot using the USB.

## Verify the Boot Mode

Check if the system is running in **UEFI mode**:
```bash
cat /sys/firmware/efi/fw_platform_size
```

## Connect to the Internet and Synchronize Clock

1. Verify an active internet connection:
   ```bash
   ip link
   ```
   - Look for `UP` on one of the interfaces.
2. Synchronize the system clock:
   ```bash
   timedatectl
   ```

---

# Partition
**Partitioning** is done using `gdisk`:

1. Identify the target device:
   ```bash
   lsblk
   ```
   - Usually named **sdc**, **sdd**, etc.
2. Assume the device name is `sdz` (replace `sdz` with the actual device name):
   ```bash
   gdisk /dev/sdz
   ```
3. Key commands in `gdisk`:
   - **`p`**: Print partition details.
   - **`d`**: Delete a partition.
   - **`n`**: Create a new partition.
   - **`w`**: Write changes to disk.
4. Steps to partition:
   - **Delete all partitions** using `d`.
   - **Create new partitions**:
     - **Boot Partition**: 2GB, type **EF00**.
     - **Swap Partition**: 5GB (or 1.5x the total RAM), type **8200**.
     - **Root Partition**: Remaining space, type **8300**.
   - Verify partitions with `p`.
   - Save changes with `w`.

---

# Format

**Assume** the following partitions:
- `sdz1`: **EFI system partition**
- `sdz2`: **Swap partition**
- `sdz3`: **Root partition**

Commands to format:

1. Format the **root partition** with Btrfs:
   ```bash
   mkfs.btrfs /dev/sdz3
   ```
2. Format the **swap partition**:
   ```bash
   mkswap /dev/sdz2
   ```
3. Format the **EFI partition**:
   ```bash
   mkfs.fat -F 32 /dev/sdz1
   ```
4. Verify partition sizes:
   ```bash
   lsblk
   ```

---

# Mount disk
> [!NOTE]
> When using BTRFS for `root_partition` look at the recovery guide to properly set up BTRFS snapshots with snapper

1. Mount the **root partition**:
   ```bash
   mount /dev/sdz3 /mnt
   ```
2. Enable swap:
   ```bash
   swapon /dev/sdz2
   ```
3. Mount the **EFI partition**:
   ```bash
   mount --mkdir /dev/sdz1 /mnt/boot/efi
   ```
4. Verify mount points:
   ```bash
   lsblk
   ```

---

# Installation
## Select Mirrors

Update the mirror list using `reflector`:
```bash
reflector --country India --latest 5 --sort rate --save /etc/pacman.d/mirrorlist
```

## Upgrade Keyring

Ensure the latest keyring:
```bash
pacman -Sy archlinux-keyring
```

## Install Essential Packages

Install the required packages:
```bash
pacstrap -K /mnt linux linux-firmware base base-devel networkmanager amd-ucode neovim man-db man-pages
```

---

# Configure the system
## Fstab and Chroot

1. Generate the **fstab file**:
   ```bash
   genfstab -U /mnt >> /mnt/etc/fstab
   ```
2. Verify entries in `fstab`:
   ```bash
   cat /mnt/etc/fstab
   ```
3. Change root to the new system:
   ```bash
   arch-chroot /mnt
   ```

## Time, Clock, and Network Configuration

1. Set the timezone:
   ```bash
   ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
   ```
2. Synchronize hardware clock:
   ```bash
   hwclock --systohc
   ```
3. Set the hostname:
   ```bash
   echo "ArchUSB64" >> /etc/hostname
   ```
4. Edit the hosts file as required.

## Localization

1. Edit the locale configuration:
   ```bash
   nvim /etc/locale.gen
   ```
   - Find and uncomment the **US locale** line (e.g., `en_US.UTF-8`).
2. Generate the locale:
   ```bash
   locale-gen
   ```
3. Set the language environment variable:
   ```bash
   echo "LANG=en_US.UTF-8" >> /etc/locale.conf
   ```
4. Verify the language settings:
   ```bash
   cat /etc/locale.conf
   ```

### Install Bootloader

1. Install GRUB and related packages:
   ```bash
   pacman -S grub efibootmgr
   ```
2. Install GRUB for UEFI:
   ```bash
   grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --removable
   ```
3. Generate GRUB configuration:
   ```bash
   grub-mkconfig -o /boot/grub/grub.cfg
   ```

---

## Restart

1. Exit the chroot environment:
   ```bash
   exit
   ```
2. Unmount all partitions:
   ```bash
   umount -R /mnt
   ```
3. Restart the system:
   ```bash
   reboot
   ```

Remove the live environment and boot into your new Arch Linux system!

# Pre-installation
## Setup and boot to live environment
1. Goto https://archlinux.org/download/ and download the latest ISO file
2. Flash the ISO in the USB. Can use memtest86's iso burner.
3. Restart the PC. Boot with the USB
## Verify the boot mode
Check if the system is UEFI (mine is UEFI)
```bash
cat /sys/firmware/efi/fw_platform_size
```
## Connect to the internet and clock
Check if there is `UP` on one of the internet connection
```bash
ip link
```
Use timedatectl to ensure the system clock is synchronized
```bash
timedatectl
```
## Partition
Partition is done with `gdisk`
1. Use `lsblk` to find the device name where Arch will be installed. It is usually `sdc`, `sdd`, etc.
2. **Consider** the device `sdz` (Change `sdz` in the following line to the proper device name).
3. `gdisk /dev/sdz` to Edit Partition on the drive.
   The basic commands are `p` (get details about all partitions), `d` (delete partition), `n` (create a new partition), and `w` (write the changes of the partition)
4. View the partitions with `p`
5. Clear all the partitions with `d`. In the next prompt enter partition number.
6. Add new partitions with `n`. We will need 3 partitions because of the UEFI system
7. Create a `boot` partition of 2Gb, EF00 as partition type
8. Create a `[swap]` partition of 5Gb (actually 1.5x of total RAM if possible), 8200 as partition type
9. Create a `/` partition that will take all the remaining space, 8300 as the partition type
10. Check if all partitions are ok with `p`
11. Write all the partition info with `w`
## Format
**Consider** sdz1 is `efi_system_partition`, sdz2 is `swap_partition`, sdz3 is `root_partition`.
1. Using the https://wiki.archlinux.org/title/File_systems select the Btrfs for the `root_partition`. Commands are
2. `mkfs.btrfs /dev/sdz3` for `root_partition`
3. `mkswap /dev/sdz2` for `swap_partition`
4. `mkfs.fat -F 32 /dev/sdz1` for `efi_system_partition`
5. Use `lsblk` to check for correct sizes
## Mount disk
> [!NOTE]
> When using BTRFS for `root_partition` look at the recovery guide to properly set up BTRFS snapshots with snapper

For mounting. We are using UEFI so, we have an extra `efi_system_partition`. Commands are
1. `mount /dev/sdz3 /mnt` for `root_partition`
2. `swapon /dev/sdz2` for `swap_partition`
3. `mount --mkdir /dev/sdz1 /mnt/boot/efi` for `efi_system_partition`
4. Use `lsblk` to check the correct mount points. we should have a `/mnt/boot`, `[swap]`, `/mnt`
# Install
## Select the mirrors 
Using `reflector` we are going to update our mirror list and save the new mirrorlist in the ArchLinux
```bash
reflector --country India --latest 5 --sort rate --save /etc/pacman.d/mirrorlist
```
## Upgrade keyring
```bash
pacman -Sy archlinux-keyring
```
## Install essential packages
```bash
pacstrap -K /mnt linux linux-firmware base base-devel networkmanager amd-ucode neovim man-db man-pages 
```
# Configure the system
## Fstab and Chroot
1. Fstab `genfstab -U /mnt >> /mnt/etc/fstab`
2. Check there are 3 entries in the file `cat /mnt/etc/fstab`
3. Chroot `arch-chroot /mnt`
## Time, Clock, Network configuration (hostname)
1. Timezone `ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime`
2. Update Clock `hwclock --systohc`
3. Hostname `echo "ArchUSB64" >> /etc/hostname`
4. Edit hosts file
## Localization
1. Write the command `nvim /etc/locale.gen` to open the file `/etc/locale.gen`
2. Use the `/` and type US to find the line with US
3. Uncomment the line
4. `:wq` to save the file
5. Run the command `locale-gen` to generate locale
6. Run `echo "LANG=en_US.UTF-8" >> /etc/locale.conf` to set the Language variable
7. Run `cat /etc/locale.conf` to view the same file
## Root password
Set the password after typing the command `passwd`
## Boot loader
Select a Boot loader. Here we are going to use `GRUB`
1. Install the packages `pacman -S grub efibootmgr`
2. Run `grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB --removable` to set up `GRUB`
3. Run `grub-mkconfig -o /boot/grub/grub.cfg` to generate config
# Restart
1. Run `exit` to get out of system
2. Run `umount -R /mnt` to unmount drives
3. Run `reboot` to restart sytsem
---
RESTART remove the Live Environment

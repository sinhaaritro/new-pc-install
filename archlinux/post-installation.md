# Creating new users and groups
1. Create a user named aritro by `useradd -m -G wheel aritro`
2. Change aritro's password by `passwd aritro`
## Editing when password is needed by pacman
Here `vi` is always needed. You need to run `visudo`
1. Run the command `visudo /etc/sudoers`
2. Find the **User privilege specification** section. Can use search
3. Uncomment the line `# %wheel  ALL=(ALL:ALL) ALL
4. `:wq` to save and quit

You can add the following line to let people run some commands without sudo
```bash
## Allow wheel members to run some commands without a password
# %wheel ALL=(ALL) NOPASSWD: /usr/bin/shutdown,/usr/bin/reboot,/usr/bin/pacman -Syu,/usr/bin/pacman -Syyu,/usr/bin/pacman -Rns
```

# Upgrading pacman
# Install AUR helper
AUR helpers automate the process of building packages. But it is better to build the package manually.
## Making package
1. Search the package from https://aur.archlinux.org/
2. Copy its **Git Clone URL**
3. Goto a repo folder and run `git clone [GIT URL FROM STEP 2]
4. Go in the folder `cd [PACKAGE NAME]
5. Run `makepkg -s` to make the package. This will create a .pkg.tar.zst file
6. Run `sudo pacman -U [FILE NAME FROM STEP 5]

Alternatively, in step 5 we can write `makepkg -si`. Here `s` will get all dependencies, and `i` will also install the file (no need for step 6)
## Upgrading package
1. Goto repo folder and run `git pull`
2. Do steps 5 and 6 of Install AUR helper
# Managing systemd processes with systemctl (Start networkmanager)
systemctl can enable, start, stop service

`systemctl enable NetworkManager` will auto start networkmanager. This will help us to connect to the Internet.
# Install nvidia drivers
https://wiki.archlinux.org/title/NVIDIA
## Enable multilib repository 
1. Run `sudo nano /etc/pacman.conf`
2. Uncomment the line `[multilib]`
3. Uncomment the line `Include = /etc/pacman.d/mirrorlist`
4. Update pacman database `pacman -Syu`
## Installing the driver packages
1. Find the Card name from https://nouveau.freedesktop.org/CodeNames.html 
2. Get the package name from the table

| **_Driver name_**                                           	| **_Kernel_**     	| **_Base driver_** 	| **_OpenGL_**       	| **_OpenGL (multilib)_**  	|
|-------------------------------------------------------------	|------------------	|-------------------	|--------------------	|--------------------------	|
| **Turing (NV160/TUXXX) and newer**                          	| linux            	| nvidia-open       	| nvidia-utils       	| lib32-nvidia-utils       	|
| **Turing (NV160/TUXXX) and newer**                          	| any other kernel 	| nvidia-open-dkms  	| nvidia-utils       	| lib32-nvidia-utils       	|
| **Maxwell (NV110) series up to Ada Lovelace (NV190/ADXXX)** 	| linux            	| nvidia            	| nvidia-utils       	| lib32-nvidia-utils       	|
| **Maxwell (NV110) series up to Ada Lovelace (NV190/ADXXX)** 	| linux-lts        	| nvidia            	| nvidia-utils       	| lib32-nvidia-utils       	|
| **Maxwell (NV110) series up to Ada Lovelace (NV190/ADXXX)** 	| any other kernel 	| nvidia-dkms       	| nvidia-utils       	| lib32-nvidia-utils       	|
| **Kepler (NVE0) series**                                    	| any              	| nvidia-470xx-dkms 	| nvidia-470xx-utils 	| lib32-nvidia-470xx-utils 	|
| **GeForce 400/500/600 series cards [NVCx and NVDx]**        	| any              	| nvidia-390xx-dkms 	| nvidia-390xx-utils 	| lib32-nvidia-390xx-utils 	|
| **Tesla (NV50/G80-90-GT2XX)**                               	| any              	| nvidia-340xx-dkms 	| nvidia-340xx-utils 	| lib32-nvidia-340xx-utils 	|

3. Run `pacman -S nvidia-open nvidia-utils lib32-nvidia-utils nvidia-settings`
## Setup the Kernel Parameter for GRUB users
1. Edit GRUB file by `sudo nvim /etc/default/grub`
2. Find the line with `GRUB_CMDLINE_LINUX_DEFAULT`
3. New line will be `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nvidia-drm.modeset=1 nvidia-drm.fbdev=1"`
3. Save `:wq`
4. Update GRUB configuration `sudo grub-mkconfig -o /boot/grub/grub.cfg`
## Early Loading of NVIDIA Modules
1. Edit `mkinitcpio.conf` file by `sudo nvim /etc/mkinitcpio.conf`
2. Find the line that says `MODULES=()`
3. New line will be `MODULES=(... nvidia nvidia_modeset nvidia_uvm nvidia_drm ...)`
4. Find the line that says `HOOKS=()`
5. On the line delete the word `kms`
6. Save `:wq`
7. Regenerate the initramfs with `sudo mkinitcpio -P`
## Add the Pacman Hook
1. Create the hooks directory `sudo mkdir -p /etc/pacman.d/hooks/`
2. Create the file `nvim nvidia.hook`
3. Copy paste the following code
4. Save `:wq`
```
[Trigger]
Operation=Install
Operation=Upgrade
Operation=Remove
Type=Package
# Should match your base driver package, e.g. Target=nvidia-470xx-dkms
Target=nvidia
# Should match your kernel package, e.g. Target=linux-lts
Target=linux

[Action]
Description=Update Nvidia module in initcpio
Depends=mkinitcpio
When=PostTransaction
NeedsTargets
Exec=/bin/sh -c 'while read -r trg; do case $trg in linux) exit 0; esac; done; /usr/bin/mkinitcpio -P'
```
## Reboot
Run `nvidia-smi` to get card details
# Install wayland
Install `sudo pacman -S wayland`
# Install hyprland
1. Install `sudo pacman -S kitty hyprland`
2. Run the command in ttyl `Hyprland`
3. `[SUPER]+M` to quit hyprland

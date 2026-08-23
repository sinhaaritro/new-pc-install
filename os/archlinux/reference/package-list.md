# Master Package List

> Auto-generated from `manifest.yaml`. Do not edit manually.

## Pre-Install

| Module | Packages | Required |
|--------|----------|----------|
| System Overview | — | ✅ Required |
| Pre-Flight Checklist | — | ✅ Required |

## Base System

| Module | Packages | Required |
|--------|----------|----------|
| Verify Boot & Network | — | ✅ Required |
| Partitioning | — | ✅ Required |
| Filesystems & Btrfs Subvolumes | `btrfs-progs` | ✅ Required |
| Install Base Packages | `base`, `base-devel`, `linux`, `linux-headers`, `linux-firmware`, `amd-ucode`, `btrfs-progs`, `nano`, `git` | ✅ Required |
| System Configuration | `networkmanager` | ✅ Required |
| Users & Sudo | — | ✅ Required |
| Bootloader (GRUB) | `grub`, `efibootmgr`, `os-prober`, `mtools`, `dosfstools` | ✅ Required |
| First Reboot | — | ✅ Required |

## System Hardening

| Module | Packages | Required |
|--------|----------|----------|
| NVIDIA Drivers | `nvidia-open`, `nvidia-utils`, `lib32-nvidia-utils`, `nvidia-settings` | ⚡ Recommended |
| Btrfs Snapshots & Recovery | `snapper`, `snap-pac`, `grub-btrfs`, `btrfs-assistant`, `rsync` | ⚡ Recommended |
| AUR Helper (yay) | — | ⚡ Recommended |
| Sound (PipeWire) | `pipewire`, `wireplumber`, `pipewire-alsa`, `pipewire-pulse`, `pipewire-jack`, `helvum` | ⚡ Recommended |
| Wi-Fi & Bluetooth | `bluez`, `bluez-utils`, `bluetui` | 💡 Optional |
| Clock Sync (Dual-Boot) | — | 💡 Optional |
| Firewall | `ufw` | 💡 Optional |
| External Drives & NTFS | `ntfs-3g`, `udisks2`, `udiskie` | 💡 Optional |
| SSH & Git | `openssh` | ⚡ Recommended |

## Desktop

| Module | Packages | Required |
|--------|----------|----------|
| Install Hyprland | `hyprland`, `wayland`, `xdg-desktop-portal-hyprland`, `kitty`, `qt5-wayland`, `qt6-wayland` | ✅ Required |
| Hyprland Core Config | — | ✅ Required |
| Lock & Idle | `hyprlock`, `hypridle` | ⚡ Recommended |
| Wallpaper | `swww` | 💡 Optional |
| Screen Sharing | `xdg-desktop-portal-hyprland` | ⚡ Recommended |
| Shell & Terminal | `zsh`, `fzf`, `zoxide` | ⚡ Recommended |
| App Launcher | `rofi-wayland` | ⚡ Recommended |
| Status Bar | `waybar` | ⚡ Recommended |
| Notifications | `swaync` | ⚡ Recommended |
| Display Manager | `greetd`, `greetd-tuigreet` | 💡 Optional |
| Clipboard | `wl-clipboard`, `clipse` | ⚡ Recommended |
| Screenshots | `grim`, `slurp`, `swappy` | 💡 Optional |
| File Manager | `yazi`, `thunar` | ⚡ Recommended |
| Fonts | `noto-fonts`, `noto-fonts-emoji`, `ttf-jetbrains-mono-nerd` | ⚡ Recommended |

## Workflow

| Module | Packages | Required |
|--------|----------|----------|
| Dotfiles Backup (GNU Stow) | `stow` | ⚡ Recommended |

### Profile: Developer

| Module | Packages | Required |
|--------|----------|----------|
| NeoVim | `neovim` | ⚡ Recommended |
| Containers (Podman) | `podman` | 💡 Optional |
| DevPod | — | 💡 Optional |
| Local AI Models | `nvidia-container-toolkit` | 💡 Optional |
| Language Runtimes | — | 💡 Optional |
| API Testing | — | 💡 Optional |

### Profile: Gaming

| Module | Packages | Required |
|--------|----------|----------|
| Steam | `steam` | ⚡ Recommended |
| Proton & ProtonGE | — | ⚡ Recommended |
| Heroic Launcher | — | 💡 Optional |
| MangoHud | `mangohud` | 💡 Optional |
| Controllers | — | 💡 Optional |

### Profile: Creative

| Module | Packages | Required |
|--------|----------|----------|
| OBS Studio | `obs-studio` | 💡 Optional |
| DaVinci Resolve | — | 💡 Optional |
| Media Players | `mpv` | 💡 Optional |

---

**Total unique packages:** 73

**Full list (alphabetical):**
```
amd-ucode base base-devel bluetui bluez bluez-utils btrfs-assistant btrfs-progs clipse dosfstools efibootmgr fzf git greetd greetd-tuigreet grim grub grub-btrfs helvum hypridle hyprland hyprlock kitty lib32-nvidia-utils linux linux-firmware linux-headers mangohud mpv mtools nano neovim networkmanager noto-fonts noto-fonts-emoji ntfs-3g nvidia-container-toolkit nvidia-open nvidia-settings nvidia-utils obs-studio openssh os-prober pipewire pipewire-alsa pipewire-jack pipewire-pulse podman qt5-wayland qt6-wayland rofi-wayland rsync slurp snap-pac snapper steam stow swappy swaync swww thunar ttf-jetbrains-mono-nerd udiskie udisks2 ufw waybar wayland wireplumber wl-clipboard xdg-desktop-portal-hyprland yazi zoxide zsh
```
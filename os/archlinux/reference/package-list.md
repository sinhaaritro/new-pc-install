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
| GPU (NVIDIA) | `nvidia-open`, `nvidia-utils`, `lib32-nvidia-utils`, `nvidia-settings` | ⚡ Recommended |
| Bootloader (GRUB) | `grub`, `efibootmgr`, `os-prober`, `mtools`, `dosfstools` | ✅ Required |
| First Reboot | — | ✅ Required |

## System Hardening

| Module | Packages | Required |
|--------|----------|----------|
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
| Terminal Emulator | `kitty` | ⚡ Recommended |
| Window Manager | `hyprland`, `wayland`, `xdg-desktop-portal-hyprland`, `qt5-wayland`, `qt6-wayland` | ✅ Required |
| Desktop Config | — | ✅ Required |
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
| File Manager | `yazi` | ⚡ Recommended |
| Fonts | `noto-fonts`, `noto-fonts-emoji`, `ttf-jetbrains-mono-nerd` | ⚡ Recommended |
| Browser | `firefox`, `zen-browser-bin` | 💡 Optional |
| Dotfiles (GNU Stow) | `stow` | ⚡ Recommended |

## Workflow

| Module | Packages | Required |
|--------|----------|----------|

### Profile: Developer

| Module | Packages | Required |
|--------|----------|----------|
| NeoVim | `neovim` | ⚡ Recommended |
| Containers (Podman) | `podman` | 💡 Optional |
| DevPod | — | 💡 Optional |
| Language Runtimes | — | 💡 Optional |
| API Testing | — | 💡 Optional |

### Profile: AI

| Module | Packages | Required |
|--------|----------|----------|
| Local Inference (llama.cpp) | `cuda` | ⚡ Recommended |
| AI Harness Tools | — | ⚡ Recommended |
| IDE Integration | — | ⚡ Recommended |
| Autonomous Agents | — | 💡 Optional |
| AI Training | — | 💡 Optional |

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

**Total unique packages:** 74

**Full list (alphabetical):**
```
amd-ucode base base-devel bluetui bluez bluez-utils btrfs-assistant btrfs-progs clipse cuda dosfstools efibootmgr firefox fzf git greetd greetd-tuigreet grim grub grub-btrfs helvum hypridle hyprland hyprlock kitty lib32-nvidia-utils linux linux-firmware linux-headers mangohud mpv mtools nano neovim networkmanager noto-fonts noto-fonts-emoji ntfs-3g nvidia-open nvidia-settings nvidia-utils obs-studio openssh os-prober pipewire pipewire-alsa pipewire-jack pipewire-pulse podman qt5-wayland qt6-wayland rofi-wayland rsync slurp snap-pac snapper steam stow swappy swaync swww ttf-jetbrains-mono-nerd udiskie udisks2 ufw waybar wayland wireplumber wl-clipboard xdg-desktop-portal-hyprland yazi zen-browser-bin zoxide zsh
```
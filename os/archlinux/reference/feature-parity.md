# Windows → Arch Linux + Hyprland: Feature Parity Reference

> [!NOTE]
> This is a **lookup reference** for transitioning from Windows to Arch + Hyprland.
> For each Windows feature, find the Linux equivalent across CLI, TUI, and GUI — then follow the guide path to set it up.
>
> **Tool priority**: TUI → CLI → GUI. The **★ Recommended** column shows the preferred pick.
>
> **Feature Gaps** notes anything the Linux tool *cannot* do compared to the Windows version.

---

## Tier 1: Bare-Minimum OS

*Everything needed to boot, log in, and use the system as a basic daily driver.*

### 1A. System Foundation

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 1.1 | OS Installation | `archinstall` (guided) | — | — | `archinstall` or manual | `os/archlinux/1-setup-and-installation.md` | No graphical installer; all terminal-based |
| 1.2 | Bootloader (UEFI) | `grub-install`, `grub-mkconfig` | — | — | GRUB | `os/archlinux/1-setup-and-installation.md` | No auto-repair like Windows Recovery |
| 1.3 | Package Manager (Windows Update) | `pacman -Syu` | — | — | pacman + yay (AUR) | `os/archlinux/2.1-post-installation.md` | Rolling release = more frequent updates; no scheduled updates UI |
| 1.4 | AUR Helper | — | `yay` (interactive prompts) | `pamac` | yay | `os/archlinux/2.3-aur-packages.md` | AUR packages are community-built, not officially supported |
| 1.5 | User Accounts & Permissions | `useradd`, `passwd`, `visudo` | — | — | CLI | `os/archlinux/2.2-user-setup.md` | No Settings UI for accounts |
| 1.6 | System Restore / Recovery | `snapper` CLI | `btrfs-assistant` | `btrfs-assistant` | snapper + btrfs-assistant | `os/archlinux/2.x recovery.md` | More powerful than Windows Restore (per-package snapshots) |
| 1.7 | GPU Drivers (Nvidia App) | `nvidia-smi`, `nvidia-settings` CLI | — | `nvidia-settings` | nvidia-open + nvidia-settings | `os/archlinux/2.x nvidia-driver.md` | No ShadowPlay, no Game Filters, no overlay. See Tier 3/5 for alternatives |
| 1.8 | Dual-Boot Clock Sync | `timedatectl set-ntp true` | — | — | timedatectl | `os/archlinux/2.x clock.md` | Requires Windows registry edit on the other side |

### 1B. Desktop Environment & Shell

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 1.9 | Desktop / Window Manager | — | — | Hyprland | Hyprland | `os/archlinux/3.x hyprland-config.md` | Tiling WM — no traditional desktop metaphor; steep learning curve |
| 1.10 | Display Server | — | — | Wayland | Wayland (via Hyprland) | `os/archlinux/2.1-post-installation.md` | Some legacy X11 apps need `xwayland` |
| 1.11 | Terminal Emulator | — | — | Kitty | Kitty | `os/archlinux/3.x kitty-config.md` | — |
| 1.12 | Command Shell (PowerShell) | zsh + oh-my-zsh | — | — | zsh + oh-my-zsh | `os/archlinux/3.x zsh-setup.md` | No PowerShell-style object pipeline; different scripting paradigm |
| 1.13 | Shell Enhancements (history, jump) | `fzf`, `zoxide` | — | — | fzf + zoxide | `os/archlinux/3.x zsh-setup.md` | — |
| 1.14 | File Explorer | `ls`, `find`, `fd` | `yazi` | `thunar` | yazi (TUI) | `os/archlinux/3.x yazi-config.md` | yazi: no drag-and-drop. Thunar available for when GUI is needed |
| 1.15 | Start Menu / App Launcher | `dmenu` | — | `rofi-wayland` | rofi-wayland | `os/archlinux/3.x rofi-config.md` | No pinned apps grid like Windows Start; search-driven |
| 1.16 | Taskbar | — | — | `waybar` | waybar | `os/archlinux/3.x waybar-config.md` | Fully customizable but requires manual JSON/CSS config |
| 1.17 | System Tray | — | — | waybar (built-in tray) | waybar tray module | `os/archlinux/3.x waybar-config.md` | Some apps don't support Wayland tray protocol yet |
| 1.18 | Lock Screen | `hyprlock` | — | `hyprlock` | hyprlock | `os/archlinux/3.x hyprlock-config.md` | — |
| 1.19 | Login Screen (Display Manager) | `greetd` + `tuigreet` | `tuigreet` | `sddm` | greetd + tuigreet | `os/archlinux/3.x greetd-setup.md` | tuigreet: no user avatar or fancy animations; minimal and fast |
| 1.20 | Wallpaper | — | — | `swww` | swww | `os/archlinux/3.x swww-setup.md` | swww supports animated wallpapers; hyprpaper is static-only alternative |
| 1.21 | Notifications (Action Center) | `notify-send` | — | `swaync` | swaync | `os/archlinux/3.x swaync-config.md` | swaync has notification center panel like Windows Action Center |
| 1.22 | Keyboard Shortcuts / Tiling | Hyprland `bind` config | — | — | Hyprland keybinds | `os/archlinux/3.x hyprland-config.md` | Far more powerful than Windows Snap; fully scriptable |
| 1.23 | Multi-Monitor Management | `hyprctl monitors` | — | Hyprland config | Hyprland | `os/archlinux/3.x hyprland-config.md` | Per-monitor workspaces; config-driven, no drag-and-drop display settings |
| 1.24 | Idle/Screen Off Management | `hypridle` config | — | — | hypridle | `os/archlinux/3.x hypridle-config.md` | — |

### 1C. Connectivity & Hardware

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 1.25 | Wi-Fi | `iwctl`, `nmcli` | `impala` | `nm-applet` | impala (TUI) | `os/archlinux/2.x wifi-bluetooth.md` | — |
| 1.26 | Bluetooth | `bluetoothctl` | `bluetui` | `blueman` | bluetui (TUI) | `os/archlinux/2.x wifi-bluetooth.md` | — |
| 1.27 | Volume / Audio Output | `wpctl`, `pactl` | `pulsemixer` | `pavucontrol` | pulsemixer (TUI) | `os/archlinux/2.x sound.md` | — |
| 1.28 | Audio Server (system-level) | — | — | PipeWire + WirePlumber | PipeWire | `os/archlinux/2.x sound.md` | Replaces Windows audio stack entirely |
| 1.29 | Audio Routing (Voicemeeter) | `pw-link`, `pw-cli` | — | `helvum` | helvum (GUI patchbay) | `os/archlinux/3.x audio-routing.md` | No virtual cable abstraction like Voicemeeter; PipeWire is node-based instead. Requires manual routing setup |
| 1.30 | Media Keys (play/pause/skip) | `playerctl` | — | waybar media module | playerctl + waybar | `os/archlinux/3.x waybar-config.md` | — |
| 1.31 | Brightness Control | `brightnessctl` | — | waybar module | brightnessctl | `os/archlinux/3.x hyprland-config.md` | Desktop PCs often don't expose brightness via kernel |
| 1.32 | Power (shutdown, reboot, sleep) | `systemctl poweroff/reboot/suspend` | — | rofi power menu or `wlogout` | wlogout | `os/archlinux/3.x wlogout-config.md` | Hibernate needs swap + config; not automatic like Windows |
| 1.33 | NTFS Drive Mounting | `mount`, `ntfs-3g` | — | Thunar auto-mount | ntfs-3g + udisks2 + udiskie | `os/archlinux/2.x external-drives.md` | — |
| 1.34 | USB Hot-Plug / Auto-Mount | `udiskie` (daemon) | — | Thunar/udiskie | udiskie | `os/archlinux/2.x external-drives.md` | — |
| 1.35 | Firewall (Windows Defender FW) | `ufw`, `iptables` | — | `gufw` | ufw | `os/archlinux/2.x firewall.md` | CLI-based rules; no per-app popup prompts |

### 1D. Utilities & Essentials

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 1.36 | Clipboard (Ctrl+C/V) | `wl-copy`, `wl-paste` | `clipse` | — | wl-clipboard + clipse | `os/archlinux/3.x clipboard-setup.md` | clipse provides clipboard history in TUI |
| 1.37 | Screenshots (Snipping Tool) | `grim` + `slurp` | — | `hyprshot` or `flameshot` | grim + slurp + hyprshot | `os/archlinux/3.x screenshot-setup.md` | No built-in annotation like Snipping Tool; use `swappy` for annotation |
| 1.38 | Screenshot Annotation | — | — | `swappy` | swappy | `os/archlinux/3.x screenshot-setup.md` | — |
| 1.39 | Color Picker (PowerToys) | `hyprpicker` | — | — | hyprpicker | `os/archlinux/3.x hyprland-config.md` | — |
| 1.40 | File Search (Windows Search) | `fd`, `find`, `locate` | `fzf` (interactive) | — | fd + fzf | `os/archlinux/3.x zsh-setup.md` | No system-wide indexed search; fd is instant but searches on-demand |
| 1.41 | Content Search (grep in files) | `rg` (ripgrep) | `fzf` + `rg` combo | — | ripgrep + fzf | `os/archlinux/3.x zsh-setup.md` | — |
| 1.42 | Process Manager (Task Manager) | `ps`, `kill`, `top` | `btop`, `glances` | `gnome-system-monitor` | btop (TUI) | `os/archlinux/3.x btop-config.md` | btop is arguably better than Task Manager |
| 1.43 | Disk Usage Analyzer | `du`, `df` | `ncdu` | `baobab` | ncdu (TUI) | `os/archlinux/3.x utilities.md` | — |
| 1.44 | Archive Manager (7-Zip) | `7z`, `tar`, `unzip` | — | `file-roller` | p7zip + file-roller | `os/archlinux/3.x utilities.md` | — |
| 1.45 | Calculator | `bc`, `python` | `kalker` (AUR) | — | kalker | `os/archlinux/3.x utilities.md` | — |
| 1.46 | Fonts | `fc-list`, `fc-cache` | — | — | Nerd Fonts + noto-fonts | `os/archlinux/3.x fonts-setup.md` | Need to install fonts explicitly; no Windows-like font store |
| 1.47 | Dotfile Backup (config sync) | `stow` | — | — | GNU Stow + git | `os/archlinux/3.x stow-setup.md` | More powerful than Windows settings sync; version-controlled |
| 1.48 | Emoji Picker (Win+.) | — | — | `rofi-emoji` or `wofi-emoji` | rofi-emoji | `os/archlinux/3.x rofi-config.md` | — |

---

## Tier 2: Development & Coding

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 2.1 | Git + SSH Keys | `git`, `ssh-keygen`, `ssh-add` | `lazygit` | — | git + lazygit (TUI) | `os/archlinux/2.x ssh.md` | lazygit provides full TUI for staging, branching, rebasing |
| 2.2 | Code Editor (VSCodium) | — | `neovim` (with plugins) | `vscodium` (AUR) | neovim (TUI) | `software/development/neovim/linux-setup.md` | NeoVim needs plugin config (LSP, treesitter, etc.) for full IDE parity |
| 2.3 | Code Editor (Antigravity) | — | — | `antigravity` | antigravity (GUI) | `software/development/antigravity/linux-setup.md` | Check Linux availability |
| 2.4 | NeoVim Plugin Manager | — | `lazy.nvim` | — | lazy.nvim | `software/development/neovim/linux-setup.md` | — |
| 2.5 | NeoVim LSP / Completion | — | `mason.nvim` + `nvim-lspconfig` | — | mason + lspconfig | `software/development/neovim/linux-setup.md` | — |
| 2.6 | Terminal Multiplexer (no Win equivalent) | `tmux` or `zellij` | `zellij` | — | zellij (TUI) | `software/development/zellij/linux-setup.md` | Windows doesn't have this; it's a Linux superpower |
| 2.7 | Containers (Docker Desktop) | `podman` | `lazydocker` | `podman-desktop` | podman + lazydocker | `os/archlinux/2.x containers.md` | lazydocker needs alias for podman socket |
| 2.8 | Dev Environments (DevPod) | `devpod` CLI | — | DevPod GUI (broken on Wayland) | devpod CLI | `os/archlinux/3.x development-setup.md` | GUI doesn't work on Wayland; CLI-only |
| 2.9 | Local AI Models | `ollama` (via podman) | — | Open WebUI (browser) | ollama + Open WebUI | `os/archlinux/2.x local-ai-models.md` | — |
| 2.10 | VPN (OpenVPN Connect) | `openvpn` | — | `nm-applet` VPN integration | openvpn + nmcli | `software/development/openvpn/linux-setup.md` | No GUI client like OpenVPN Connect; use nmcli or nm-applet |
| 2.11 | Python Environment | `python`, `pyenv`, `uv` | — | — | python + uv | `software/development/python/linux-setup.md` | — |
| 2.12 | Language Runtimes (Java, Go, etc.) | `pacman -S go jdk-openjdk ruby nodejs` | — | — | pacman | `software/development/runtimes/linux-setup.md` | — |
| 2.13 | Keyboard Firmware (QMK/VIA) | `qmk` CLI | — | VIA (AppImage/web) | qmk CLI + VIA web | `peripherals/keyboards/linux-setup.md` | VIA web app at usevia.app works in browser; no install needed |
| 2.14 | API Testing (Postman etc.) | `curl`, `httpie` | `posting` (TUI, AUR) | Insomnia / Bruno | posting (TUI) | `software/development/api-testing/linux-setup.md` | posting is a beautiful TUI API client |
| 2.15 | Database Client | `psql`, `mysql` | `lazysql` | `dbeaver` | lazysql (TUI) | `software/development/database/linux-setup.md` | — |
| 2.16 | SSH Remote Access | `ssh` | — | — | openssh | `os/archlinux/2.x ssh.md` | Already documented |

---

## Tier 3: Entertainment (Video, Movies, Images)

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 3.1 | Media Player (video) | `mpv` (CLI-launchable) | — | `mpv` (with GUI wrapper) | mpv | `software/entertainment/mpv/linux-setup.md` | mpv is CLI-first but opens a GUI window. Best player on Linux |
| 3.2 | Music Player | — | `cmus` / `ncmpcpp` | — | ncmpcpp + mpd | `software/entertainment/music/linux-setup.md` | No Spotify-like discovery; for local library playback |
| 3.3 | Image Viewer (Photos app) | `feh` | `viu` (terminal preview) | `imv` or `loupe` | imv | `software/entertainment/image-viewer/linux-setup.md` | imv is lightweight Wayland-native |
| 3.4 | Codecs (K-Lite Codec Pack) | — | — | `ffmpeg` + GStreamer plugins | ffmpeg (auto-handled) | `software/entertainment/codecs/linux-setup.md` | mpv/VLC handle codecs natively; no separate codec pack needed |
| 3.5 | Screen Recording | `wf-recorder` | — | OBS Studio | wf-recorder (CLI) | `software/entertainment/screen-recording/linux-setup.md` | wf-recorder for quick captures; OBS for full streaming/recording |
| 3.6 | Game/Replay Recording (ShadowPlay) | `gpu-screen-recorder` (CLI) | — | `gpu-screen-recorder-gtk` | gpu-screen-recorder | `software/entertainment/screen-recording/linux-setup.md` | Hardware-accelerated replay buffer; closest to ShadowPlay |
| 3.7 | Streaming (OBS Studio) | — | — | `obs-studio` | OBS Studio | `software/entertainment/obs/linux-setup.md` | Needs `obs-vkcapture` for game capture on Wayland; PipeWire for audio |
| 3.8 | Screen Sharing (Teams/Discord) | — | — | `xdg-desktop-portal-hyprland` | xdg-desktop-portal-hyprland | `os/archlinux/3.x screen-sharing-setup.md` | Critical for video calls. Requires portal + PipeWire config |
| 3.9 | Video Editing (DaVinci Resolve) | — | — | DaVinci Resolve (from website) | DaVinci Resolve | `software/creative/davinci-resolve/linux-setup.md` | Linux version exists but needs `opencl-nvidia`; no H.264/H.265 in free version |
| 3.10 | Vector Graphics (Inkscape) | — | — | `inkscape` | Inkscape | `software/creative/inkscape/linux-setup.md` | Native Linux; identical to Windows version |
| 3.11 | Raster Graphics (Affinity) | — | — | `krita` or `gimp` | Krita (for design) | `software/creative/krita/linux-setup.md` | **No Affinity on Linux**. Krita is closest for design/illustration. GIMP for photo editing |
| 3.12 | 3D Modeling (Blender) | — | — | `blender` | Blender | `software/creative/blender/linux-setup.md` | Native Linux; identical to Windows |
| 3.13 | Web Browser (Chrome) | — | `w3m`, `lynx` | `google-chrome` (AUR) / `chromium` / `firefox` | firefox + google-chrome | `software/browsers/linux-setup.md` | Firefox pre-installed; Chrome via AUR |
| 3.14 | PDF Viewer | — | — | `zathura` (keyboard-driven) | zathura | `software/entertainment/pdf/linux-setup.md` | zathura is vim-keybind PDF viewer; lightweight, keyboard-first |

---

## Tier 4: Office & Productivity

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 4.1 | Office Suite (Word/Excel/PPT) | — | — | `libreoffice-fresh` or `onlyoffice` | LibreOffice | `software/office/libreoffice/linux-setup.md` | **Formatting differences** with MS Office files. OnlyOffice has better .docx compatibility. Or use Office 365 web |
| 4.2 | Microsoft Teams | — | — | `teams-for-linux` (AUR) or PWA | teams-for-linux | `software/office/teams/linux-setup.md` | Official Linux client discontinued. Community Electron wrapper or browser PWA. Screen sharing works via portal |
| 4.3 | OneDrive (cloud sync) | `rclone` | — | `onedriver` (AUR, FUSE mount) | rclone | `software/office/onedrive/linux-setup.md` | No native client. rclone can mount as filesystem. `onedriver` provides FUSE GUI mount |
| 4.4 | Obsidian (notes) | — | — | `obsidian` | Obsidian | `software/office/obsidian/linux-setup.md` | Native Linux AppImage/pacman; identical to Windows |
| 4.5 | Email Client (Outlook) | `neomutt` | `neomutt` | `thunderbird` | neomutt (TUI) | `software/office/email/linux-setup.md` | neomutt is powerful but steep learning curve; Thunderbird for easier setup |
| 4.6 | Calendar Widget | — | `calcurse` | waybar clock module | calcurse | `software/office/calendar/linux-setup.md` | No system-integrated calendar like Windows; calcurse is standalone |
| 4.7 | USB Flasher (Balena Etcher) | `dd`, `ventoy` | — | `balena-etcher` (AUR) | ventoy (CLI) | `software/utilities/usb-flasher/linux-setup.md` | Ventoy: flash once, copy ISOs forever. Superior to Etcher |
| 4.8 | File Sharing (network) | `scp`, `rsync` | — | `warpinator` or KDE Connect | rsync (CLI) | `software/utilities/file-sharing/linux-setup.md` | rsync for SSH-based transfer. warpinator for LAN GUI sharing |
| 4.9 | Torrent Client | — | `rtorrent` | `qbittorrent` | rtorrent or qbittorrent | `software/utilities/torrent/linux-setup.md` | — |

---

## Tier 5: Gaming

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 5.1 | Steam | — | — | `steam` (multilib) | Steam | `software/gaming/steam/linux-setup.md` | Needs multilib repo enabled. Native Linux client |
| 5.2 | Proton (Windows game compat) | — | — | Bundled with Steam | Proton + ProtonGE | `software/gaming/proton/linux-setup.md` | Check [protondb.com](https://protondb.com) for per-game compatibility. ProtonGE fixes more games |
| 5.3 | Epic Games Launcher | — | — | `heroic-games-launcher` (AUR) | Heroic | `software/gaming/heroic/linux-setup.md` | **No native Epic launcher on Linux**. Heroic is the community client (also supports GOG) |
| 5.4 | Discord | — | — | `vesktop` (AUR) | Vesktop | `software/gaming/discord/linux-setup.md` | Vesktop over official Discord: better Wayland screen-sharing + Vencord built-in |
| 5.5 | FPS Overlay (Nvidia Overlay) | `mangohud` (env var) | — | MangoHud overlay | MangoHud | `software/gaming/mangohud/linux-setup.md` | More detailed than Nvidia overlay (CPU, GPU, frametime graphs) |
| 5.6 | Game Filters (Nvidia Freestyle) | `vkbasalt` (env var) | — | — | vkBasalt | `software/gaming/vkbasalt/linux-setup.md` | **Limited** compared to Freestyle. Supports ReShade shaders but fewer presets |
| 5.7 | Xbox Controller Support | Built-in kernel HID | — | — | kernel HID (works OOB) | `software/gaming/controllers/linux-setup.md` | Works out of the box for most controllers via kernel |
| 5.8 | PS4/PS5 Controller | `ds4drv` | — | — | kernel HID (works OOB) | `software/gaming/controllers/linux-setup.md` | PS5 DualSense works natively; some haptic features may be limited |
| 5.9 | Anti-Cheat (EAC/BattlEye) | N/A | N/A | N/A | Game-dependent | `software/gaming/anti-cheat/linux-setup.md` | **Major gap**. Some games with EAC/BattlEye work via Proton if dev enables it. Kernel-level anti-cheats (Vanguard, FACEIT) do NOT work |
| 5.10 | Game Launchers Unified | — | — | `lutris` | Lutris | `software/gaming/lutris/linux-setup.md` | Manages Wine prefixes, GOG, Epic, Humble; unified game library |
| 5.11 | Multi-Monitor Game Pinning | Hyprland window rules | — | — | Hyprland config | `os/archlinux/3.x hyprland-config.md` | `windowrulev2` to pin games to specific monitors |

---

## Tier 6: Hardware & Peripherals (Bonus)

| # | Windows Feature | CLI | TUI | GUI | ★ Recommended | Guide Path | Feature Gaps |
|---|---|---|---|---|---|---|---|
| 6.1 | Mouse Macros (Logitech GHUB) | `ratbagctl` | — | `piper` | piper (GUI) | `peripherals/mouse/logitech-g502/linux-setup.md` | **No macro recording** like GHUB. DPI, button remap, and polling rate only. Onboard memory profiles work if set from Windows first |
| 6.2 | RGB: Motherboard (ASRock Polychrome) | `openrgb` CLI | — | `openrgb` | OpenRGB | `hardware/lighting/openrgb/linux-setup.md` | Single app replaces ASRock Polychrome, G.Skill, and Zotac FireStorm. Some boards need i2c kernel module |
| 6.3 | RGB: RAM (G.Skill) | `openrgb` CLI | — | `openrgb` | OpenRGB | `hardware/lighting/openrgb/linux-setup.md` | Covered by OpenRGB |
| 6.4 | RGB: GPU (Zotac FireStorm) | `openrgb` CLI | — | `openrgb` | OpenRGB | `hardware/lighting/openrgb/linux-setup.md` | Covered by OpenRGB |
| 6.5 | Fan Control (DeepCool) | `fancontrol` | — | — | lm_sensors + fancontrol | `hardware/cooling/linux-setup.md` | **No DeepCool app on Linux**. Use BIOS fan curves (preferred) or kernel `fancontrol`. Limited compared to Windows app |
| 6.6 | Keyboard Firmware (QMK/VIA) | `qmk` CLI | — | VIA web (usevia.app) | qmk CLI + VIA web | `peripherals/keyboards/linux-setup.md` | VIA web app works in Chromium-based browsers. Need udev rules for keyboard access |

---

## Summary Dashboard

| Tier | Total | With TUI Option | CLI Only | GUI Only |
|---|---|---|---|---|
| **1. Bare-Minimum OS** | 48 | 18 | 16 | 14 |
| **2. Development** | 16 | 7 | 5 | 4 |
| **3. Entertainment** | 14 | 2 | 3 | 9 |
| **4. Office** | 9 | 3 | 3 | 3 |
| **5. Gaming** | 11 | 0 | 2 | 9 |
| **6. Hardware** | 6 | 0 | 4 | 2 |
| **TOTAL** | **104** | **30** | **33** | **41** |

---

## Open Decisions

> [!IMPORTANT]
> Before we start writing install guides, please confirm these choices or suggest alternatives:

| # | Decision | My Recommendation | Why | Alternative |
|---|---|---|---|---|
| 1 | Notification Manager | **swaync** | Has notification center panel (closest to Windows Action Center) | dunst (lighter, no panel) |
| 2 | Wallpaper Manager | **swww** | Supports animated wallpapers + smooth transitions | hyprpaper (static only, lighter) |
| 3 | Display Manager | **greetd + tuigreet** | Minimal, fast, TUI-first | sddm (graphical, heavier) |
| 4 | Status Bar | **waybar** | Most mature, best Hyprland integration, huge community | eww (more customizable but Rust DSL) |
| 5 | Process Viewer | **btop** | Better than glances for interactive use, GPU monitoring | glances (better for remote/dashboard) |
| 6 | Office Suite | **LibreOffice** | Full offline suite, most features | OnlyOffice (better MS compat) |
| 7 | Affinity Replacement | **Krita** (design) + **GIMP** (photo) | No single replacement; split by use case | — |
| 8 | Music Player | **ncmpcpp + mpd** | TUI-first, daemon-based, separates playback from UI | cmus (simpler, all-in-one) |
| 9 | Email Client | **neomutt** | TUI-first, extremely powerful | thunderbird (easier, GUI) |
| 10 | Discord Client | **Vesktop** | Better Wayland screen-sharing than official Discord | official discord package |

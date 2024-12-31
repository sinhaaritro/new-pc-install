# Linux Overview
Distro: Arch
Boot Loader: GRUB
Driver: nvidia-open
Display Server Protocol: Wayland
Window Manager: Hyprland
Terminal: Kitty
Command Shell: zsh
Command Shell Customization: ohmyzsh
Config Backup Manager: stow
Display Managers: 
Lock Screen: hyprlock
App Launcher: rofi 
File Manager(TUI): yazi
File Manager(GUI): Thunar,
Status Bar: waybar,hybrid-bar,eww
Wallpaper Manager: hyprpaper ?
Notification Manager: dunst, mako, fnott and swaync
Process Viewer: glances
Text Editor: NeoVim
Fonts: 
Media Player: mpv
Screen Recorder: https://wiki.archlinux.org/title/Screen_capture#Wayland
Screen Sharing: pipewire ?
Color picker: Hyprpicker ?
Clipboard Managers: clipse, cb

Useful packages: fzf,zoxide,podman,podman_desktop

# Hyprland Setup
# Config Hyprland
# Install display manager
# Wallpaper
# bash
# Application launcher
# Notification
# Kitty
# Status bar

# NeoVim Setup
# Base setup
# Plugin manager
# Color scheme
# Syntax highlighter

# GNU Stow
gnu-stow naming
[type]_[name]_[variant]
[type]: p=(For a specific Package like neovim) s=(For a specific Style that groups multiple package)
[name]: Name of the package
[variant]: 
[version]: 

cd dotfiles/
mkdir -p ~/dotfiles/p_kitty/.config/kitty
mv ~/.config/kitty ~/dotfiles/p_kitty/.config/
stow --adopt p_kitty
git --reset hard


# SSH
Add openssh to list package

Type-Name-Variant





hyprland
kitty
wofi
waybar


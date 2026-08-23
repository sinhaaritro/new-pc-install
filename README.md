# New PC Install Guide

A modular PC installation and configuration guide. Documentation is split into logical domains so you can mix and match components without cluttering your view.

> **Status:** The [Arch Linux guide](./os/archlinux/) is the main body of this repo and is actively being written — Phases 0–2 are complete, Phases 3–4 are in progress (each module page notes its own status).

## 🖥️ OS Installation & Setup

### [Arch Linux + Hyprland](./os/archlinux/README.md)
Modular, phased install guide. Each phase produces a **usable system** at a defined milestone.

| Phase | Milestone | Status |
|-------|-----------|--------|
| [Phase 0: Pre-Install](./os/archlinux/phase-0-pre-install/README.md) | Ready to install | ✅ Done |
| [Phase 1: Base System](./os/archlinux/phase-1-base-system/README.md) | Bootable CLI (TTY) | ✅ Done |
| [Phase 2: System Hardening](./os/archlinux/phase-2-system-hardening/README.md) | Stable + drivers | ✅ Done |
| [Phase 3: Desktop](./os/archlinux/phase-3-desktop/README.md) | Graphical desktop | 🚧 In progress |
| [Phase 4: Workflow](./os/archlinux/phase-4-workflow/README.md) | Daily driver | 🚧 In progress |

Reference material:
- [Feature Parity](./os/archlinux/reference/feature-parity.md) — Windows → Linux equivalents
- [Package List](./os/archlinux/reference/package-list.md) — all packages by phase (auto-generated)
- [Dependency Chart](./os/archlinux/chart.html) — rendered module dependency map
- [Manifest](./os/archlinux/manifest.yaml) — module metadata (single source of truth)

### Windows
- [Pre-Install Checklist](./os/windows/pre-install.md) — backups & screenshots before wiping
- [Installation](./os/windows/installation.md) — Windows 11 install from USB + initial setup
- [Optional: Partitioning](./os/windows/optional-partitioning.md) — shrink C: for dual-boot
- [Optional: Automatic Login](./os/windows/optional-login.md) — netplwiz + Hello toggles
- [Start Menu Layout](./os/windows/apps/) — screenshots of the customized start menu
- [System Sound Setup](./os/windows/audio/) — screenshots of volume mixer config

## 🤖 Automation

- [Ansible — Play 1](./ansible/README.md) — live-USB install through first reboot (Arch Linux, Phase 0–1): partition → pacstrap → chroot config → GRUB dual-boot → reboot. Safety-gated (`--confirm-destructive`); manifest parity checked.

## 🛠️ Hardware Configuration
*Motherboard, core components, and lighting instructions.*
- **BIOS:** [Motherboard Setup](./hardware/bios/setup.md) — UEFI access, EXPO/XMP, fast boot
- **Lighting:** *(screenshot folders — docs in progress)*
  - [ASRock Polychrome](./hardware/lighting/asrock/)
  - [G.Skill RGB](./hardware/lighting/gskill/)
  - [GPU RGB](./hardware/lighting/gpu/)

## ⌨️ Peripherals
*Keyboards, mice, and external accessories.*
- **Keyboards (QMK/VIA):**
  - **RK R65** — [VIA definition](./peripherals/keyboards/R65_QMK_VIA_definition.json) · [custom layout](./peripherals/keyboards/rk-r65.custom_layout.json) · [default layout](./peripherals/keyboards/rk_r65.default.layout.json)
  - **Shorty Zero 1** — [VIA definition](./peripherals/keyboards/shorty_zero_1_QMK_VIA_definition.json) · [custom layout](./peripherals/keyboards/shorty_zero_1.custom_layout.json)
- **Mouse:**
  - [Logitech G502 Hero](./peripherals/mouse/logitech-g502/) — G HUB config screenshots

## 💾 Software
*App installs and configurations, per operating system.*

### Windows (main guide)
- [Windows Setup — App Inventory](./software/windows-setup.md) — full app list + one-shot `winget import` reinstall
- [winget Export](./software/winget-export.json) — machine-readable app export

### By Category
| Category | Guide |
|----------|-------|
| Audio | [VoiceMeeter Potato](./software/audio/voicemeeter-potato/) — routing diagram + importable settings XML |
| Creative | [DaVinci Resolve](./software/creative/davinci-resolve/windows-setup.md) |
| Development | [Git](./software/development/git/windows-setup.md) · [VSCodium](./software/development/vscodium/windows-setup.md) · [Antigravity](./software/development/antigravity/windows-setup.md) |
| Gaming | [Steam / Epic / Discord](./software/gaming/windows-setup.md) |
| Graphics | [NVIDIA App](./software/graphics/nvidia/windows-setup.md) |
| Office | [Microsoft Office (MAS activation)](./software/office/windows-setup.md) |

---
*If you swap a physical component (e.g. replacing the ASRock motherboard), simply create a new folder under `hardware/` and update these links!*

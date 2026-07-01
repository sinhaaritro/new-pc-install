# Arch Linux Installation Guide

A modular, phased installation guide for Arch Linux with Hyprland. Each phase produces a **usable system** at a defined milestone.

| Phase | Milestone | Status |
|-------|-----------|--------|
| [**Phase 0: Pre-Install**](./phase-0-pre-install/README.md) | Ready to install | BIOS, USB, drive ID |
| [**Phase 1: Base System**](./phase-1-base-system/README.md) | Bootable CLI (TTY) | Btrfs, GRUB, dual-boot |
| [**Phase 2: System Hardening**](./phase-2-system-hardening/README.md) | Stable + drivers | NVIDIA, snapshots, audio, SSH |
| [**Phase 3: Desktop**](./phase-3-desktop/README.md) | Graphical desktop | Hyprland + desktop tools |
| [**Phase 4: Workflow**](./phase-4-workflow/README.md) | Daily driver | Dev / Gaming / Creative profiles |

## Quick Links

- [Feature Parity Reference](./reference/feature-parity.md) — Windows → Linux equivalents
- [Package List](./reference/package-list.md) — All packages by phase
- [Manifest](./manifest.yaml) — Module metadata (single source of truth)

## Dependency Chart

<!-- CHART:START -->

```mermaid
flowchart TD
    subgraph phase_0["📋 Phase 0: Pre-Install"]
        overview(["Overview"])
        pre_flight(["Pre-Flight Checklist"])
        overview --> pre_flight
    end

    subgraph phase_1["🖥️ Phase 1: Base System"]
        verify_boot(["Verify Boot & Network"])
        partitioning(["Partitioning"])
        filesystems(["Filesystems & Btrfs"])
        install_base(["Install Base"])
        system_config(["System Config"])
        users_sudo(["Users & Sudo"])
        bootloader(["Bootloader GRUB"])
        first_reboot(["First Reboot"])

        verify_boot --> partitioning --> filesystems --> install_base
        install_base --> system_config --> users_sudo --> bootloader --> first_reboot
    end

    subgraph phase_2["🛡️ Phase 2: System Hardening"]
        nvidia(["NVIDIA Drivers"])
        snapshots(["Btrfs Snapshots"])
        aur(["AUR Helper"])
        sound(["Sound PipeWire"])
        networking{{"Wi-Fi & Bluetooth"}}
        clock_sync{{"Clock Sync"}}
        firewall{{"Firewall"}}
        ext_drives{{"External Drives"}}
        ssh_mod(["SSH & Git"])
    end

    subgraph phase_3["🪟 Phase 3: Desktop"]
        subgraph hyprland["Hyprland"]
            hypr_install(["Install"])
            hypr_config(["Core Config"])
            hypr_lock(["Lock & Idle"])
            hypr_wall{{"Wallpaper"}}
            hypr_share(["Screen Sharing"])
            hypr_install --> hypr_config
            hypr_config --> hypr_lock
            hypr_config --> hypr_wall
        end
        shell(["Shell & Terminal"])
        launcher(["App Launcher"])
        bar(["Status Bar"])
        notif(["Notifications"])
        dm{{"Display Manager"}}
        clip(["Clipboard"])
        shots{{"Screenshots"}}
        filemgr(["File Manager"])
        fonts_mod(["Fonts"])
    end

    subgraph phase_4["🚀 Phase 4: Workflow"]
        subgraph profile_dev["🛠️ Developer"]
            neovim_mod(["NeoVim"])
            containers{{"Containers"}}
            devpod_mod{{"DevPod"}}
            local_ai{{"Local AI"}}
            languages{{"Languages"}}
            api_test{{"API Testing"}}
            containers --> devpod_mod
        end
        subgraph profile_gaming["🎮 Gaming"]
            steam_mod(["Steam"])
            proton_mod(["Proton"])
            heroic{{"Heroic"}}
            mangohud_mod{{"MangoHud"}}
            controllers_mod{{"Controllers"}}
            steam_mod --> proton_mod
        end
        subgraph profile_creative["🎨 Creative"]
            obs_mod{{"OBS"}}
            davinci{{"DaVinci Resolve"}}
            media{{"Media Players"}}
        end
        dotfiles(["Dotfiles Backup"])
    end

    %% Cross-phase dependencies
    pre_flight --> verify_boot
    first_reboot --> nvidia & snapshots & aur & sound & networking & clock_sync & firewall & ext_drives & ssh_mod
    nvidia --> hypr_install
    hypr_config --> shell & launcher & bar & notif & dm & clip & shots & filemgr & fonts_mod
    sound --> hypr_share
    hypr_install --> neovim_mod
    shell --> neovim_mod
    nvidia --> local_ai & steam_mod & heroic & mangohud_mod & davinci
    containers --> local_ai
    sound --> obs_mod & media
    hypr_share --> obs_mod
    ssh_mod --> dotfiles

    %% Phase styles
    style phase_0 fill:#1a1a2e,stroke:#e94560,color:#fff
    style phase_1 fill:#16213e,stroke:#0f3460,color:#fff
    style phase_2 fill:#1a1a2e,stroke:#533483,color:#fff
    style phase_3 fill:#0f3460,stroke:#e94560,color:#fff
    style phase_4 fill:#533483,stroke:#e94560,color:#fff
```

<!-- CHART:END -->

## Tooling

```bash
# Generate/update the Mermaid chart
python scripts/generate-chart.py

# Inject updated chart into this README
python scripts/generate-chart.py --inject README.md

# Validate all module files exist
python scripts/generate-chart.py --validate

# Generate package list
python scripts/generate-chart.py --packages --packages-output reference/package-list.md
```

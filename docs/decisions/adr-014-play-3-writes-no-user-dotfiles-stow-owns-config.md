---
tags: [ansible, phase-3, desktop, stow, config-ownership]
---

# ADR-014: Play 3 Writes No User Dotfiles — Stow Owns All Config

Status: Accepted
Date: 2026-08-24
Source: docs/specs/005-ansible-play-3-phase-3-desktop-boot-system-selectable-modules-config-free.md

## Context

Play 2 (spec 004) roles write system configuration (snapper config, GRUB, ufw,
PipeWire sockets) because those have no per-user dotfile alternative. Play 3's
modules are almost entirely user-facing desktop tools (Hyprland, waybar, rofi,
swaync, kitty, yazi, zsh) whose behavior is driven by dotfiles the user already
maintains via GNU Stow (Phase 4 `dotfiles-backup`). If Play 3 also wrote those
configs, it would collide with stow and drift from the user's dotfiles.

## Decision

Play 3 is **config-free**: it installs packages and enables services but writes
**zero** user dotfiles. Each role's final message lists the config paths the
user's stow package must supply (a "stow should provide X" note). The single
exception is `/etc/greetd/config.toml` — a *system service file* for the
display manager, not a user dotfile, so Play 3 (root) writes it from a
template.

## Consequences

The user's stow package remains the single source of truth for all dotfiles;
Play 3 can be re-run freely without touching stow state. Play 3 roles are
deliberately thin (install + service-enable + verify-print), which keeps them
easy to audit and low-risk. A module whose function depends on a config
(e.g. `hyprland-config`, which is package-free) reduces to a printed note —
acceptable because the config is genuinely the user's to author.

---
tags: [ansible, stow, config-ownership, dotfiles, config-boundary, desktop]
---

# ADR-011: Config Ownership — No User Dotfiles from Automation; Named System-Artifact Exception; dotfiles-backup Bootstrap

Status: Accepted
Date: 2026-08-24
Source: docs/specs/005-ansible-play-3-phase-3-desktop-boot-system-selectable-modules-config-free.md

## Context

Play 2 roles write system configuration (snapper config, GRUB, ufw, PipeWire
sockets) because those have no per-user dotfile alternative. Play 3's modules are
almost entirely user-facing desktop tools (Hyprland, waybar, rofi, swaync, kitty,
yazi, zsh) whose behavior is driven by dotfiles the user already maintains via GNU
Stow (the Phase 4 `dotfiles-backup` shared module). If Play 3 also wrote those
configs, it would collide with stow and drift from the user's dotfiles. Phase 4
modules, however, require a few artifacts that are not preference content: the
devpod binary (root-owned, `/usr/local/bin`), the rootless-podman subuid/subgid
range (`/etc/subuid` state), the ufw 8080 rule, and the llama-server user systemd
unit (a service definition whose model list is delegated to the stow-owned
`~/models/config.ini` by path). Options: strict config-free (leaves llama-server
unenableable as a service, which the inference doc's Path B explicitly wants) or
writing configs (collides with stow). The shared `dotfiles-backup` module itself
must create the stow boundary the other roles' notes point at — but its doc's
adopt/move steps (Step 3-5: `stow --adopt`, `git checkout -- .`) are interactive,
user-judgment steps, and `--adopt` can overwrite repo versions.

## Decision

Automation writes **no user dotfiles** — stow owns all config. Play 3 is
**config-free**: it installs packages and enables services but writes zero user
dotfiles; each role's final message lists the config paths the user's stow package
must supply (a "stow should provide X" note). The single Play 3 exception is
`/etc/greetd/config.toml` — a *system service file* for the display manager, not a
user dotfile, so Play 3 (root) writes it from a template.

Play 4 extends this with a **named exception class** ("service unit definitions and
root-owned system artifacts"): it writes exactly four named system-level, non-
dotfile artifacts — the devpod binary, the podman subuid/subgid range, the ufw
8080/tcp rule, and the llama-server.service user unit file — and prints "your stow
package should provide X" notes for everything else. The unit-file role notes that
the user may prefer stow ownership and delete it. The exception class stays closed —
any future Phase 4+ artifact must be classified as either that class or stow-owned,
case by case.

The `dotfiles_backup` role bootstraps the boundary idempotently and non-
destructively: it installs stow (pacman), creates `~/dotfiles` as a git repo only if
it does not already exist (never `git init` over an existing repo), and prints the
naming convention, the suggested stow package list, and the adopt/checkout workflow
as instructions. It moves no files and writes no stow package contents.

## Consequences

The user's stow package remains the single source of truth for all preference
content; Play 3 roles are deliberately thin (install + service-enable + verify-
print), easy to audit and low-risk, and re-runnable without touching stow state; a
module whose function depends on a config (e.g. `hyprland-config`, package-free)
reduces to a printed note — acceptable because the config is genuinely the user's to
author. The inference and devpod modules are fully operable (service enabled, LAN
reachable, binary on PATH) while stow stays authoritative; the stow boundary the
other 18 roles' notes reference is guaranteed to exist after a Play 4 run. Costs:
the duplicate-ownership edge case for the unit file (playbook writes, stow may also
ship it) is resolved by print-not-fail; the user still performs the per-package
adopt/move by hand (exactly the judgment this ADR assigns to the user); an existing
`~/dotfiles` repo with a different layout is left untouched — the role's prints
assume the doc's convention. Follow-up: if the adopt workflow is ever deemed safe to
script (e.g. repo empty, target files untracked), a flag-gated task can extend the
dotfiles_backup role.

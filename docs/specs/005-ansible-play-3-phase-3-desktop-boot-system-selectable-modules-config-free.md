---
tags: [ansible, archlinux, phase-3, desktop, hyprland, wayland]
---

# [005]: Ansible Play 3 — Phase 3 Desktop (Boot-System, Selectable Modules, Config-Free)

Status: APPROVED
Handoff: 2026-08-24
Phase: 1-Plan
Handoff: (pending)

## 1. Goal & Context

Build **Play 3** of the Ansible automation to run **on the booted Arch system**
(post Phase 2) and drive the **Phase 3: Desktop** modules
(`os/archlinux/phase-3-desktop/`). Play 3 installs the **packages and user
services** for a Hyprland-based Wayland desktop.

**Scope = all 14 Phase 3 modules**: `hyprland-install`, `hyprland-config`,
`hyprland-lock`, `hyprland-wallpaper`, `hyprland-screenshare`, `shell-terminal`,
`app-launcher`, `status-bar`, `notifications`, `display-manager`, `clipboard`,
`screenshots`, `file-manager`, `fonts`.

**Critical constraint (user directive): Play 3 does NOT write any dotfiles or
config files.** The end user maintains their own dotfiles via **GNU Stow**
(Phase 4 `dotfiles-backup` module). Play 3's job is to ensure:

1. Every package the modules need is installed (pacman, root).
2. User-level systemd services/sockets that the desktop needs are enabled for
   the end user (`systemctl --user` via the `sudo -u` wrapper, spec 004 D1).
3. A few root-level non-dotfile system artifacts where they are not configs
   (e.g. the `/etc/greetd/config.toml` service file for the display manager —
   this is a system service definition, not a user dotfile).

Everything else — `hyprland.conf`, `waybar/config`, `swaync/style.css`,
`rofi/config.rasi`, `kitty.conf`, `hyprlock.conf`, `hypridle.conf`,
`yazi.toml`, fontconfig user config, etc. — is **owned by the user's stow
package** and is deliberately out of Play 3's scope. Where a module's
functionality depends on a config that stow will provide, Play 3 prints a
"your stow package should provide X" note instead of writing it.

**Why this is different from Play 2:** Play 2's modules are mostly
root-configuration (PipeWire sockets, snapper config, GRUB, ufw) where there is
no "user dotfile" alternative. Play 3's modules are almost entirely
user-facing desktop tools whose behavior is config-driven — and that config is
the user's stow territory. So Play 3 roles are deliberately thin: install +
service-enable + verify-print.

## 2. Architectural Decisions & Trade-offs

- **D1 — One play, `become`-based context split (same as spec 004 D1).**
  Root tasks (pacman, greetd service file) set `become: true`; user-context
  tasks (any `systemctl --user` enables) run via the
  `sudo -u <user> XDG_RUNTIME_DIR=/run/user/<uid> systemctl --user …` wrapper.
  Play 3 has very few user-service enables (most desktop tools are launched by
  Hyprland's `exec-once` from the user's stow config, not by systemd-user), so
  the user-context surface is small: primarily `display-manager` (greetd is a
  system service, root) and possibly nothing else. This keeps the play simple.

- **D2 — Per-module selectability = inventory flag + Ansible tag (same as spec
  004 D2).** Every module role is gated by an `enable_<id>` inventory boolean
  **and** carries its own tag. Flags default to the Phase 3 README
  recommendation: the "Required" and "Recommended" modules on; the "Optional"
  modules off. A bare `make run-phase3` does the sensible set; the user can
  narrow with `--tags` or flip flags.

- **D3 — Window-manager-agnostic data layer (extension of spec 004 D3).**
  A `wm_vendor` inventory var selects the desktop path. **`hyprland` is
  implemented**; `niri`, `sway`, and `none` are **declared but not
  implemented** — they hit a clear "not implemented yet" gate. This mirrors the
  `gpu_vendor` pattern: per-WM package lists live in
  `vars/distros/archlinux.yml` under a `wm:` map, so adding a WM later = data +
  one role branch, no rewrite. Today only the `hyprland` entry has packages.
  The shared (WM-agnostic) modules — shell, launcher, status bar, notifications,
  display manager, clipboard, screenshots, file manager, fonts — are
  **unaffected by `wm_vendor`**; only the 5 `hyprland-*` roles are
  WM-gated.

- **D4 — Config-free: no dotfile writes, printed "stow should provide" notes
  (the core departure from spec 004 D4).** Where a module's docs describe a
  config file, Play 3 does **not** write it. Instead the role's final debug
  message lists the config paths the user's stow package must supply (e.g.
  `hyprland-config` prints "stow should provide
  `~/.config/hypr/hyprland.conf` with keybinds, monitors, window rules"). The
  one exception is a **system service file** that is not a user dotfile:
  `display-manager` writes `/etc/greetd/config.toml` (root, system-level)
  because greetd is a system service with no per-user alternative. This keeps
  the user's stow package as the single source of truth for all dotfiles while
  still letting Play 3 fully enable the display manager. Alternative rejected:
  Play 3 writing configs (collides with stow, drifts from the user's
  dotfiles) or a hybrid (inconsistent ownership).

- **D5 — `hyprland-install` is the prerequisite gate for the other 4
  Hyprland roles.** The 5 `hyprland-*` roles are sequential in the README
  (01→02→03→04→05). Play 3 enforces this at the play level: `hyprland-config`,
  `hyprland-lock`, `hyprland-wallpaper`, and `hyprland-screenshare` each carry
  `when: enable_<id> and (enable_hyprland_install | default(true))` so a user
  cannot enable a downstream Hyprland module without the install. The 9
  shared modules depend only on `hyprland-install` (they need Hyprland running)
  but not on each other, so they run in any order.

- **D6 — Parity checker extends to Phase 3 (same as spec 004 D5).**
  `manifest_to_playbook.py` gains `phase-3` in `PHASE_IDS` and maps each Phase
  3 module id to its role. Package references are checked against the
  roles/vars/group_vars tree as today. This keeps the manifest as single
  source of truth for Phase 3.

- **D7 — No new verification infra; reuse the Play 1/2 harness (same as spec
  004 D6).** Always-on checks stay `ansible-playbook --syntax-check`,
  `yamllint`, `ansible-lint`, and the parity check (now Phase 0–3). Acceptance
  is a documented manual bring-up: run Play 3 with a chosen module set, log in
  to the desktop, and confirm each applied module's verification command
  passes. No CI added.

## 3. Affected Files & Scope

- **Created:**
  - `ansible/playbooks/30-desktop.yml` — **Play 3** (14 module roles, each
    tagged + flag-gated; the 4 downstream Hyprland roles also gated on
    `enable_hyprland_install`).
  - `ansible/roles/hyprland_install/tasks/main.yml` — manifest module
    `hyprland-install`; installs the Hyprland + Wayland + terminal + browser +
    TUI-fm package set (root). No config (first-launch config is stow's job).
  - `ansible/roles/hyprland_config/tasks/main.yml` — manifest module
    `hyprland-config`; **package-free** (config-only module). Prints the stow
    "should provide `hyprland.conf`" note + verification. No packages to
    install, no config written.
  - `ansible/roles/hyprland_lock/tasks/main.yml` — manifest module
    `hyprland-lock`; installs `hyprlock` + `hypridle` (root). Prints stow note
    for `hyprlock.conf` / `hypridle.conf`.
  - `ansible/roles/hyprland_wallpaper/tasks/main.yml` — manifest module
    `hyprland-wallpaper`; installs `swww` (root). Prints stow note for the
    wallpaper autostart + image path.
  - `ansible/roles/hyprland_screenshare/tasks/main.yml` — manifest module
    `hyprland-screenshare`; ensures `xdg-desktop-portal-hyprland` is present
    (already in `hyprland-install`, so this is a no-op install + a
    portal-backend note). Prints the `~/.config/xdg-desktop-portal/portals.conf`
    stow note.
  - `ansible/roles/shell_terminal/tasks/main.yml` — manifest module
    `shell-terminal`; installs `zsh oh-my-zsh fzf zoxide` (root) + sets the
    end user's login shell to zsh (`chsh`, root). Prints stow note for
    `~/.zshrc` + `~/.config/kitty/kitty.conf`.
  - `ansible/roles/app_launcher/tasks/main.yml` — manifest module
    `app-launcher`; installs `rofi-wayland` (root). Prints stow note for
    `~/.config/rofi/config.rasi`.
  - `ansible/roles/status_bar/tasks/main.yml` — manifest module `status-bar`;
    installs `waybar` (root). Prints stow note for `~/.config/waybar/`.
  - `ansible/roles/notifications/tasks/main.yml` — manifest module
    `notifications`; installs `swaync mako` (root). Prints stow note for
    `~/.config/swaync/`.
  - `ansible/roles/display_manager/tasks/main.yml` — manifest module
    `display-manager`; installs `greetd tuigreet` (root), writes
    `/etc/greetd/config.toml` (system service file — the one non-dotfile
    artifact, D4), enables the `greetd` system service.
  - `ansible/roles/clipboard/tasks/main.yml` — manifest module `clipboard`;
    installs `wl-clipboard clipse` (root). Prints stow note for the clipse
    `exec-once` + keybind in `hyprland.conf`.
  - `ansible/roles/screenshots/tasks/main.yml` — manifest module
    `screenshots`; installs `grim slurp swappy` (root). Prints stow note for
    the screenshot keybinds in `hyprland.conf`.
  - `ansible/roles/file_manager/tasks/main.yml` — manifest module
    `file-manager`; installs `thunar thunar-archive-plugin thunar-vcs-plugin`
    (root). Yazi is already in `hyprland-install`. Prints stow note for
    `~/.config/yazi/yazi.toml`.
  - `ansible/roles/fonts/tasks/main.yml` — manifest module `fonts`; installs
    `fontconfig noto-fonts noto-fonts-cjk noto-fonts-emoji
    ttf-jetbrainsmono-nerd ttf-material-design-icons` (root) + runs
    `fc-cache -fv`. Prints stow note for optional
    `~/.config/fontconfig/fonts.conf`.
  - `ansible/templates/greetd-config.toml.j2` — the single template Play 3
    writes (the greetd system service file, parameterized by `end_user` and
    the WM session command).

- **Modified:**
  - `ansible/inventory/hosts.yml` — add Phase 3 vars: `wm_vendor: hyprland` and
    the 14 `enable_<id>` flags with README-recommended defaults (Required +
    Recommended on, Optional off).
  - `ansible/vars/distros/archlinux.yml` — add a `wm:` map (hyprland
    implemented; niri/sway/none declared empty) holding the per-WM base package
    list, and per-module package lists for the 9 shared modules
    (`shell_terminal`, `app_launcher`, `status_bar`, `notifications`,
    `display_manager`, `clipboard`, `screenshots`, `file_manager`, `fonts`).
  - `ansible/generators/manifest_to_playbook.py` — `PHASE_IDS +=
    ("phase-3",)`; `ROLE_MAP` entries for the 14 Phase 3 module ids.
  - `ansible/Makefile` — add `run-phase3` target (`ansible-playbook
    playbooks/30-desktop.yml`); extend `syntax` to check `30-desktop.yml`.
  - `ansible/README.md` — document the Play 3 user flow (post Phase 2, log in
    as user, `make run-phase3`, pick modules via flags/tags, per-module
    verification) and the **config-free / stow** boundary.
  - `os/archlinux/phase-3-desktop/README.md` — add a pointer to the `ansible/`
    Play 3 automation companion (mirrors the Phase 0–1 and Phase 2 pointers).

- **Deleted:** none

- **Out of scope (stow-owned, explicitly NOT touched by Play 3):** every user
  dotfile and per-tool config — `~/.config/hypr/hyprland.conf`,
  `~/.config/hyprlock/`, `~/.config/hypridle/`, `~/.config/waybar/`,
  `~/.config/rofi/`, `~/.config/swaync/`, `~/.config/kitty/`,
  `~/.config/yazi/`, `~/.config/fontconfig/`, `~/.zshrc`, and the wallpaper
  image files.

## 4. Actionable TODO Checklist

- [ ] Step 1: Extend `ansible/vars/distros/archlinux.yml` with the `wm:` map
      (hyprland implemented with its base package list; niri/sway/none declared
      empty) + per-module package lists for the 9 shared modules.
- [ ] Step 2: Add Phase 3 vars to `ansible/inventory/hosts.yml` (`wm_vendor` +
      the 14 `enable_*` flags with recommended defaults).
- [ ] Step 3: Implement `roles/hyprland_install` (module `hyprland-install`):
      install the WM base packages from the `wm` map (root); no config.
- [ ] Step 4: Implement `roles/hyprland_config` (module `hyprland-config`):
      package-free; print the stow "provide hyprland.conf" note + verification.
- [ ] Step 5: Implement `roles/hyprland_lock` (module `hyprland-lock`): install
      hyprlock + hypridle; print stow note.
- [ ] Step 6: Implement `roles/hyprland_wallpaper` (module
      `hyprland-wallpaper`): install swww; print stow note.
- [ ] Step 7: Implement `roles/hyprland_screenshare` (module
      `hyprland-screenshare`): ensure portal package; print portals.conf stow
      note.
- [ ] Step 8: Implement `roles/shell_terminal` (module `shell-terminal`):
      install zsh/oh-my-zsh/fzf/zoxide; `chsh` to zsh for end_user; print stow
      note for .zshrc + kitty.conf.
- [ ] Step 9: Implement `roles/app_launcher` (module `app-launcher`): install
      rofi-wayland; print stow note.
- [ ] Step 10: Implement `roles/status_bar` (module `status-bar`): install
      waybar; print stow note.
- [ ] Step 11: Implement `roles/notifications` (module `notifications`):
      install swaync + mako; print stow note.
- [ ] Step 12: Implement `roles/display_manager` (module `display-manager`):
      install greetd + tuigreet; write `/etc/greetd/config.toml` from template;
      enable the greetd service.
- [ ] Step 13: Implement `roles/clipboard` (module `clipboard`): install
      wl-clipboard + clipse; print stow note.
- [ ] Step 14: Implement `roles/screenshots` (module `screenshots`): install
      grim + slurp + swappy; print stow note.
- [ ] Step 15: Implement `roles/file_manager` (module `file-manager`): install
      thunar + plugins; print stow note for yazi.
- [ ] Step 16: Implement `roles/fonts` (module `fonts`): install font packages;
      `fc-cache -fv`; print stow note.
- [ ] Step 17: Create `ansible/templates/greetd-config.toml.j2`.
- [ ] Step 18: Create `ansible/playbooks/30-desktop.yml` wiring the 14 roles,
      each tagged + flag-gated; the 4 downstream Hyprland roles also gated on
      `enable_hyprland_install`.
- [ ] Step 19: Extend `generators/manifest_to_playbook.py` (PHASE_IDS phase-3,
      ROLE_MAP for the 14 ids); update `Makefile` (`run-phase3`, syntax check
      for 30-desktop.yml).
- [ ] Step 20: Update `ansible/README.md` (Play 3 flow + config-free/stow
      boundary) + Phase 3 README pointer.
- [ ] Step 21: Run `make lint syntax check` (Phase 0–3 parity green) and a
      `--syntax-check` on `30-desktop.yml`; document the manual bring-up.

## 5. Verification Commands

- Lint: `make lint` (yamllint + ansible-lint over playbooks/ + roles/)
- Syntax: `ansible-playbook --syntax-check playbooks/30-desktop.yml`
- Parity: `python3 generators/manifest_to_playbook.py --check --manifest
  ../os/archlinux/manifest.yaml` (now covers Phase 0–3: every Phase 3 module id
  has a role; every Phase 3 package is referenced)
- Selectability smoke: `ansible-playbook playbooks/30-desktop.yml --list-tasks
  --tags hyprland-install` shows only that role; a run with
  `enable_display_manager: false` skips it.
- Prerequisite smoke: a run with `enable_hyprland_install: false` and
  `enable_hyprland_lock: true` skips hyprland-lock (D5 gate).
- Manual bring-up (real machine, post Phase 2): log in as `end_user`,
  `make run-phase3` with a chosen module set, then for each applied module run
  its docs' verification (e.g. `fc-list | wc -l`, `rofi -show drun`,
  `swaync-client -t`, `systemctl status greetd`, `Hyprland` launches,
  `wl-copy`/`wl-paste`, `grim` capture).

## 6. Rollback Strategy

Play 3 is additive and package-centric; rollback is per-module package removal
+ (for display-manager) service disable + config-file delete. No user dotfiles
are ever written, so stow state is never disturbed.

- **hyprland-install:** `sudo pacman -Rns hyprland wayland
  xdg-desktop-portal-hyprland kitty qt5-wayland qt6-wayland firefox yazi`
- **hyprland-config:** no packages, no files — nothing to roll back.
- **hyprland-lock:** `sudo pacman -Rns hyprlock hypridle`
- **hyprland-wallpaper:** `sudo pacman -Rns swww`
- **hyprland-screenshare:** package already from hyprland-install; no separate
  removal (only the stow portals.conf, which stow owns).
- **shell-terminal:** `sudo pacman -Rns zsh oh-my-zsh fzf zoxide`;
  `sudo chsh -s /bin/bash <user>` to restore the previous shell.
- **app-launcher:** `sudo pacman -Rns rofi-wayland`
- **status-bar:** `sudo pacman -Rns waybar`
- **notifications:** `sudo pacman -Rns swaync mako`
- **display-manager:** `sudo systemctl disable --now greetd`;
  `sudo rm /etc/greetd/config.toml`; `sudo pacman -Rns greetd tuigreet`
- **clipboard:** `sudo pacman -Rns wl-clipboard clipse`
- **screenshots:** `sudo pacman -Rns grim slurp swappy`
- **file-manager:** `sudo pacman -Rns thunar thunar-archive-plugin
  thunar-vcs-plugin` (yazi removal is part of hyprland-install)
- **fonts:** `sudo pacman -Rns fontconfig noto-fonts noto-fonts-cjk
  noto-fonts-emoji ttf-jetbrainsmono-nerd ttf-material-design-icons`;
  `fc-cache -fv`

If the parity checker or lint fails 3× on the same change, revert that file to
its pre-change state (git) and re-derive from the manifest — the manifest is the
source of truth, so a green `make check` is the recovery target.

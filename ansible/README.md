# Ansible — Plays 1–4: Install, Hardening, Desktop, Workflow (Phase 0–4)

Four plays automate the Arch Linux build:

- **Play 1** (`playbooks/10-install.yml`) — Live-USB install through first
  reboot (Phase 0–1): Phase 0 verification gate, then Phase 1 modules 01–09,
  ending in a reboot into a bootable dual-boot CLI system (GRUB menu with
  Linux + Windows).
- **Play 2** (`playbooks/20-hardening.yml`) — Phase 2 system hardening on the
  booted system (selectable modules: NVIDIA, snapshots, AUR, PipeWire, …).
- **Play 3** (`playbooks/30-desktop.yml`) — Phase 3 desktop on the booted
  system (selectable, **config-free** modules: Hyprland + desktop tools; all
  dotfiles are owned by the user's stow package).
- **Play 4** (`playbooks/40-workflow.yml`) — Phase 4 workflow on the booted
  system (profile-selectable modules: dev / ai / gaming / creative + shared
  dotfiles-backup; **system-level only** — dotfiles stay stow-owned).

The module/package source of truth is
[`os/archlinux/manifest.yaml`](../os/archlinux/manifest.yaml); the generator
parity check keeps the two from drifting.

## User Flow

1. **Phase 0 (manual, pre-Linux)** — follow
   [`os/archlinux/phase-0-pre-install/`](../os/archlinux/phase-0-pre-install/README.md):
   BIOS Secure Boot off, Windows Fast Startup off, flash the USB, boot in UEFI mode.
2. **On the live USB**, install the tooling:

   ```bash
   pacman -S git ansible
   git clone <this-repo-url> ~/new-pc-install
   cd ~/new-pc-install/ansible
   ```

3. **Set your drive** in `inventory/hosts.yml` — the single "place to put the
   drive". Identify it first:

   ```bash
   lsblk -o NAME,SIZE,MODEL
   ```

   Set `target_drive` (e.g. `nvme1n1`), `target_drive_model` (e.g. `SAMSUNG`),
   and `target_drive_size` (e.g. `1T`). These are validated before anything is
   written.
4. **Run Play 1** with the destructive gate flag:

   ```bash
   make run
   # or: ansible-playbook playbooks/10-install.yml --confirm-destructive
   ```

    The play will halt before writing any GPT table unless `--confirm-destructive`
    is present. You will be prompted for the root and end-user passwords
    (see **Passwords** below).
5. **Reboot** — the play ends in `reboot`. Remove the USB when the system
   powers off. Confirm the GRUB menu shows **Arch Linux** and
   **Windows Boot Manager**, boot Linux, log in as your user, and check
    `ping archlinux.org`, `findmnt -t btrfs`, `ls /sys/firmware/efi`.

## Play 3 User Flow (Phase 3 Desktop, config-free)

After Phase 2 (a stable system with NVIDIA drivers + PipeWire), log in as
`end_user` and run:

```bash
make run-phase3
# or: ansible-playbook playbooks/30-desktop.yml
```

Play 3 installs the **packages and services** for a Hyprland Wayland desktop.
It is **config-free** (spec 005, ADR-011): it writes **no user dotfiles** —
every `hyprland.conf`, `waybar/`, `rofi/`, `swaync/`, `kitty.conf`, `yazi.toml`,
`.zshrc`, and the wallpaper image is owned by the user's **stow** package. The
single exception is `/etc/greetd/config.toml` (a *system service file* for the
display manager, not a dotfile), which Play 3 writes and enables.

- **Modules are selectable** two ways (spec 005 D2): the `enable_<id>` flags in
  `inventory/hosts.yml` (Recommended default on, Optional off), or `--tags
  <id>` at run time. Example: `--tags fonts,shell-terminal`.
- **Window manager** — `wm_vendor: hyprland` (only `hyprland` is implemented;
  `niri`/`sway`/`none` hit a "not implemented" gate). Only the 5 `hyprland-*`
  roles are WM-gated; the 9 shared modules are WM-agnostic.
- **Prerequisite gate** — the 4 downstream Hyprland roles (`config`, `lock`,
  `wallpaper`, `screenshare`) only run when `enable_hyprland_install` is also
  true (spec 005 D5).
- **After the play**: log in to the desktop (or reboot for greetd) and run each
  applied module's verification from its docs (e.g. `hyprland --version`,
  `rofi -show drun`, `swaync-client -t`, `systemctl status greetd`,
  `fc-list | wc -l`, `wl-copy`/`wl-paste`).

## Play 4 User Flow (Phase 4 Workflow, system-level only)

After Phase 3 (a desktop you log into), still logged in as `end_user` (wheel),
run:

```bash
make run-phase4
# or: ansible-playbook playbooks/40-workflow.yml
```

Play 4 installs the **packages, user services, and system-level artifacts**
for the Phase 4 workflow modules (see
[`os/archlinux/phase-4-workflow/`](../os/archlinux/phase-4-workflow/README.md)).
It is **system-level only** (spec 006, ADR-011): like Play 3 it writes **no
user dotfiles** — the one exception class is *service unit definitions and
root-owned system artifacts*, of which Play 4 writes exactly four:

1. `/usr/local/bin/devpod` (devpod module, binary download),
2. the end user's subuid/subgid range (containers module, `usermod`),
3. the `ufw allow 8080/tcp` rule (inference module),
4. `~/.config/systemd/user/llama-server.service` (inference module — a
   *service definition*, not a config file; the role prints that you may
   prefer stow to own it).

Everything else in the Phase 4 docs (`~/.ssh/config`, `~/models/config.ini`,
`opencode.json`, neovim specs, aliases, …) is printed as a "your stow package
should provide X" note — the shared `dotfiles-backup` module sets up that
stow + git-repo boundary (GNU Stow, `~/dotfiles`; it never moves your
existing configs).

**Module selection** — three ways (spec 006 D1):

- **Profile vars** (the ergonomic default): `profile_dev`, `profile_ai`,
  `profile_creative`, `profile_gaming` in `inventory/hosts.yml`. A profile on
  enables all of its modules (default: dev + ai on; gaming + creative off).
- **Per-module flags**: the 18 `enable_<id>` flags (all default `false`; the
  profile vars drive selection). For per-module control, set your `profile_*`
  vars to `false` and flip individual flags. Note the OR-semantics: a module
  cannot be switched *off* while its profile is *on* — narrow at run time with
  `--tags` instead.
- **Tags**: `--tags <id>` at run time (ids: `containers`, `devpod`,
  `inference`, `agents`, …, plus the shared `dotfiles-backup`).

Prerequisite gates: `devpod` needs `containers` (podman as its provider);
`agents` needs `inference` (llama-server). The `yay` AUR helper must exist
(installed by Play 2 with `enable_aur: true`) before Play 4 runs — the pre-task
gate fails with a clear message otherwise.

**Model downloads are opt-in** (spec 006 D5): set `enable_ai_models: true` to
have the inference/agents roles `wget -c` the GGUFs into `~/models/`
(tens of GB); default off, so a normal run never fetches models. `inference`
always creates `~/models/` and the llama-server service; the model preset
(`~/models/config.ini`) is stow-owned.

**Placeholder modules** (spec 006 D3): 12 of the 18 Phase 4 docs are
placeholders. Their roles are *thin* — they install only the packages their
manifest entry lists (steam, mangohud, obs-studio, mpv, neovim, podman) and
print a "doc is a placeholder — manual steps pending" note. No playbook
redesign is needed when the docs are filled in later.

**After the play** (manual bring-up): run each applied module's verification
from its docs — e.g. `stow --version` + `ls -la ~/dotfiles/.git`
(dotfiles-backup), `podman run --rm hello-world` + `lazypodman` (containers),
`devpod list` (devpod), `nvim --version` (neovim),
`llama-server --version` + `systemctl --user status llama-server.service` +
`curl -s http://127.0.0.1:8080/v1/models` (inference), `npm ls -g` (harness),
`which claude-desktop` (agents), `steam --version` (steam), `mangohud
--version` (mangohud), `obs --version` (obs), `mpv --version`
(media-players).

## Safety Gates

- **Destructive gate** — no GPT table is written without `--confirm-destructive`.
- **Drive validation** — `target_drive` must be present and match
  `target_drive_model` / `target_drive_size` before the gate is reached.
- **Phase 1 module 01 gate** — the `verify_boot_network` role asserts UEFI
  mode, internet, and NTP up front; any failure halts with a clear message.
- **Selectable layout** — `fstype` (only `btrfs` implemented) gates the
  btrfs-specific checks in `filesystems_btrfs`, `system_config`, and
  `first_reboot`; `bootloader` (only `grub` implemented) is the same pattern
  for the bootloader role.
- Re-runs are safe from the live USB: the play re-partitions and re-pacstraps
  from scratch (idempotent recovery path).

## Distro Selection (Option A: distros as data)

The **inventory group the host is under** selects the distro (ADR-002).
`localhost` sits in the `archlinux` group (`all:` → `archlinux:` → `hosts:` →
`localhost:`), which auto-loads `inventory/group_vars/archlinux.yml` — the
per-distro package names, commands, paths, and layout constants (btrfs layout,
gdisk hex codes, sudo group/shell, and the variant-module maps). To run a
different distro, move the host under a different group (e.g. `ubuntu:`) that
has its own `group_vars/<distro>.yml` file. Adding a distro is a new group +
a data file — no role rewrites. Only `archlinux.yml` exists in this spec
(Phase 0–1 scope). The old `ansible_distro` var and the `vars/distros/` folder
are retired.

## Passwords (spec 003)

`root_password` and `end_user_password` are per-machine inventory vars with
pre-fill semantics:

- **Non-empty value** → used as-is; the keyboard prompt is skipped.
- **Empty (`""`) or absent** → the play prompts interactively.
- **Enter at the prompt** → that password is left unset for now.

Both are applied via `chroot chpasswd` with `no_log: true`. Prefer the
prompt for a fresh install; the inventory pre-fill exists for re-runs and
automation.

## Var Layering (spec 002 / ADR-002 / ADR-002 / ADR-002: single source of truth)

One rule for where values live:

- **Per-machine values** → `inventory/hosts.yml` (`target_drive*`,
  `hostname`, `timezone`, `locale`, `end_user`, `country`, `efi_size`,
   `swap`, `swap_size`, `fstype`, `bootloader`, `root_password`,
   `end_user_password`). The host's **group** is also its distro selector
  (ADR-002) — `localhost` is under `archlinux:`.
- **Static shared layout constants** → `inventory/group_vars/all.yml`
  (`mount_point`, `efi_dir` — the UEFI efivars path — and the
  `confirm_destructive` gate), auto-loaded for every host.
- **Distro-specific data** (packages/commands/paths/btrfs/gdisk/sudo + the
  variant-module maps) → `inventory/group_vars/<distro>.yml`, auto-loaded
  when the host is in the `<distro>` group (the group is the selector;
  `ansible_distro` is retired).
- **Role-local policy that is not a distro fact** (e.g. btrfs-gated snapper
  retention) → `roles/<r>/vars/<name>.yml` (auto-loaded by Ansible).

Roles reference these keys directly; no `roles/*/defaults/<distro>.yml`
files remain, no per-role `include_vars` of a distro file is used, and no
play-level `include_vars` loads the distro data — both the static and the
distro layers arrive via standard `group_vars/` auto-load.

### Variant-module data pattern (ADR-002)

Two module shapes, both read from the global distro file:

- **Simple** — `distro_packages.<module>` (a flat package list), e.g.
  `distro_packages.base`, `distro_packages.bootloader`.
- **Variant** — a top-level `<role>:` section keyed by a host var, each
  variant carrying `packages` plus a **`config` keyword**. The keyword
  resolves to `roles/<r>/vars/<kw>.yml` (lookup data) and optionally
  `roles/<r>/templates/<kw>.*.j2` (a file rendered with `{{ }}` to a real
  system file). A `<variant>: none` or absent host var makes the role skip —
  the same gate as the `gpu:` map (ADR-003/ADR-004), which is the first
  (two-selector nested) instance of this pattern. Single-selector variant
  modules (e.g. the planned `wifi`) are flat: `wifi: { <variant>: { packages,
  config } }`.

**vars/ vs templates/ split** — by content type, not per module: data looked
up inside a task → `roles/<r>/vars/` (`.yml`); a file rendered with `{{ }}` to
a real system file → `roles/<r>/templates/` (`.j2`); never a `.j2` in
`vars/`.

## Verification (always-on, no CI)

```bash
make lint       # yamllint + ansible-lint
make syntax     # ansible-playbook --syntax-check (Plays 1-4)
make check      # manifest <-> playbook parity (exit 0 iff in sync, Phases 0-4, profile-aware)
make run-phase3 # Play 3: Phase 3 desktop (booted system, config-free)
make run-phase4 # Play 4: Phase 4 workflow (booted system, system-level only)
```

Acceptance = the manual bring-up above: Play 1 reboots into a GRUB menu showing
both Linux and Windows; Play 2/3/4 each leave their applied modules'
verification commands passing.

## Layout

```
ansible/
├── ansible.cfg
├── inventory/hosts.yml            # per-machine values: drive, identity, layout, swap, fstype, bootloader, passwords, country, wm + enable_* flags; host is under the distro group (selector)
├── inventory/group_vars/all.yml         # static shared constants: mount_point, efi_dir, gate (auto-loaded, every host)
├── inventory/group_vars/archlinux.yml   # Option A distro layer (packages/commands/paths/layout + wm map + per-module pkgs + variant maps); auto-loaded when host is in the `archlinux` group (ADR-002)
├── playbooks/10-install.yml   # Play 1: verify_boot_network -> modules 01-09 -> reboot
├── playbooks/20-hardening.yml # Play 2: Phase 2 selectable modules (booted system)
├── playbooks/30-desktop.yml   # Play 3: Phase 3 selectable desktop modules (booted system, config-free)
├── playbooks/40-workflow.yml  # Play 4: Phase 4 profile-selectable modules (booted system, system-level only)
├── templates/llama-server.service.j2  # the only template Play 4 writes (inference user unit)
├── roles/
│   ├── verify_boot_network/   # 01 (UEFI, Wi-Fi, connectivity, NTP)
│   ├── partitioning/          # 02 (detect-all fact, validation, gate, gdisk template)
│   ├── filesystems_btrfs/     # 03 (mkfs, subvolumes, mounts)
│   ├── install_base/          # 04 (reflector, keyring, pacstrap -K /mnt)
│   ├── system_config/         # 05 (genfstab; chroot: timezone, locale, hostname, NM)
│   ├── users_sudo/            # 06 (user + sudoers.d drop-in, chroot-stage)
│   ├── gpu/                   # 07 (NVIDIA driver in chroot: multilib, KMS cmdline, mkinitcpio, hook)
│   ├── bootloader_grub/       # 08 (grub, mkconfig, os-prober, efibootmgr)
│   ├── first_reboot/          # 09 (final checks, unmount, reboot)
│   ├── snapshots/             # Play 2 (snapper + snap-pac + grub-btrfs); vars/snapshots_retention.yml = role-local policy
│   ├── aur/ sound/ networking/ clock_sync/ firewall/ external_drives/ ssh_git/  # Play 2
│   ├── hyprland_install/ hyprland_config/ hyprland_lock/ hyprland_wallpaper/ hyprland_screenshare/  # Play 3 (WM)
│   ├── shell_terminal/ app_launcher/ status_bar/ notifications/ clipboard/ screenshots/ file_manager/ fonts/  # Play 3 (shared)
│   ├── display_manager/  # Play 3 (shared); templates/greetd-config.toml.j2 = only file Play 3 writes
│   ├── dotfiles_backup/  # Play 4 (shared): stow + ~/dotfiles git bootstrap (config-free)
│   ├── dev_neovim/ dev_containers/ dev_devpod/ dev_languages/ dev_api_testing/  # Play 4 (dev profile)
│   ├── ai_inference/ ai_harness/ ai_ide_integration/ ai_agents/ ai_training/  # Play 4 (ai profile)
│   ├── gaming_steam/ gaming_proton/ gaming_heroic/ gaming_mangohud/ gaming_controllers/  # Play 4 (gaming profile)
│   └── creative_obs/ creative_davinci_resolve/ creative_media_players/  # Play 4 (creative profile)
└── generators/manifest_to_playbook.py  # parity checker (Phases 0-4, profile-aware)
```

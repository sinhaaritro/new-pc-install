---
tags: [ansible, archlinux, phase-2, hardening, gpu, btrfs, pipewire]
---

# [004]: Ansible Play 2 — Phase 2 System Hardening (Boot-System, Selectable Modules)

Status: APPROVED
Phase: 2-Build
Handoff: 2026-08-23

## 1. Goal & Context

Build **Play 2** of the Ansible automation to run **on the booted Arch system** (post
Phase 1 first-reboot) and drive the **Phase 2: System Hardening** modules
(`os/archlinux/phase-2-system-hardening/`). Unlike Play 1 (live-USB, root@archiso,
fixed order), Phase 2 is **flexible** — modules have no hard ordering (except NVIDIA
should precede Phase 3) and the user **picks and chooses** which to apply. Play 2
therefore runs each module as an **individually selectable unit** (inventory flag +
Ansible tag) on the live system, mixing **root** and **regular-user** contexts in a
**single play**.

Scope = all 9 Phase 2 modules: `nvidia`, `snapshots`, `aur`, `sound`, `networking`,
`clock-sync`, `firewall`, `external-drives`, `ssh`. The **GPU module is
vendor-agnostic and expandable**: `nvidia` is fully implemented; `amd`, `intel`, and
`none` are first-class options (data + role branch, **no driver code** yet) so later
specs add them without a rewrite.

## 2. Architectural Decisions & Trade-offs

- **D1 — One play, `become`-based context split (not two plays).** Phase 2 runs on the
  *booted* system as the normal user (in `wheel`), so a single play covers both
  contexts: root tasks set `become: true`; user-context tasks (`aur`, `ssh`, and the
  PipeWire user sockets in `sound`) run as the user with `become: false`. The one thing
  Ansible cannot express natively — `systemctl --user` — is handled by a small
  `shell` task wrapping `sudo -u <user> XDG_RUNTIME_DIR=/run/user/<uid> systemctl --user …`
  (the user is already logged in, so `XDG_RUNTIME_DIR` exists). Alternative rejected:
  two plays (20a root / 20b user) — doubles inventory/runs for a split that is shallow
  (only `aur`, `ssh`, and `sound` user-sockets truly need user context).
- **D2 — Per-module selectability = inventory flag + Ansible tag.** Every module role
  is gated by an `enable_<id>` inventory boolean **and** carries its own tag, so the
  user can skip modules two ways: set `enable_x: false` in inventory, or run with
  `--tags nvidia,sound`. Flags default to the README recommendation (the 5 "Recommended"
  modules on; the 4 "Optional" off) so a bare run does the sensible set. Alternative
  rejected: tags-only (no persistent per-machine intent) or a hard-coded recommended
  set (no flexibility).
- **D3 — GPU module is vendor-agnostic (Option A extension).** A `gpu_vendor`
  inventory var (`nvidia` | `amd` | `intel` | `none`) selects the path. `nvidia` and
  `none` are implemented (none = no-op with a note); `amd` and `intel` are
  **declared but not implemented** — they hit a clear "not implemented yet" gate. All
  per-vendor values (package lists, mkinitcpio modules, GRUB cmdline, hook content)
  live in `vars/distros/archlinux.yml` under a `gpu:` map, so adding a vendor = data +
  one task branch, no role rewrite. This mirrors the existing `fstype`/`bootloader`
  selectable pattern from spec 003 and the `cpu_vendor` microcode pattern from spec 002.
  Alternative rejected: a separate role per vendor (N-fold role sprawl before a second
  vendor has real code).
- **D4 — Interactive/manual steps become explicit gates + printed artifacts, never
  silent guesses.** Personal data (SSH email, passphrase, git identity) is read via
  prompt vars (no_log) or a clear "please add this key" printout of the public key +
  GitHub instructions; machine-external steps (Windows UTC registry, Bluetooth
  pairing, USB plug-in test) are **executed where scriptable** (Linux side) and the
  OS-external remainder is printed as an instruction for the user to verify in the
  docs. The SSH public key is always printed so the docs' "how to get the key for
  GitHub" section is satisfied. Alternative rejected: auto-generating a passphrase-less
  key / fabricating an email (security + correctness risk).
- **D5 — Parity checker extends to Phase 2.** `manifest_to_playbook.py` gains Phase 2
  in `PHASE_IDS` and maps each Phase 2 module id to its role (GPU module id `nvidia`
  maps to the `gpu` role, which references the manifest id). Package references are
  checked against the roles/vars/group_vars tree as today. This keeps the manifest as
  single source of truth for Phase 2, exactly as for Phase 0–1 (spec 001 D1).
- **D6 — No new verification infra; reuse Play 1's harness.** Always-on checks stay
  `ansible-playbook --syntax-check`, `yamllint`, `ansible-lint`, and the parity check
  (now Phase 0–2). Acceptance is a documented manual bring-up on the real machine:
  run Play 2 with a chosen module set, confirm each applied module's verification
  command passes. No CI added (repo has none today, spec 001 D6).

## 3. Affected Files & Scope

- Created:
  - `ansible/playbooks/20-hardening.yml` — **Play 2** (9 module roles, each tagged +
    flag-gated; runs on the booted system).
  - `ansible/roles/gpu/tasks/main.yml` (+ `templates/`) — manifest module `nvidia`;
    `gpu_vendor`-selectable. Implements `nvidia` (multilib, packages, GRUB cmdline,
    mkinitcpio MODULES/HOOKS, pacman hook, mkinitcpio -P, grub-mkconfig with Win-EFI
    auto-mount) and `none` (no-op). `amd`/`intel` → "not implemented" gate.
  - `ansible/roles/snapshots/tasks/main.yml` — manifest module `snapshots`; snapper
    create-config, delete auto-subvol + remount `@snapshots`, retention/ACL config,
    timers, mkinitcpio `grub-btrfs-overlayfs` hook, `50-bootbackup.hook`.
  - `ansible/roles/aur/tasks/main.yml` — manifest module `aur`; user-context `git clone
    yay` + `makepkg -si`.
  - `ansible/roles/sound/tasks/main.yml` — manifest module `sound`; root `pacman -S`
    stack + user-context PipeWire/WirePlumber sockets via the `sudo -u` wrapper.
  - `ansible/roles/networking/tasks/main.yml` — manifest module `networking`; `pacman -S
    bluez…`, enable bluetooth, `yay -S wlctl-bin` (user); BT pairing + `wlctl` printed
    as user-verification instructions.
  - `ansible/roles/clock_sync/tasks/main.yml` — manifest module `clock-sync`;
    `timedatectl set-ntp true` + printed Windows-UTC registry instruction.
  - `ansible/roles/firewall/tasks/main.yml` — manifest module `firewall`; ufw install,
    default rules, enable, optional ssh rule.
  - `ansible/roles/external_drives/tasks/main.yml` — manifest module `external-drives`;
    pkgs install; fstab entry only when `drive_uuid`+`drive_mount` provided, else
    printed instruction; USB test = user verification.
  - `ansible/roles/ssh_git/tasks/main.yml` — manifest module `ssh`; `pacman -S openssh`
    (root), user keygen (prompt email/passphrase), agent, git config (prompt
    name/email), **print public key + GitHub instructions**.
  - `ansible/roles/*/defaults/archlinux.yml` — per-role Arch values (packages, paths,
    hook content) sourced from the manifest.
  - `ansible/templates/` — `nvidia.hook.j2`, `50-bootbackup.hook.j2`, `snapper-root.j2`
    (retention/ACL block), `fstab-drive.j2` as needed.
- Modified:
  - `ansible/inventory/hosts.yml` — add Phase 2 vars: `gpu_vendor: nvidia`,
    `enable_nvidia/snapshots/aur/sound/ssh: true`, `enable_networking/clock-sync/
    firewall/external-drives: false`; optional `git_name`, `git_email`, `ssh_email`,
    `ssh_passphrase` (empty = prompt), `firewall_allow_ssh`, `drive_uuid`,
    `drive_mount`.
  - `ansible/vars/distros/archlinux.yml` — add `gpu:` map (per-vendor packages,
    mkinitcpio modules, grub params, hook), `snapshots:` packages/paths, `sound:`,
    `networking:`, `firewall:`, `external_drives:`, `ssh:` package lists.
  - `ansible/generators/manifest_to_playbook.py` — `PHASE_IDS += ("phase-2",)`;
    `ROLE_MAP` entries for the 9 Phase 2 module ids (`nvidia → gpu`, `snapshots →
    snapshots`, `aur → aur`, `sound → sound`, `networking → networking`, `clock-sync →
    clock_sync`, `firewall → firewall`, `external-drives → external_drives`, `ssh →
    ssh_git`).
  - `ansible/Makefile` — add `run-phase2` target (`ansible-playbook
    playbooks/20-hardening.yml`) and extend `check` (parity now Phase 0–2).
  - `ansible/README.md` — document the Play 2 user flow (log in as user → run
    `make run-phase2` → pick modules via flags/tags → per-module verification).
  - `os/archlinux/phase-2-system-hardening/README.md` — add a pointer to the `ansible/`
    Play 2 automation companion (mirrors the Phase 0–1 pointer).
  - `os/archlinux/phase-2-system-hardening/ssh.md` — add a short "Get your SSH key for
    GitHub" note (key path + that Play 2 prints it).
  - `os/archlinux/manifest.yaml` — **no change** (modules/packages already correct);
    the parity checker now reads Phase 2 from it.
- Deleted: none

## 4. Actionable TODO Checklist

- [ ] Step 1: Extend `ansible/vars/distros/archlinux.yml` with the `gpu:` map
      (nvidia implemented; amd/intel/none declared) + `snapshots/sound/networking/
      firewall/external_drives/ssh` package & path lists.
- [ ] Step 2: Add Phase 2 vars to `ansible/inventory/hosts.yml` (gpu_vendor, the 9
      `enable_*` flags with recommended defaults, optional identity/drive/firewall vars).
- [ ] Step 3: Implement `roles/gpu` (module `nvidia`): vendor gate, nvidia path
      (multilib → packages → GRUB cmdline → mkinitcpio MODULES/HOOKS → pacman hook
      template → mkinitcpio -P → Win-EFI mount + grub-mkconfig), `none` no-op,
      amd/intel not-implemented gate.
- [ ] Step 4: Implement `roles/snapshots` (module `snapshots`): pkgs, snapper
      create-config + auto-subvol swap, retention/ACL (substitute end_user), timers,
      mkinitcpio hook, boot backup hook template.
- [ ] Step 5: Implement `roles/aur` (module `aur`, user-context): clone yay +
      `makepkg -si`.
- [ ] Step 6: Implement `roles/sound` (module `sound`): root pkgs + user sockets via
      `sudo -u` XDG_RUNTIME_DIR wrapper.
- [ ] Step 7: Implement `roles/networking` (module `networking`): bluez pkgs + enable,
      `yay -S wlctl-bin`; print `wlctl`/BT-pairing verification instructions.
- [ ] Step 8: Implement `roles/clock_sync` (module `clock-sync`): NTP enable + print
      Windows-UTC registry instruction.
- [ ] Step 9: Implement `roles/firewall` (module `firewall`): ufw install, defaults,
      enable, optional ssh rule.
- [ ] Step 10: Implement `roles/external_drives` (module `external-drives`): pkgs;
      fstab entry when drive vars set, else instruction; USB test = user verify.
- [ ] Step 11: Implement `roles/ssh_git` (module `ssh`): openssh (root), user keygen
      (prompt email/passphrase), agent, git config (prompt name/email), print pubkey +
      GitHub instructions.
- [ ] Step 12: Create `ansible/playbooks/20-hardening.yml` wiring the 9 roles, each
      tagged + `when: enable_<id>`.
- [ ] Step 13: Extend `generators/manifest_to_playbook.py` (PHASE_IDS phase-2, ROLE_MAP
      for the 9 ids); update `Makefile` (`run-phase2`, check now Phase 0–2).
- [ ] Step 14: Update `ansible/README.md` (Play 2 flow) + Phase 2 README pointer +
      `ssh.md` "get your key" note.
- [ ] Step 15: Run `make lint syntax check` (Phase 0–2 parity green) and a
      `--syntax-check` on `20-hardening.yml`; document the manual bring-up.

## 5. Verification Commands

- Lint: `make lint` (yamllint + ansible-lint over playbooks/ + roles/)
- Syntax: `ansible-playbook --syntax-check playbooks/20-hardening.yml`
- Parity: `python3 generators/manifest_to_playbook.py --check --manifest
  ../os/archlinux/manifest.yaml` (now covers Phase 0–2: every Phase 2 module id has a
  role; every Phase 2 package is referenced)
- Selectability smoke: `ansible-playbook playbooks/20-hardening.yml --list-tasks
  --tags nvidia` shows only the gpu role; a run with `enable_firewall: false` skips it.
- Manual bring-up (real machine, post Phase 1): log in as `end_user`, `make run-phase2`
  with a chosen module set, then run each applied module's verification command
  (e.g. `nvidia-smi`, `snapper -c root list`, `yay --version`, `wpctl status`,
  `sudo ufw status`, `ssh -T git@github.com`).

## 6. Rollback Strategy

Play 2 is mostly idempotent and additive; rollback is per-module, not a single undo:

- **GPU (nvidia):** `sudo pacman -Rns nvidia-open nvidia-utils lib32-nvidia-utils
  nvidia-settings`; remove the two GRUB params and re-run `grub-mkconfig`; remove the
  nvidia modules from `mkinitcpio.conf` MODULES, re-add `kms` to HOOKS, `mkinitcpio -P`;
  delete `/etc/pacman.d/hooks/nvidia.hook`. Reboot.
- **Snapshots:** `sudo pacman -Rns snapper snap-pac grub-btrfs btrfs-assistant`;
  `systemctl disable --now snapper-timeline.timer snapper-cleanup.timer`; delete
  `/etc/snapper/configs/root` and `/etc/pacman.d/hooks/50-bootbackup.hook`; remove the
  `grub-btrfs-overlayfs` hook from mkinitcpio, `mkinitcpio -P`.
- **AUR:** `yay -Rns yay` (or `sudo pacman -Rns yay`) — user context.
- **Sound:** `sudo pacman -Rns pipewire wireplumber pipewire-alsa pipewire-pulse
  pipewire-jack helvum playerctl mpv-mpris`; `systemctl --user disable --now
  pipewire.socket pipewire-pulse.socket wireplumber.service`.
- **Networking:** `sudo pacman -Rns bluez bluez-utils bluetui`; `yay -Rns wlctl-bin`;
  `systemctl disable --now bluetooth`.
- **Clock:** `sudo timedatectl set-ntp false` (Windows registry is unchanged by Play 2).
- **Firewall:** `sudo ufw disable; sudo pacman -Rns ufw`.
- **External drives:** remove the fstab line + rmdir the mountpoint; `sudo pacman -Rns
  ntfs-3g udisks2 udiskie`.
- **SSH/Git:** `sudo pacman -Rns openssh`; remove generated keys under `~/.ssh` and the
  global git config (`git config --global --unset …`).

If the parity checker or lint fails 3× on the same change, revert that file to its
pre-change state (git) and re-derive from the manifest — the manifest is the source of
truth, so a green `make check` is the recovery target.

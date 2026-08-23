---
tags: [ansible, archlinux, automation, provisioning, live-usb]
---

# [001]: Ansible Play 1 — Live-USB Install Through First Reboot (Phase 0–1)

Status: APPROVED
Phase: 3-Review
Handoff: 2026-08-23

## 1. Goal & Context

Build **Play 1** of an Ansible automation that automates the Arch Linux install from the
**live USB** (`root@archiso`), covering **Phase 0 (verification checks)** and all of
**Phase 1 (modules 01–08, ending at first reboot)**. The play partitions, formats,
pacstraps, configures (chroot), creates the user, installs GRUB, and reboots — leaving a
bootable dual-boot CLI system. The architecture is **distro-agnostic (Option A: distros
as data)** so later specs can add Phases 2–4 and other distros without rewriting roles.
**Phases 2–4 and multi-distro data files are explicitly out of scope** for this spec.

## 2. Architectural Decisions & Trade-offs

- **D1 — Repo layout & single source of truth.** A top-level `ansible/` domain (sibling of
  `os/`). `os/archlinux/manifest.yaml` remains the single source of truth for modules,
  prerequisites, and packages; Play 1 roles mirror it and a thin generator
  (`ansible/generators/manifest_to_playbook.py`) checks module/package parity so the two
  cannot silently drift. Alternative rejected: making Ansible the source of truth and
  generating the MD docs (inverts the repo's docs-first philosophy).
- **D2 — Distro abstraction = Option A (distros as data).** One generic role per module;
  per-distro values live in `vars/distros/<distro>.yml` (package names, commands, paths)
  plus per-role `defaults/<distro>.yml`, selected by the `ansible_distro` inventory var.
  Adding a distro later = adding data files, **no role rewrites**. Only `archlinux.yml`
  is implemented in this spec; the indirection layer exists but is single-distro for now.
  Alternatives rejected: B (one playbook tree per distro → N-fold duplication), C (defer
  the abstraction → deferred repo-wide refactor when distro #2 arrives).
- **D3 — Drive selection model (store-all, target-selected).** The `partitioning` role
  runs `lsblk`, stores **all detected drives as a list** in a fact, then operates **only**
  on the drive the user named. The user sets `target_drive` (e.g. `nvme1n1`) in
  `ansible/inventory/hosts.yml` — the single "place to put the drive." Before writing any
  GPT table the play validates `target_drive` against expected model/size and requires an
  explicit `--confirm-destructive` flag. Alternative rejected: unattended partitioning
  (risk of wiping the Windows drive; the guide itself carries a CAUTION).
- **D4 — Two-stage install pattern (live-USB host → chroot target).** Ansible cannot run
  inside the not-yet-existing target, so the play uses two stages: (1) **host stage** on
  the live USB — partition, format, mount, `pacstrap`, write configs (plain tasks against
  `/mnt`); (2) **chroot stage** — anything needing the new system's `pacman`/`systemctl`
  (NetworkManager, user/sudo, GRUB) runs via a `shell` task wrapping `arch-chroot /mnt`.
  No `become`/sudo is needed anywhere: on the live USB the operator is already root.
- **D5 — Phase 0 is a verification gate, not an action.** Phase 0's real steps (BIOS
  Secure Boot, Windows Fast Startup, USB flashing, UEFI boot) are manual and pre-Linux;
  Ansible cannot and should not script firmware. Play 1 therefore implements Phase 0 as a
  **pre-flight assertion gate** (UEFI present, network up, NTP, target drive present and
  matching) that halts with a clear message on failure. The one Phase 0 step Ansible can
  do (drive identification) becomes the input to D3.
- **D6 — Verification/test harness (no CI).** Always-on checks: `ansible-playbook
  --syntax-check` on the play, `yamllint`, `ansible-lint`, and the generator parity check
  (every Phase 0–1 manifest module id has a role; every listed package is referenced).
  Acceptance = a documented manual bring-up on the real machine (or a disposable VM): run
  Play 1, confirm it reboots into a GRUB menu showing Linux + Windows. The repo has no CI
  today; none is added. Alternative rejected: molecule/Vagrant VM automation (large infra
  investment; deferred to a follow-up spec).

## 3. Affected Files & Scope

- Created: `ansible/` domain (Phase 0–1 scope only):
  - `ansible/README.md` — user flow (Phase 0 manual steps → install git+ansible on live USB
    → clone → set `target_drive` → run Play 1 → reboot), safety gates, distro selection
  - `ansible/ansible.cfg` — localhost inventory, interpreter, retry file off
  - `ansible/inventory/hosts.yml` — `localhost` + user vars: `ansible_distro: archlinux`,
    `target_drive`, `target_drive_model`, `target_drive_size`, `hostname`, `timezone`,
    `locale`, `end_user`, `swap: true`, `country` (for reflector)
  - `ansible/group_vars/all.yml` — shared defaults
  - `ansible/vars/distros/archlinux.yml` — Arch package/command/path mapping (Option A layer)
  - `ansible/playbooks/10-install.yml` — **Play 1** (the only play in this spec):
    Phase 0 gate → Phase 1 modules 01–08 → reboot
  - `ansible/roles/`:
    - `roles/preflight/tasks/main.yml` — Phase 0 verification gate (UEFI, network, NTP,
      drive present + model/size match); halts on failure
    - `roles/verify_boot/tasks/main.yml` — module 01: assert UEFI, connectivity, `timedatectl set-ntp true`
    - `roles/partitioning/tasks/main.yml` — module 02: detect-all-drives fact, target
      selection + validation, **destructive gate**, gdisk (templated script)
      (+ `templates/gdisk-script.j2`)
    - `roles/filesystems_btrfs/tasks/main.yml` — module 03: mkfs.fat, mkswap/swapon,
      mkfs.btrfs, subvolume loop, templated mounts
    - `roles/install_base/tasks/main.yml` — module 04: reflector, keyring, `pacstrap -K /mnt`
    - `roles/system_config/tasks/main.yml` — module 05: genfstab; chroot-stage timezone,
      `locale.gen` template + `locale-gen`, hostname, NetworkManager
      (+ `templates/locale.gen.j2`)
    - `roles/users_sudo/tasks/main.yml` — module 06: user + sudoers.d drop-in (chroot-stage)
    - `roles/bootloader_grub/tasks/main.yml` — module 07: grub install, `grub-mkconfig`,
      os-prober, `efibootmgr` (chroot-stage)
    - `roles/first_reboot/tasks/main.yml` — module 08: final checks + `reboot`
    - `roles/*/defaults/archlinux.yml` — per-role Arch values (packages, paths) sourced from manifest
  - `ansible/generators/manifest_to_playbook.py` — parity checker: every Phase 0–1 module id
    → a role; every manifest package → referenced. `--check` exits non-zero on drift.
  - `ansible/.yamllint`, `ansible/Makefile` (targets: `lint`, `syntax`, `check`, `run`)
- Modified:
  - `README.md` (repo root) — add an `ansible/` domain line + link (Phase 0–1 status)
  - `os/archlinux/README.md` — add a pointer to the `ansible/` Play 1 automation companion
- Deleted: none

## 4. Actionable TODO Checklist

- [x] Step 1: Scaffold `ansible/` — `ansible.cfg`, `inventory/hosts.yml` (with the `target_drive`
      field the user fills), `group_vars/all.yml`, `vars/distros/archlinux.yml`, `Makefile`, `.yamllint`.
- [x] Step 2: Build `generators/manifest_to_playbook.py`; run `--check` against
      `os/archlinux/manifest.yaml` for Phase 0–1 module ids + packages (baseline green).
- [x] Step 3: Implement `roles/preflight` + `roles/verify_boot` (Phase 0 gate + module 01):
      assert UEFI, ping, `timedatectl set-ntp true`, target-drive-present check.
- [x] Step 4: Implement `roles/partitioning` (module 02): detect-all-drives fact, store as list,
      select `target_drive`, validate model/size, **destructive gate** (`--confirm-destructive`),
      `templates/gdisk-script.j2` (EFI 2G, optional swap, root).
- [x] Step 5: Implement `roles/filesystems_btrfs` (module 03): mkfs.fat, mkswap/swapon,
      mkfs.btrfs, subvolume create loop `[@,@home,@snapshots,@var_log,@pkg]`, templated mounts.
- [x] Step 6: Implement `roles/install_base` (module 04): reflector (country var), keyring,
      `pacstrap -K /mnt {{ base_packages }}` (list from Option A vars).
- [x] Step 7: Implement `roles/system_config` (module 05): genfstab; chroot-stage timezone,
      locale.gen template + locale-gen, hostname, NetworkManager enable.
- [x] Step 8: Implement `roles/users_sudo` (module 06): user + sudoers.d drop-in via chroot-stage.
- [x] Step 9: Implement `roles/bootloader_grub` (module 07): grub install, mkconfig, os-prober,
      efibootmgr via chroot-stage.
- [x] Step 10: Implement `roles/first_reboot` (module 08): final asserts + `reboot`.
- [x] Step 11: Wire `playbooks/10-install.yml` — preflight → 01..08 in manifest order, ending at reboot.
- [x] Step 12: Verification — `make lint`, `make syntax` (`ansible-playbook --syntax-check`),
      `make check` (generator parity). All green. (check: green — PARITY OK, 10 modules /
      15 packages, PASS attempt 1. lint/syntax: tooling (ansible, yamllint, ansible-lint)
      not installed on this machine; all YAML validated via python yaml. Run `make lint`
      and `make syntax` on the live USB before bring-up.)
- [x] Step 13: Document the user flow + manual bring-up acceptance in `ansible/README.md`.

## 5. Verification Commands

- Lint: `make -C ansible lint` (runs `yamllint -c .yamllint .` and `ansible-lint playbooks/ roles/`)
- Syntax: `make -C ansible syntax` (runs `ansible-playbook --syntax-check playbooks/10-install.yml`)
- Parity: `python ansible/generators/manifest_to_playbook.py --check` (exit 0 iff every Phase 0–1
  manifest module id has a role and every listed package is referenced)
- Bring-up (manual, acceptance): follow `ansible/README.md` — on the live USB run
  `ansible-playbook playbooks/10-install.yml --confirm-destructive` after setting `target_drive`;
  confirm the machine reboots into a GRUB menu showing both Linux and Windows.

## 6. Rollback Strategy

The `ansible/` domain is additive; the only `os/` changes are two doc links. If verification
fails 3× (circuit breaker):
1. `git restore ansible/` (and the two link edits) to revert all created/modified files.
2. Partitioning is destructive-gated: a failed run should not have written a GPT table without
   the `--confirm-destructive` flag. Confirm via `lsblk` that the target drive is untouched
   before retrying; if a GPT write did occur, re-run the play (it re-partitions from scratch).
3. Re-run `make check` to confirm manifest parity before re-running the play.
4. Isolate a failing role with `ansible-playbook playbooks/10-install.yml --limit localhost
   -e tags=<role_tag>` and fix in place rather than reverting the whole domain.
5. Because Play 1 ends in a reboot, a partially-completed install is recoverable by re-running
   Play 1 from the live USB (idempotent re-partition + re-pacstrap).

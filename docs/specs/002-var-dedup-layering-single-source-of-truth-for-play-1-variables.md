---
tags: [ansible, refactor, vars, single-source-of-truth]
lane: B
---

# [002]: Var Dedup & Layering — Single Source of Truth for Play 1 Variables

Status: APPROVED
Handoff: 2026-08-23
Phase: 3-Review

## 1. Goal

Eliminate duplicated and dead variables in the `ansible/` Play 1 tree (spec 001) and fix
var layering to one rule: **per-machine values → inventory, static shared layout
constants → `group_vars/all.yml`, distro-specific data (packages/commands/paths) →
`vars/distros/<distro>.yml` (Option A layer)**. No behavior change: the play's tasks,
gates, and ordering are untouched; only where values live changes.

## 3. Affected Files & Scope

- Modified:
  - `ansible/group_vars/all.yml` — becomes the single home for static shared vars:
    `ansible_distro`, `mount_point`, `efi_dir` (kernel ABI path, distro-agnostic),
    `confirm_destructive: false`
  - `ansible/inventory/hosts.yml` — per-machine values: `target_drive*`, `hostname`,
    `timezone`, `locale`, `end_user`, `country`, `swap`, `swap_size`, `efi_size`
  - `ansible/vars/distros/archlinux.yml` — absorbs distro-specific data currently
    stranded in dead role defaults: btrfs layout, gdisk hex codes, sudo group/shell
  - `ansible/playbooks/10-install.yml` — none (vars_files unchanged)
  - `ansible/roles/preflight/tasks/main.yml` — use shared `efi_dir`; drop
    `preflight_efi_dir`
  - `ansible/roles/verify_boot/tasks/main.yml` — use shared `efi_dir`
  - `ansible/roles/partitioning/tasks/main.yml` — consume `partitioning_efi_code` etc.
    from distro vars (template uses them)
  - `ansible/roles/partitioning/templates/gdisk-script.j2` — reference hex codes from
    vars instead of hardcoding
  - `ansible/roles/filesystems_btrfs/tasks/main.yml` — consume `btrfs_subvolumes`,
    `btrfs_mount_options`, `btrfs_mkfs_args` (names already match distro vars)
  - `ansible/roles/users_sudo/tasks/main.yml` — consume `sudo_group`, `sudo_shell`
  - `ansible/generators/manifest_to_playbook.py` — widen package-reference scan from
    `roles/`+`vars/` to include `group_vars/` (keeps parity honest after moves)
- Deleted:
  - `ansible/roles/preflight/defaults/archlinux.yml` (dead `preflight_efi_dir`)
  - `ansible/roles/verify_boot/defaults/archlinux.yml` (dead `verify_boot_efivars_dir`)
  - `ansible/roles/partitioning/defaults/archlinux.yml` (moves to distro vars)
  - `ansible/roles/filesystems_btrfs/defaults/archlinux.yml` (dead re-exports)
  - `ansible/roles/users_sudo/defaults/archlinux.yml` (moves to distro vars)
  - `ansible/roles/first_reboot/defaults/archlinux.yml` (dead)
- Created: none (no `defaults/<distro>.yml` files remain; the Option A layer is
  `vars/distros/` + role tasks referencing those keys)
- Docs: `ansible/README.md` Layout section updated to reflect the new var layering.

## 4. Actionable TODO Checklist

- [/] Step 1: Consolidate `group_vars/all.yml` (`efi_dir`, `mount_point`,
      `ansible_distro`, `confirm_destructive`).
- [ ] Step 2: Move `efi_size` to inventory next to `swap`/`swap_size`.
- [x] Step 3: Absorb surviving role-default values into `vars/distros/archlinux.yml`
      (gdisk hex codes, sudo group/shell; btrfs keys already present).
- [x] Step 4: Update role tasks to canonical names (`efi_dir`, `sudo_group`,
      `sudo_shell`, `btrfs_*`, `partitioning_*_code`); gdisk template consumes hex
      codes from vars.
- [x] Step 5: Delete all six dead/redundant `roles/*/defaults/archlinux.yml` files.
- [x] Step 6: Widen generator package scan to `group_vars/`; `make check` green.
- [x] Step 7: Update `ansible/README.md` layout + var-layering note.
- [x] Step 8: Verification — parity check green, all YAML parses, no task references
      a deleted var name.

---
tags: [ansible, refactor, roles, passwords, fstype, bootloader]
lane: B
---

# [003]: Role Consolidation & Selectable Layout — verify_boot merge, fstype-conditional checks, bootloader pattern, password flow

Status: APPROVED
Phase: 2-Build
Handoff: 2026-08-23
Handoff:

## 1. Goal

Four follow-ups from spec 002 review:

1. **Merge `verify_boot` into `preflight`** (Option A): delete the duplicate role;
   preflight becomes the single Phase 0/01 assertion gate (UEFI, internet, NTP,
   target drive). No behavior change: same assertions, one home.
2. **Fstype-conditional checks**: `system_config` and `first_reboot` gate their
   btrfs-only assertions on `fstype == btrfs`; any other value skips them.
   Today only btrfs exists downstream — the gates make the layout selectable
   without breaking non-btrfs runs.
3. **Bootloader-selectable pattern**: a `bootloader` inventory var (default
   `grub`) that the bootloader role consumes, so a future alternative bootloader
   is a data + task-branch change, not a rewrite. No second bootloader is
   implemented in this spec (GRUB is the only one, per spec 001/002 scope).
4. **Password flow**: interactive prompts for both `root_password` and
   `end_user_password` (Q2-B). Inventory values of non-zero length pre-fill the
   prompt (skip the keyboard read); empty or absent prompts. Both passwords are
   set via chroot `chpasswd` with `no_log: true`. Fixes the latent bug where a
   pre-defined `end_user_password` was silently ignored.

No manifest change: modules/packages are untouched; only role structure,
gating, and the password mechanics change.

## 3. Affected Files & Scope

- Modified:
  - `ansible/playbooks/10-install.yml` — drop the `verify_boot` role entry
  - `ansible/roles/preflight/tasks/main.yml` — absorb verify_boot's assertions
    (already all present: UEFI stat on `efi_dir`, ping, NTP enable + active
    assert); add a comment noting it covers manifest modules overview,
    pre-flight, and verify-boot
  - `ansible/roles/preflight/vars/` or playbook comment — none; module-id
    coverage is by string reference in tasks (parity checker reads task text)
  - `ansible/generators/manifest_to_playbook.py` — `ROLE_MAP`:
    `"verify-boot": "preflight"` (was `verify_boot`); the "module id referenced
    in tasks" check then reads `verify-boot` in preflight's task file, so the
    header comment must name it
  - `ansible/inventory/hosts.yml` — add `fstype: btrfs`, `bootloader: grub`,
    commented `root_password: ""` and `end_user_password: ""` (empty = prompt)
  - `ansible/roles/filesystems_btrfs/tasks/main.yml` — read `fstype` (per
    spec 002 layering: per-machine value lives in inventory); tasks are
    btrfs-only for now, so add an up-front assert
    `fstype in ['btrfs']` with a clear "other fstypes not implemented yet"
    fail_msg (defense-in-depth; the real work lands when ext4/xfs arrive)
  - `ansible/roles/system_config/tasks/main.yml` — the "Assert fstab has btrfs
    subvolume entries" task gets `when: fstype == 'btrfs'`
  - `ansible/roles/first_reboot/tasks/main.yml` — final checks stay
    fstype-agnostic (fstab non-empty, grub.cfg non-empty, user exists); add a
    btrfs-specific `findmnt` check gated `when: fstype == 'btrfs'` so the
    "verify based on which filesystem is used" pattern is demonstrable
  - `ansible/roles/users_sudo/tasks/main.yml` — replace the single
    `end_user_password` pause with two prompt tasks:
    - root: `pause` pre-filled from `root_password | default('')` when
      non-empty (skip prompt), else prompt; on non-empty input, chroot
      `chpasswd` for root (`no_log: true`)
    - end user: same pattern with `end_user_password`; chroot `chpasswd` for
      `{{ end_user }}`
    - the pre-defined-but-empty edge (var set to `""`) must prompt, not skip
  - `ansible/README.md` — role list (verify_boot merged into preflight),
    inventory section (fstype, bootloader, password vars), var-layering note
    (fstype/bootloader are per-machine)
- Deleted:
  - `ansible/roles/verify_boot/` (whole role dir; tasks merged into preflight)
- Created: none

## 4. Actionable TODO Checklist

- [x] Step 1: Merge verify_boot into preflight — absorb assertions, update
      preflight header comment to name all three module ids, drop the role
      from the playbook, update `ROLE_MAP` in the parity checker.
- [x] Step 2: Add `fstype: btrfs` and `bootloader: grub` to inventory; add the
      up-front `fstype` assert in filesystems_btrfs; gate the system_config
      subvol assertion on `fstype == 'btrfs'`; add the gated btrfs `findmnt`
      check in first_reboot.
- [x] Step 3: Password flow — two prompt tasks (root + end user) with
      pre-fill semantics (non-empty inventory value skips the prompt; empty or
      absent prompts), chroot chpasswd for both, `no_log: true`.
- [x] Step 4: Widen — nothing to widen in the generator (no new packages);
      `make check` green.
- [x] Step 5: Update `ansible/README.md` (roles, inventory, layering).
- [x] Step 6: Verification — parity check green, all YAML parses, no references
      to the deleted `verify_boot` role or old `users_sudo_password` var,
      password tasks render for both pre-filled and prompt paths.

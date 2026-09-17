---
tags: [ansible, arch-linux, nvidia, fonts, microcode]
---

# 006: CPU microcode, NVIDIA initramfs robustness, and host-overridable fonts

Status: APPROVED
Phase: 2-Build
Handoff: 2026-09-17

## 1. Goal & Context

The greenfield `ansible/` tree currently "installs the package" for the GPU and has no microcode or
fonts role at all, so a minimal run breaks at the first `linux` update (NVIDIA) and ships a box with
no vendor microcode and no system font fallbacks. This spec ports the three robustness concerns the
retired `ansible_bck/` tree handled (CPU microcode by vendor, the full NVIDIA initramfs/GRUB/rebuild-hook
setup, and a system-wide fonts role) into the new tree using its existing variant-selection (ADR-018)
and two-variable (ADR-007) patterns.

## 2. Architectural Decisions & Trade-offs

1. **CPU microcode is an inventory-selected variant (`cpu_vendor`) resolved through the shared
   `x_packages.ucode` map and is OPTIONAL: `amd` installs `amd-ucode`, `intel` installs `intel-ucode`,
   and an absent/`~` value installs nothing (no default, no assert). It is installed at the chroot
   pacstrap and again in the converge path, both of which no-op when the value is unset.**
   Alternative: hardcode `amd-ucode` in base packages, or make `cpu_vendor` required. Rejected:
   hardcoding ignores the vendor, and a required assert would break any host that declares no vendor
   when "nothing" is a legitimate choice. (consequence flagged in section 3)

2. **The ENTIRE NVIDIA setup is owned by the single `gpu` role (play 02, booted): package install,
   the GRUB kernel cmdline, the initramfs `MODULES`, the `kms`-hook removal, the `PostTransaction`
   rebuild pacman hook, and `mkinitcpio -P`; all NVIDIA specifics live in a new `gpu_nvidia`
   distro-data block, and there are NO per-vendor role files.** Alternative: split the GRUB cmdline
   into `bootloader` (play 01, chroot), or revive the old tree's `gpu/tasks/{amd,intel,nvidia}.yml`.
   Rejected: a split owner means two roles must stay in sync for one driver, and per-vendor role files
   are explicitly rejected by ADR-009; keeping it all in `gpu` means `bootloader` is left untouched.
   Accepted trade-off: the first boot uses a generic initramfs (no NVIDIA `MODULES`) and the GRUB
   cmdline is applied by the `gpu` role post-boot; the `PostTransaction` rebuild hook carries the
   NVIDIA modules into the initramfs on the next driver/kernel transaction. (consequence flagged in
   section 3)

3. **Fonts become a dedicated `fonts` role in play 02 (after `aur_helper`). Both the package list and
   the fontconfig profile (primary mono/sans + fallback chain) are resolved across THREE levels —
   host, arch-group, and role default — and a parameterized system `local.conf` is rendered then
   `fc-cache -fv` runs; the font packages currently in `theming` move into the fonts role so one role
   owns all font installation.** The main font (`mono`/`sans`) is the first non-empty value walking
   host -> arch-group -> role default. The fallback chain is the host + arch-group + role lists
   concatenated with per-name dedupe (first/highest-priority level wins) and order preserved within
   each level. Alternative: fold fonts into `theming` (spec 002's current wording) with a static
   `local.conf`. Rejected: `theming` is about GTK/Qt theme/cursor/icon, and a static `local.conf`
   cannot change the primary font per host; ADR-011 says the system `local.conf` is owned by the role
   that installs fonts, not by theme config. (consequence flagged in section 3)

## 3. Risks & Open Questions

> [!IMPORTANT]
> **User Review Required**
> - Decision 2: the NVIDIA `PostTransaction` pacman hook rebuilds the initramfs on every future
>   `linux`/driver transaction; a malformed hook could make a kernel update hard to boot. This is the
>   standard Arch NVIDIA pattern, but it is the load-bearing part. Accepted.
> - Decision 2: the `gpu` role applies the GRUB cmdline and initramfs post-boot, so the very first
>   boot carries a generic initramfs (no NVIDIA `MODULES`); the `PostTransaction` hook picks it up on
>   the next driver/kernel transaction. Accepted — the rebuild on next boot is fine.
> - Decision 3: moving `font-hack-ttf`/`font-dejavu` out of `theming` changes `theming`'s package
>   contract (it will no longer install any font packages). Acceptable?

### Open Questions

- [ ] Q1: RESOLVED — `cpu_vendor` is optional; absent/`~` installs nothing (no default, no assert).
- [ ] Q2: RESOLVED — the fonts `local.conf` is parameterized and resolved across three levels
  (host -> arch-group -> role default); the main font takes the first non-empty value and the
  fallback chain concatenates the three levels with per-name dedupe (order preserved per level).
- [ ] Q3: RESOLVED — microcode installs in BOTH the chroot pacstrap and the converge path, both
  no-op when `cpu_vendor` is unset.

## 4. Affected Files & Contracts

- Deleted: none

### [MODIFY] ansible/inventory/group_vars/arch.yml

Distro data. Adds three blocks: `x_packages.ucode` (vendor -> manager -> pkgs), `x_packages.fonts`
(pacman + aur list), and a `gpu_nvidia` block (GRUB cmdline, initramfs modules, hook target per driver
variant). The `fonts` block carries BOTH the package list and the arch-group fontconfig profile
(mono/sans/fallback), so the arch group is the middle level of the three-level font resolution.

- Contract:
  - `x_packages.ucode.amd.pacman` == `[amd-ucode]`; `x_packages.ucode.intel.pacman` == `[intel-ucode]`
  - `x_packages.fonts.pacman` includes `fontconfig`; `x_packages.fonts.aur` == `[maplemono-ttf]`
  - `x_packages.fonts.profile` carries arch-group `mono`/`sans` (may be empty) and a `fallback` list
  - `gpu_nvidia.grub_cmdline` == `"nvidia_drm.modeset=1 nvidia_drm.fbdev=1"`
  - `gpu_nvidia.mkinitcpio_modules` == `[nvidia, nvidia_modeset, nvidia_uvm, nvidia_drm]`
  - `gpu_nvidia.hook_target.{nvidia_open,nvidia}` name the base driver package per variant

### [MODIFY] ansible/inventory/hosts.yml

Per-machine vars for `thispc`. Adds `cpu_vendor: amd` and the host-level font overrides
(`fonts_packages_overrides` + `fonts_overrides`), both empty by default so the arch-group and role
defaults apply.

- Contract:
  - `cpu_vendor` is either a key present in `x_packages.ucode` or absent/`~` (installs nothing)
  - `fonts_packages_overrides` is an empty mapping by default (host adds/replaces font packages)
  - `fonts_overrides` is an empty mapping by default (host sets main font / prepends fallback)

### [MODIFY] ansible/roles/base_install/tasks/main.yml

Chroot pacstrap (play 01). Conditionally appends the selected ucode package(s) to the pacstrap package
list when `cpu_vendor` is set; installs nothing when it is absent/`~` (no assert).

- Contract:
  - pacstrap command includes the ucode package(s) only when `cpu_vendor` is set and valid; no
    `assert` task — an unset `cpu_vendor` is a valid "install nothing" choice

### [MODIFY] ansible/roles/base_packages/tasks/main.yml

Converge-path (play 02). Installs the selected ucode package(s) idempotently via `install_packages`
only when `cpu_vendor` is set; a no-op task when it is absent/`~`.

- Contract:
  - includes `install_packages` with `install_packages_source: "{{ x_packages.ucode[cpu_vendor] }}"`,
    skipped when `cpu_vendor` is absent/`~`

### [MODIFY] ansible/roles/gpu/tasks/main.yml

Booted-system (play 02) — the SINGLE owner of the whole NVIDIA setup. Keeps package install +
`nvidia-persistenced`; adds, gated on `gpu_variant` matching `nvidia.*`: write the GRUB kernel
cmdline, write the rebuild pacman hook, add the NVIDIA `MODULES` to `/etc/mkinitcpio.conf`, remove the
`kms` hook, and run `mkinitcpio -P` only when an edit changed. The `bootloader` role is NOT modified.

- Contract:
  - nvidia-specific tasks are gated on `gpu_variant | default('') | string is match('nvidia.*')`
  - sets `GRUB_CMDLINE_LINUX_DEFAULT` to include `gpu_nvidia.grub_cmdline` (grep-guarded, idempotent)
  - writes `/etc/pacman.d/hooks/nvidia.hook` (from `nvidia.hook.j2`, mode 0644)
  - `MODULES` line set to `gpu_nvidia.mkinitcpio_modules`; `kms` removed from `HOOKS`
  - `mkinitcpio -P` runs only when the MODULES/HOOKS edit reported `changed` (idempotent)

### [NEW] ansible/roles/gpu/templates/nvidia.hook.j2

PostTransaction pacman hook that rebuilds the initramfs on linux/driver transactions (guarded to skip
driver-only transactions).

- Contract:
  - `[Trigger]` matches the base driver package (`{{ gpu_nvidia.hook_target[gpu_variant] }}`) and `linux`
  - `[Action]` `When=PostTransaction` with an `Exec` that skips when only the driver changed

### [NEW] ansible/roles/fonts/defaults/main.yml

Fonts role defaults. Holds the role-level (lowest-priority) fontconfig profile and the three-level
resolvers. Three levels, highest priority first: **host** (`fonts_overrides` /
`fonts_packages_overrides` in `hosts.yml`), **arch-group** (`x_packages.fonts.profile` /
`x_packages.fonts` in `arch.yml`), **role default** (`fonts_profile` below).

- Contract:
  - `fonts_profile` (role default) carries `mono`, `sans`, and a `fallback` list (Maple Mono NF set)
  - `fonts_config.mono` / `.sans` == first non-empty of
    `fonts_overrides.<key>` -> `x_packages.fonts.profile.<key>` -> `fonts_profile.<key>`
  - `fonts_config.fallback` == host + arch-group + role `fallback` lists concatenated, deduped by
    font name (first/highest-priority occurrence wins), order preserved within each level
  - `fonts_packages` == host + arch-group + role package lists merged per manager (host overrides a
    manager list; managers the host omits fall back to arch-group, then role)

### [NEW] ansible/roles/fonts/templates/local.conf.j2

System-wide fontconfig fallback, parameterized by the resolved `fonts_config` (primary mono/sans
aliases + the merged fallback chain + hinting/rgba). Display-server agnostic.

- Contract:
  - maps generic `monospace` -> `{{ fonts_config.mono }}` and `sans-serif` -> `{{ fonts_config.sans }}`
  - appends the `{{ fonts_config.fallback }}` list (already merged + deduped) as the fallback chain

### [NEW] ansible/roles/fonts/tasks/main.yml

Fonts role tasks (play 02). Installs the combined font packages, renders `/etc/fonts/local.conf`,
rebuilds the font cache.

- Contract:
  - includes `install_packages` with `install_packages_source: "{{ fonts_packages }}"`
  - templates `local.conf.j2` to `/etc/fonts/local.conf` (mode 0644, become)
  - runs `fc-cache -fv` (become) with a `changed_when`

### [MODIFY] ansible/roles/theming/defaults/main.yml

Removes `font-hack-ttf` and `font-dejavu` from `theming_theme_packages.pacman` (font packages now
owned by the fonts role).

- Contract:
  - `theming_theme_packages.pacman` no longer lists any `font-*` package

### [MODIFY] ansible/plays/02_system.yml

Wires the new `fonts` role in after `aur_helper` (AUR fonts need the helper) and before the other
system modules.

- Contract:
  - includes role `fonts` positioned after the `Aur helper` task

## 5. Task DAG

All Verify commands run with working directory `ansible/`. Lint oracles assert the touched role/play
files are `ansible-lint` clean (no new findings; the pre-existing `clock_sync` finding is out of
scope). Syntax oracle asserts the site still parses.

### Task 1: CPU microcode variant selection + install

- Target Files: [MODIFY] ansible/inventory/group_vars/arch.yml, [MODIFY] ansible/inventory/hosts.yml, [MODIFY] ansible/roles/base_install/tasks/main.yml, [MODIFY] ansible/roles/base_packages/tasks/main.yml
- Depends On: None
- Subtasks:
  - [x] 1.1 Add the `x_packages.ucode` vendor map to `arch.yml`.
    - Input: old-tree `distro_packages.ucode` (`amd-ucode`/`intel-ucode`).
    - Output: `x_packages.ucode.{amd,intel}.pacman` present in `arch.yml`.
    - Verify: `cd ansible && grep -c amd-ucode inventory/group_vars/arch.yml`
    - Expect: "1"
  - [x] 1.2 Add `cpu_vendor: amd` to `hosts.yml`.
    - Input: this machine's vendor.
    - Output: `cpu_vendor` set for `thispc` (absent on other hosts = install nothing).
    - Verify: `cd ansible && grep -c cpu_vendor inventory/hosts.yml`
    - Expect: "1"
  - [x] 1.3 Make `base_install` append the ucode package to the pacstrap list only when `cpu_vendor` is set (no assert; unset = nothing).
    - Input: 1.1 + 1.2.
    - Output: chroot pacstrap installs the selected microcode; an unset vendor adds no package.
    - Verify: `cd ansible && ansible-lint roles/base_install`
    - Expect: "0 failure(s), 0 warning(s)"
  - [x] 1.4 Make `base_packages` install the ucode package idempotently via `install_packages`, skipped when `cpu_vendor` is unset.
    - Input: 1.1.
    - Output: converge path (play 02) converges microcode on a live system; no-op when unset.
    - Verify: `cd ansible && ansible-lint roles/base_packages`
    - Expect: "0 failure(s), 0 warning(s)"
- Phase Gate: `cd ansible && ansible-playbook -i inventory/hosts.yml --syntax-check site.yml`

### Task 2: NVIDIA full setup (all in the gpu role; bootloader untouched)

- Target Files: [MODIFY] ansible/inventory/group_vars/arch.yml, [MODIFY] ansible/roles/gpu/tasks/main.yml, [NEW] ansible/roles/gpu/templates/nvidia.hook.j2
- Depends On: None
- Subtasks:
  - [x] 2.1 Add the `gpu_nvidia` distro block (grub_cmdline, mkinitcpio_modules, hook_target) to `arch.yml`.
    - Input: old-tree `gpu.nvidia` values.
    - Output: `gpu_nvidia` block present with cmdline + modules + per-variant hook target.
    - Verify: `cd ansible && grep -c nvidia_drm.fbdev inventory/group_vars/arch.yml`
    - Expect: "1"
  - [x] 2.2 Add the `nvidia.hook.j2` rebuild-hook template (PostTransaction, driver+linux trigger, skip driver-only).
    - Input: 2.1 hook_target.
    - Output: a valid pacman hook that rebuilds the initramfs on linux/driver transactions.
    - Verify: `cd ansible && grep -c PostTransaction roles/gpu/templates/nvidia.hook.j2`
    - Expect: "1"
  - [x] 2.3 Extend the `gpu` role to set the GRUB cmdline, write the hook, set the NVIDIA `MODULES`, remove the `kms` hook, and run `mkinitcpio -P` only on change (all gated on a nvidia variant).
    - Input: 2.1 + 2.2.
    - Output: the booted system carries the NVIDIA GRUB cmdline + initramfs modules + a self-maintaining rebuild hook; `bootloader` is unchanged.
    - Verify: `cd ansible && ansible-lint roles/gpu`
    - Expect: "0 failure(s), 0 warning(s)"
- Phase Gate: `cd ansible && ansible-playbook -i inventory/hosts.yml --syntax-check site.yml`

### Task 3: Three-level fonts role (host -> arch-group -> role default)

- Target Files: [NEW] ansible/roles/fonts/defaults/main.yml, [NEW] ansible/roles/fonts/tasks/main.yml, [NEW] ansible/roles/fonts/templates/local.conf.j2, [MODIFY] ansible/inventory/group_vars/arch.yml, [MODIFY] ansible/inventory/hosts.yml, [MODIFY] ansible/roles/theming/defaults/main.yml, [MODIFY] ansible/plays/02_system.yml
- Depends On: None
- Subtasks:
  - [ ] 3.1 Add the `x_packages.fonts` arch-group block (pacman + `maplemono-ttf` aur list AND the arch-group `profile` with mono/sans/fallback) to `arch.yml`.
    - Input: old-tree `distro_packages.fonts` + the Maple Mono profile.
    - Output: arch-group font packages + the middle-level profile present.
    - Verify: `cd ansible && grep -c fontconfig inventory/group_vars/arch.yml`
    - Expect: "1"
  - [ ] 3.2 Add `fonts_packages_overrides: {}` and `fonts_overrides: {}` to `hosts.yml`.
    - Input: none (empty = arch-group + role defaults apply).
    - Output: host can set the main font and prepend/override the fallback + package lists.
    - Verify: `cd ansible && grep -c fonts_overrides inventory/hosts.yml`
    - Expect: "1"
  - [ ] 3.3 Create `fonts/defaults/main.yml` with the role-default `fonts_profile` plus the three-level resolvers (main font = first non-empty host->group->role; fallback = host+group+role concatenated, deduped by name, order preserved per level; packages merged per manager host->group->role).
    - Input: 3.1 + 3.2.
    - Output: role defaults expose the resolved `fonts_config` + `fonts_packages`.
    - Verify: `cd ansible && ansible-lint roles/fonts/defaults/main.yml`
    - Expect: "0 failure(s), 0 warning(s)"
  - [ ] 3.4 Create the parameterized `fonts/templates/local.conf.j2` (mono/sans aliases + merged fallback chain + hinting/rgba).
    - Input: `fonts_config`.
    - Output: a system fontconfig driven by the resolved profile vars.
    - Verify: `cd ansible && grep -c monospace roles/fonts/templates/local.conf.j2`
    - Expect: "1"
  - [ ] 3.5 Create `fonts/tasks/main.yml` (install resolved packages, render local.conf, fc-cache).
    - Input: 3.1 + 3.3 + 3.4.
    - Output: fonts installed, `/etc/fonts/local.conf` written, cache rebuilt.
    - Verify: `cd ansible && ansible-lint roles/fonts`
    - Expect: "0 failure(s), 0 warning(s)"
  - [ ] 3.6 Remove the font packages from `theming` and wire the `fonts` role into play 02 after `aur_helper`.
    - Input: 3.5.
    - Output: one role owns all font packages; play 02 runs fonts after the AUR helper.
    - Verify: `cd ansible && grep -c "name: fonts" plays/02_system.yml`
    - Expect: "1"
- Phase Gate: `cd ansible && ansible-playbook -i inventory/hosts.yml --syntax-check site.yml`

## 6. Verification Commands

Working directory for all commands: `ansible/` (its `ansible.cfg` sets `inventory` + `roles_path`).

- Build Command: n/a (provisioning tree - no build step)
- Test Command: `cd ansible && ansible-playbook -i inventory/hosts.yml --syntax-check site.yml`
- Lint Command: `cd ansible && ansible-lint roles/fonts roles/gpu roles/base_install roles/base_packages plays/02_system.yml`

## 7. Rollback Strategy

Revert edits in reverse Task DAG order: Task 3 (remove `fonts` role + play 02 wiring, restore
`theming` font packages, drop the arch-group `x_packages.fonts` block + the host `fonts_packages_overrides`/`fonts_overrides`) -> Task 2 (remove `nvidia.hook.j2` + the gpu nvidia tasks, drop the `gpu_nvidia` block; `bootloader` was never touched) -> Task 1 (drop the `x_packages.ucode` map + `cpu_vendor` + the base_install/base_packages ucode lines). If verification
fails 3 consecutive times on any subtask the circuit breaker fires (`docs/temp/escalation.md`), dirty
edits are reverted, and the subtask reverts to `[ ]`.
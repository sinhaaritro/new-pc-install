---
tags: [ansible, vars, layering, single-source-of-truth, distro-abstraction, variant-module, inventory]
---

# ADR-002: Distro Data — Single Source of Truth, Var Layering, Variant-Module Pattern, Inventory Group Selection

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

The goal is Arch-only now but "all distros" later. Three shapes were considered:
(A) distros as data — one generic role per module with all per-distro values in a
single per-distro data file; (B) one playbook tree copied per distro; (C) defer the
abstraction until a second distro is actually needed. The build of Play 1 (spec 001)
then left duplicated and dead variables across the tree (`preflight` and
`verify_boot` each declared the UEFI efivars path; five role `defaults/archlinux.yml`
files held vars no task consumed), so a layering rule was needed where every value
has exactly one home. Later, a regression re-introduced 4 Phase-1 per-role
`defaults/<distro>.yml` files, and the data shape for a module whose packages and
config depend on a host-selected variant (the `gpu` map, ADR-004; future `wifi`) was
never codified. Finally, the distro file sat in the non-standard `ansible/vars/
distros/` folder, loaded by a copy-pasted `include_vars` block in each of the 4
plays' `pre_tasks`, selected by the `ansible_distro` inventory var — 4× duplication
of the load mechanism, and the distro choice invisible in the inventory.

## Decision

Distro abstraction is **Option A**: one generic role per module, all per-distro
values as data in a single per-distro file the roles read directly. Rejected B (N-fold
file duplication) and C (defers a repo-wide refactor until it is largest).

Variables are layered by volatility: `inventory/hosts.yml` holds per-machine values
that change between machines (`target_drive*`, `hostname`, `timezone`, `locale`,
`end_user`, `country`, `swap`, `swap_size`, `efi_size`); `group_vars/all.yml` holds
static shared layout constants (`mount_point`, `efi_dir`, `confirm_destructive`);
`inventory/group_vars/<distro>.yml` holds distro-specific data (packages, commands,
paths, btrfs layout, gdisk hex codes, sudo group/shell, and the variant-module data
maps below); `roles/<r>/vars/` (auto-loaded) holds role-local policy that is not a
distro fact (e.g. `snapshots_retention`). A path is distro data only if it actually
differs between distros; the UEFI efivars path is a Linux kernel ABI constant and
therefore lives in `group_vars/all.yml`, not the distro layer. Role
`defaults/<distro>.yml` files and per-role `include_vars` of them are abolished —
roles read the already-loaded distro file directly (abolition completed for all
Phase 1 roles in spec 007; Phases 2-4 roles must follow when migrated).

The distro file carries two module shapes: **simple** — `distro_packages.<module>`
(flat package list); **variant** — a top-level `<role>:` section keyed by a host var,
each variant carrying `packages` plus a `config` **keyword**. The keyword resolves to
`roles/<r>/vars/<kw>.yml` (lookup data) and optionally `roles/<r>/templates/<kw>.*.j2`
(rendered-to-disk files). A `<variant>: none` or absent host var makes the role skip
(same gate as `gpu`, ADR-004). A two-selector role nests one level deeper
(`gpu.<vendor>.<driver>`); a single-selector role is flat (`wifi.<variant>`).
Content-type rule: data looked up in a task goes in `roles/<r>/vars/` (`.yml`); a
file rendered with `{{ }}` to a real system file goes in `roles/<r>/templates/`
(`.j2`); never a `.j2` in `vars/`.

Distro selection is **inventory group membership**: the distro data file is named
after the distro group (`group_vars/archlinux.yml`), not a category directory, and is
auto-loaded by Ansible's group-var precedence when the host sits under
`all:` → `archlinux:` → `hosts:` → `localhost:`. "Switch distro" = move the host
under a different group. The `ansible_distro` inventory var and the
`ansible/vars/distros/` folder are retired; the per-play `include_vars` blocks are
gone. The per-distro data content is unchanged by the move — only its home and load
mechanism.

## Consequences

Adding a distro or a variant is data-only, with no role rewrites — directly serving
the "all distros" goal with zero duplication. Every value has one source of truth;
the distro choice is visible in the inventory instead of a separate var; standard
folders, no `include_vars` duplication; the `config` keyword keeps roles from
hardcoding the variant→file mapping, and the vars/ vs templates/ split is a
content-type rule, not a per-module choice. Costs: a discipline of referencing
variables (never hardcoded package names) in roles; the parity checker must scan
`group_vars/` as well as `roles/` and `vars/` so moved package references stay
checked; the README layout section must document the rule so future roles follow it;
the global distro file grows with each variant-bearing module, and a new role means
editing it. The `gpu` map (ADR-004) is the first variant-module instance (two-
selector nested case); no `gpu` data changed when the pattern was codified. Adding a
second distro is "new group under `all:` + a `group_vars/<distro>.yml` file + move
the host" — slightly more inventory-aware than dropping a file. Any consumer that
read `ansible_distro` (none in Phase 1) had to be migrated; the Phase 2/3/4 roles
that still `include_vars` `defaults/{{ ansible_distro }}.yml` are out of scope and
must be migrated off per-role `defaults/` (spec 007 follow-up) before `ansible_
distro`'s removal can affect them.

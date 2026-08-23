---
tags: [ansible, vars, layering, single-source-of-truth]
---

# ADR-007: Var Layering — Inventory for Per-Machine Values, group_vars for Static Shared, vars/distros for Distro Data

Status: Accepted
Date: 2026-08-23
Source: docs/specs/002-var-dedup-layering-single-source-of-truth-for-play-1-variables.md

## Context

Spec 001's build left duplicated and dead variables across the Play 1 tree:
`preflight` and `verify_boot` each declared the UEFI efivars path, and five more
role `defaults/archlinux.yml` files held vars no task consumed. A layering rule was
needed so every value has exactly one home. Options: keep per-role defaults (status
quo, drift), or assign layers by volatility — per-machine values to inventory, static
shared layout constants to `group_vars/all.yml`, distro-specific packages/commands/
paths to the Option A `vars/distros/` layer.

## Decision

Variables are layered by volatility: `inventory/hosts.yml` holds per-machine values
that change between machines (`target_drive*`, `hostname`, `timezone`, `locale`,
`end_user`, `country`, `swap`, `swap_size`, `efi_size`); `group_vars/all.yml` holds
static shared layout constants (`ansible_distro`, `mount_point`, `efi_dir`,
`confirm_destructive`); `vars/distros/<distro>.yml` holds distro-specific data
(packages, commands, paths, btrfs layout, gdisk hex codes, sudo group/shell). A path
is distro data only if it actually differs between distros; the UEFI efivars path is
a Linux kernel ABI constant and therefore lives in `group_vars/all.yml`, not the
distro layer. Role `defaults/<distro>.yml` files are abolished for Play 1.

## Consequences

Every value has one source of truth; adding a distro remains data-only (Option A)
with no role defaults to maintain. Costs: the parity checker must scan
`group_vars/` as well as `roles/` and `vars/` so moved package references stay
checked, and the README layout section must document the rule so future roles follow
it. Follow-up: Phases 2-4 roles (later specs) adopt the same layering from day one.

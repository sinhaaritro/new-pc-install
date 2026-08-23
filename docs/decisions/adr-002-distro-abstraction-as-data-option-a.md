---
tags: [ansible, distro-agnostic, abstraction, vars]
---

# ADR-002: Distro Abstraction as Data (Option A)

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

The goal is Arch-only now but "all distros" later. Three shapes were considered: (A) distros
as data — one generic role per module with per-distro values in `vars/distros/<distro>.yml`
and per-role `defaults/<distro>.yml`, selected by an `ansible_distro` var; (B) one playbook
tree copied per distro; (C) defer the abstraction until a second distro is actually needed.

## Decision

Adopt Option A: one generic role per module, per-distro values in `vars/distros/<distro>.yml`
plus per-role `defaults/<distro>.yml`, switched by the `ansible_distro` inventory var. Only
`archlinux.yml` is implemented in this spec; the indirection layer exists but is single-distro.

## Consequences

Adding a distro later means adding data files, with no role rewrites — directly serving the
"all distros" goal with zero duplication. Costs a small up-front indirection layer and a
discipline of referencing variables (never hardcoded package names) in roles. Rejected B
(N-fold file duplication) and C (defers a repo-wide refactor until it is largest).

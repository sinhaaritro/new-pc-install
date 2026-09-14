---
tags: [ansible, bootstrap, roles, decomposition]
---

# ADR-NNN: bootstrap_arch is an orchestrator over six ordered sub-roles

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

Play 01 turns a live ISO into a bootable system: partitioning, base install, identity, user,
bootloader, initial network. Written as one task file it is a few hundred lines in which only
partitioning and the base-install command are genuinely distro-specific.

## Decision

`bootstrap_arch` includes `disk_partition`, `base_install`, `system_identity`, `user_create`,
`bootloader`, `initial_network` in that order and contains no logic of its own; play 01 dispatches
`bootstrap_{{ distro }}`.

## Consequences

A second distro reuses `system_identity`, `user_create`, `bootloader` and `initial_network`
verbatim and rewrites only two roles. The order of the includes is load-bearing and is not enforced
by anything other than the orchestrator file itself; in particular `user_create` must precede every
later `become_user: "{{ target_user }}"`.

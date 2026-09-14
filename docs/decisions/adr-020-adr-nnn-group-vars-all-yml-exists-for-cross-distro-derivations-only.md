---
tags: [ansible, group-vars, derivations, layering]
---

# ADR-NNN: group_vars/all.yml exists for cross-distro derivations only

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

ADR-006 rejected a shared `group_vars/all.yml` because Ansible overwrites rather than merges the
`packages`-shaped dicts held in distro files. `ui_mode` is not distro vocabulary — it is arithmetic
over layer-1 data — and repeating its expression in every `group_vars/<distro>.yml` is how two
copies drift apart.

## Decision

`ansible/group_vars/all.yml` is reintroduced and restricted to cross-distro derivations: no
`packages`, no `commands`, no machine facts. It currently holds exactly one key, `ui_mode`.

## Consequences

Amends ADR-006, which stands for everything it actually addressed — distro vocabulary is still
self-contained and never shared. The clobbering hazard does not apply because nothing declared in
`all.yml` is redefined downstream. The restriction is a convention enforced by review, not by a
mechanism, so a future edit could still smuggle distro data into the file.

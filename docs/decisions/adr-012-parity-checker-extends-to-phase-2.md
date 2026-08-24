---
tags: [ansible, phase-2, parity, manifest]
---

# ADR-005: Parity Checker Extends to Phase 2

Status: Accepted
Date: 2026-08-23
Source: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md

## Context

`os/archlinux/manifest.yaml` is the single source of truth for modules and packages,
and the Play 1 parity checker (`manifest_to_playbook.py`) enforces that the Ansible
tree cannot drift from it for Phase 0-1. Phase 2 has nine modules in the manifest that
the checker does not yet cover.

## Decision

`manifest_to_playbook.py` adds `phase-2` to `PHASE_IDS` and maps each Phase 2 module id
to its role (`nvidia` to the `gpu` role; the other eight to same-named roles). The
"module id referenced in a role task file" and "every manifest package referenced in
the tree" checks then apply to Phase 2 as they do to Phase 0-1.

## Consequences

The manifest remains authoritative for Phase 2; drift between docs and automation is
caught by `make check`. The cost is keeping `ROLE_MAP` and the in-task module-id
string references current when roles or the manifest change.

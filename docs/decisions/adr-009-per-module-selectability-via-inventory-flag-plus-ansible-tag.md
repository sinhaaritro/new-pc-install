---
tags: [ansible, phase-2, tags, inventory]
---

# ADR-002: Per-Module Selectability via Inventory Flag plus Ansible Tag

Status: Accepted
Date: 2026-08-23
Source: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md

## Context

Phase 2 modules have no hard ordering (except NVIDIA should precede Phase 3) and the
user wants to pick and choose which to apply. Selectability could be expressed as
inventory flags only, Ansible tags only, or a fixed recommended set.

## Decision

Every module role is gated by an `enable_<id>` inventory boolean and carries its own
Ansible tag. Flags default to the README recommendation (the five "Recommended"
modules on, the four "Optional" off), so a bare run applies the sensible set. A module
can be skipped either by setting `enable_<id>: false` or by running with `--tags`.

## Consequences

Per-machine intent is persistent (inventory) and per-run intent is ad hoc (tags); a
bare run is safe and sensible. The cost is maintaining one flag per module in
inventory and keeping flag/tag names aligned with module ids. It rejects tags-only (no
persistent intent) and a hard-coded set (no flexibility).

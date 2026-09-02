---
tags: [ansible, phase-2, tags, inventory, selectability, profiles]
---

# ADR-004: Per-Module Selectability — Inventory Flag plus Ansible Tag; Profile Vars Fold into Flags

Status: Accepted
Date: 2026-08-23
Source: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md

## Context

Phase 2 modules have no hard ordering (except NVIDIA should precede Phase 3) and the
user wants to pick and choose which to apply. Selectability could be expressed as
inventory flags only, Ansible tags only, or a fixed recommended set. Later, Phase 4
became the first profile-structured phase: 18 modules grouped into 4 profiles
(dev/ai/creative/gaming) plus a shared dotfiles-backup module. The established
one-flag-plus-one-tag-per-module mechanics does not express "give me the whole dev
profile" without 5 flags. The options were: profile flags only (coarse; breaks
per-module `--tags`), per-module flags only (no profile ergonomics), or per-module
flags plus profile convenience vars.

## Decision

Every module role is gated by an `enable_<id>` inventory boolean **and** carries its
own Ansible tag. Flags default to the README recommendation (the "Recommended"
modules on, the "Optional" off), so a bare run applies the sensible set. A module
can be skipped either by setting `enable_<id>: false` or by running with `--tags`.

For profile-structured phases, inventory additionally carries one `profile_<name>`
boolean per profile; the play's pre_tasks OR the profile var into each of its
module flags, so role `when:` clauses stay identical in shape to the flat phases.
Profile on selects the whole profile; narrowing is done via `--tags` at run time.

## Consequences

Per-machine intent is persistent (inventory) and per-run intent is ad hoc (tags); a
bare run is safe and sensible; both "whole profile" and "single module via tag"
workflows work from one playbook with no new role mechanics. Costs: maintaining one
flag per module in inventory and keeping flag/tag names aligned with module ids; an
explicit per-module flag cannot override a profile var to *off* (OR-semantics — a
module off while its profile is on is inexpressible; set `profile_*: false` and flip
individual flags), which is documented in the README. Rejected: tags-only (no
persistent intent), a hard-coded set (no flexibility), and profile-flags-only (breaks
per-module `--tags`). Follow-up: if more than one profile-structured phase appears,
extract the fold into a shared pre_task role.

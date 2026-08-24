---
tags: [ansible, phase-4, profiles, selectability, inventory]
---

# ADR-015: Play 4 profile vars fold into per-module enable flags in pre_tasks

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

Phase 4 is the first profile-structured phase: 18 modules grouped into 4
profiles (dev/ai/creative/gaming) plus a shared dotfiles-backup module. The
established selectability mechanics (spec 004 D2, spec 005 D2) is one
`enable_<id>` inventory flag + one Ansible tag per module, which does not
express "give me the whole dev profile" without 5 flags. The options were:
profile flags only (coarse; breaks per-module `--tags`), per-module flags
only (no profile ergonomics), or per-module flags plus profile convenience
vars.

## Decision

Inventory carries 18 `enable_<id>` flags plus 4 `profile_<name>` booleans;
Play 4 pre_tasks OR the profile var into each of its module flags so role
`when:` clauses stay identical in shape to Play 3's. Profile on selects the
whole profile; narrowing is done via `--tags` at run time.

## Consequences

Enables both "whole profile" and "single module via tag" workflows from one
playbook with no new role mechanics. Costs: an explicit per-module flag
cannot override a profile var to *off* (OR-semantics — a module off while
its profile is on is inexpressible; must set `profile_*: false` and flip
individual flags), which is documented in the README. Follow-up: if more
than one profile-structured phase appears, extract the fold into a shared
pre_task role.

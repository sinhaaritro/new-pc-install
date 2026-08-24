---
tags: [ansible, phase-4, parity, manifest, generator]
---

# ADR-020: Parity checker gains profile-aware Phase 4 support with flat module ids

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

The manifest encodes phase-4 with a `profiles:` structure (4 profiles,
18 modules) instead of the flat `modules:` list used by phases 0-3, so the
parity checker's `load_modules` would see zero phase-4 modules. Options:
namespace the ids as `<profile>-<module>` (breaks the flat `enable_<id>`
flag/tag convention established in specs 004/005), or teach the checker to
walk the nested structure while keeping ids flat. One id collision exists:
phase-4 `davinci` against the phase-3 naming space.

## Decision

`PHASE_IDS` gains `phase-4`; `load_modules` iterates `profiles[].modules[]`
when a phase entry has `profiles:`; module ids stay flat (they are unique
across profiles in the manifest); the single colliding role is named
`creative_davinci_resolve` with a ROLE_MAP entry `davinci` →
`creative_davinci_resolve` (mirroring how `gpu` already covers the phase-2
`nvidia` id). ROLE_MAP gains 19 entries (18 modules + shared
dotfiles-backup).

## Consequences

The manifest stays the single source of truth across all five phases
without an id-namespacing migration, and flags/tags keep their flat
`enable_<id>` shape. Costs: the checker now has two manifest shapes to
handle (branch on presence of `profiles:`), and role names can diverge from
bare module ids only through explicit ROLE_MAP entries — any future
colliding id must be given a namespaced role name and a map entry, not a
reused directory.

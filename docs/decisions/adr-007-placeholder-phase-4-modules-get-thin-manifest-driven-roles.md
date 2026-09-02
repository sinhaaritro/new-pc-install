---
tags: [ansible, phase-4, placeholders, manifest, parity]
---

# ADR-007: Placeholder Phase 4 modules get thin manifest-driven roles

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

12 of 18 Phase 4 module docs are TODO placeholders (all gaming, all
creative, plus neovim, languages, api-testing, training). Some carry
packages in the manifest (steam, mangohud, obs-studio, mpv, neovim).
Options: skip placeholders entirely (parity checker needs a whitelist;
`make run-phase4` gives no working gaming/creative baseline), or guess full
package sets from README index hints (drift risk — the manifest is the
contract), or a thin middle ground.

## Decision

Every placeholder module gets a role that installs exactly the packages
listed in its manifest entry (none if the list is empty), runs no AUR/npm/
binary steps, and prints a "doc is a placeholder — remaining manual steps
pending" note naming the doc file.

## Consequences

The parity checker stays green without a whitelist (every manifest module
id has a role; every manifest package is referenced), and a fresh install
gets a usable baseline for all four profiles today. Costs: the thin roles
are scaffolding — filling in a placeholder doc later requires extending
that role (new packages/AUR steps/services) in a follow-up task, and the
printed note must be updated when the doc lands. No package guessing means
no silent drift from the manifest.

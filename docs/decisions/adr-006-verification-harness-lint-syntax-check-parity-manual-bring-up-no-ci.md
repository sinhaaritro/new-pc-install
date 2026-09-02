---
tags: [ansible, verification, lint, syntax-check, parity, manifest, no-ci]
---

# ADR-006: Verification Harness — Lint, Syntax-Check, Parity, Manual Bring-Up; No CI

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

The repo is docs-only with no build, test, or CI. Introducing Ansible needs a way to
catch errors without a live machine for every change, but a full VM/CI pipeline is a
large infrastructure investment that does not fit. We had to choose a verification
bar that is always-on and cheap, with a separate real-hardware acceptance step. As
each later play landed (Play 2, Play 4), the question was whether to add new
verification infra or extend the existing harness; Play 4 additionally introduced a
nested `profiles:` manifest structure the parity checker had to understand.

## Decision

Always-on checks are: `ansible-playbook --syntax-check` on each play, `yamllint`,
`ansible-lint`, and the generator parity check (`ansible/generators/
manifest_to_playbook.py`). Acceptance is a documented manual bring-up on the real
machine or a disposable VM, running each applied module's verification command. **No
CI** is added.

The harness is **reused, never forked**: Play 2 runs `make lint`, `make syntax`
(extended to `20-hardening.yml`), `make check` (parity extended to Phase 0-2); Play
4 runs the same targets (`make syntax` gains `40-workflow.yml`; `make check` is
profile-aware Phase 0-4) plus `--list-tasks` selectability/prerequisite/model-gate
smokes. The parity checker keeps the manifest as single source of truth across all
five phases: `PHASE_IDS` gains `phase-2` and `phase-4`; each Phase 2 module id maps
to its role (`nvidia` → `gpu`; the other eight to same-named roles); `load_modules`
iterates `profiles[].modules[]` when a phase entry has `profiles:`, keeping module
ids **flat** (they are unique across profiles in the manifest) so the `enable_<id>`
flag/tag convention (ADR-010) is unchanged. The one id collision — phase-4 `davinci`
against the phase-3 naming space — gets the namespaced role `creative_davinci_
resolve` with a ROLE_MAP entry `davinci` → `creative_davinci_resolve` (mirroring how
`gpu` covers the phase-2 `nvidia` id); ROLE_MAP gains 19 Phase 4 entries (18 modules
+ shared dotfiles-backup). Any future colliding id must get a namespaced role name
and a map entry, not a reused directory.

## Consequences

Fast local feedback on every change and a clear definition of done without new CI
infrastructure; verification stays consistent across plays and cheap to run; a green
`make check` remains the single drift signal against the manifest across all five
phases. Costs: manual acceptance on real hardware (syntax/lint passing is necessary
but not sufficient for a working install; no automated end-to-end proof); keeping
`ROLE_MAP` and in-task module-id string references current when roles or the
manifest change; the checker now handles two manifest shapes (branch on presence of
`profiles:`). Rejected: molecule/Vagrant VM automation and any CI pipeline — the
right long-term answers, but too large an investment for this repo's scope; per-role
test roles for Play 4 (no new artifact classes needed new checks).

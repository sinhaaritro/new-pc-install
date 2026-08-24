---
tags: [ansible, phase-4, verification, lint, parity]
---

# ADR-022: Play 4 reuses the Play 1-3 verification harness with no new infra

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

Plays 1-3 verify via `ansible-playbook --syntax-check`, yamllint,
ansible-lint, the manifest parity check, and a documented manual bring-up
(spec 001 D6, spec 004 D6, spec 005 D7, ADR-006/013). Phase 4 adds no new
artifact classes that would need new checks beyond the profile-aware parity
branch (ADR-020). Options: add CI, add per-role test roles, or keep the
existing harness.

## Decision

Play 4 is verified by the existing harness: `make lint` (yamllint +
ansible-lint over playbooks/ + roles/), `make syntax` (gains
40-workflow.yml), `make check` (parity now covers Phase 0-4 profile-aware),
`--list-tasks` selectability/prerequisite/model-gate smokes, and a
documented manual bring-up running each applied module's doc verification
command.

## Consequences

No new infrastructure to maintain; the green `make check` remains the
single drift signal against the manifest across all five phases. Costs:
manual bring-up coverage of the AUR/npm/download paths depends on the
operator running the real machine pass — accepted, consistent with
ADR-006 (no CI). Follow-up: if the thin placeholder roles get real
content, their verification commands join the bring-up checklist in the
same README section.

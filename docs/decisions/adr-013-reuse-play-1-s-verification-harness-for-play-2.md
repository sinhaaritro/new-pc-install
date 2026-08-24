---
tags: [ansible, phase-2, verification, lint]
---

# ADR-006: Reuse Play 1's Verification Harness for Play 2

Status: Accepted
Date: 2026-08-23
Source: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md

## Context

Play 1 established always-on checks (ansible-playbook --syntax-check, yamllint,
ansible-lint, and the parity check) plus a documented manual bring-up as acceptance,
with no CI (the repo has none). Play 2 needs verification without introducing new
infrastructure.

## Decision

Play 2 reuses the same harness: `make lint`, `make syntax` (extended to
`20-hardening.yml`), and `make check` (parity now Phase 0-2). Acceptance is a
documented manual bring-up on the real machine: run Play 2 with a chosen module set and
run each applied module's verification command. No CI is added.

## Consequences

Verification stays consistent across plays and cheap to run locally. The cost is that
acceptance remains a manual real-machine step (no automated functional test), matching
the repo's current no-CI posture (spec 001 D6).

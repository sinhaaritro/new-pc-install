---
tags: [ansible, fqcn, pacman]
---

# ADR-<NNN>: Exclude Fqcn Canonical For Pacman Instead Of Adding The Collection

Status: Accepted
Date: 2026-09-16
Source: docs/specs/003-ansible-lint-remediation.md

## Context

Two call sites use `ansible.builtin.pacman`, and `ansible-lint` suggests the canonical
`community.general.pacman`. The target is Arch and `ansible.builtin.pacman` already resolves in
the controlled environment, so the finding is a naming suggestion, not a functional bug.

## Decision

Exclude the `fqcn[canonical]` finding for the pacman module in `ansible.cfg` instead of
switching the two call sites to `community.general.pacman`.

## Consequences

No new `community.general` collection dependency is introduced and the working pacman calls
stay untouched. The cost is that the canonical-name suggestion remains unaddressed by design,
so a lint-policy change or an environment without the builtin module would surface the finding
again.

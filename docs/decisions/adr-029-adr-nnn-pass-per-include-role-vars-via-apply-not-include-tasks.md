---
tags: [ansible, include-role, lint]
---

# ADR-<NNN>: Pass Per-Include Role Vars Via Apply, Not Include_Tasks

Status: Accepted
Date: 2026-09-16
Source: docs/specs/003-ansible-lint-remediation.md

## Context

Twenty-one roles call the shared `install_packages` role with a top-level `vars:` block, which
`ansible-lint` flags as an invalid option. The tree dispatches that role by manager filename
(ADR-009) and by role-name prefix (ADR-011), so the include must remain a role include rather
than being rewritten as `include_tasks` with `vars:`.

## Decision

Move every per-include `vars:` block under the include's `apply: { vars: {...} }`, the only
valid way to pass vars to a role include, leaving the include itself a role include.

## Consequences

The include stays a role include, preserving dispatch-by-filename and the role/package-key
one-to-one mapping. `ansible-lint` no longer reports an invalid `include_role` option. The cost
is a mechanical touch to all 21 call sites, and readers must now know that per-include vars
live under `apply:` rather than as a sibling of the module.

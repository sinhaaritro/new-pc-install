---
tags: [ansible, var-naming, lint-policy]
---

# ADR-<NNN>: Exclude Var-Naming No-Role-Prefix Instead Of Renaming

Status: Accepted
Date: 2026-09-16
Source: docs/specs/003-ansible-lint-remediation.md

## Context

`ansible-lint` reports 21 `var-naming/no-role-prefix` findings for vars such as
`package_source`, `desktop_config`, and `target_user`. These names are intentionally shared
and overridden across roles as part of the documented four-variable-layer model (ADR-007) and
the role-name-prefix dispatch (ADR-011); the prefix convention there applies to role names,
not to the shared variables a reader passes between roles.

## Decision

Exclude `var-naming/no-role-prefix` in `ansible.cfg` rather than renaming the variables to
carry a per-role prefix.

## Consequences

The tree keeps its documented cross-role variable conventions and dispatch-by-name contract
intact, and the lint run reaches zero for this rule. The cost is that the rule stays unsatisfied
by design, so a future lint-policy tightening or a new maintainer who does not know the
convention may re-surface these findings and expect renames.

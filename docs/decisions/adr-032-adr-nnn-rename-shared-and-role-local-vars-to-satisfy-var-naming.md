---
tags: [ansible, var-naming, lint-policy, x-prefix]
---

# ADR-<NNN>: Rename Shared And Role-Local Vars To Satisfy Var-Naming

Status: Accepted
Date: 2026-09-16
Source: docs/specs/004-ansible-lint-zero-finding-without-config-waivers.md

## Context

Spec 003 reached a clean `ansible-lint` run only by excluding the `var-naming` rule family in
`ansible/.ansible-lint`, which the user rejected as suppression rather than a fix. The 43
`no-role-prefix` findings split into two classes: 5 keys shared across roles
(`package_source`, `target_user`, `target_uid`, plus the group_vars keys) and 21 role-local
names in 8 `defaults/` files. ADR-004's four-variable-layer model already names the
cross-role shared layer `x_`, and ADR-011 already mandates the role-name prefix convention,
so renaming is a restoration of the documented design, not a new convention. Alternatives
(keep the exclusion, `skip_list`, per-role prefixes that break the shared contract) were
rejected.

## Decision

Rename the shared keys to the `x_` prefix at their definition sites (`group_vars/`) and at
every usage site, and rename the role-local `defaults/` vars to their role-name prefix
(`docker_defaults` -> `app_docker_defaults`, etc.), keeping shared keys identical in name
across all roles.

## Consequences

The `var-naming` rule is satisfied by the code and the rule no longer needs any exclusion;
the dispatch-by-name contract (ADR-009/011) is preserved because includes are addressed by
role name, not variable name. The cost: every usage site changes at once (group_vars, 8
defaults files, ~25 tasks files), and ADR-030's exclusion decision is superseded (recorded
here; ADR-030 is left as Accepted history per the no-edit guardrail).

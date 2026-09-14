---
tags: [ansible, role-defaults, merge-strategy, jinja]
---

# ADR-<NNN>: The Two-Variable Trick (`X_defaults` + `X_overrides` → `X`)

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Ansible replaces dicts across precedence levels; it does not merge them. If role defaults hold
six desktop components and inventory writes one, the other five vanish. The alternative — having
inventory restate the full dict on every override — was rejected: it duplicates the roster into
every machine file and turns a one-line delta into a maintenance burden.

## Decision

Role defaults hold two variables: the full data (`X_defaults` / `desktop_profile` /
`module_defaults`) and an empty override slot (`X_overrides`, `desktop_overrides`). A third,
lazily-evaluated variable merges them:

```yaml
desktop_components: "{{ desktop_profile | combine(desktop_overrides, recursive=True) }}"
```

Inventory only ever writes the override slot, never the base data. The same mechanism appears at
three levels: desktop components, module apps (`module_defaults` + `modules.<name>`), and app
parameters (`app_defaults` + `app_params`).

## Consequences

Inventory carries deltas only (`bar: ~`) and the remaining entries survive; asymmetry between
desktops becomes data, not logic (GNOME ships `desktop_profile: {}` and its component loop simply
iterates nothing — no `when:`, no branching). The costs: the merged variable is a Jinja string
resolved at use-time, so it only exists once the owning role has been included (play 03's task
order is therefore load-bearing), and inventory writing to the base variable instead of the
override slot silently defeats the whole mechanism.

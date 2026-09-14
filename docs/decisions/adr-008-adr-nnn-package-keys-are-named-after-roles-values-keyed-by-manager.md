---
tags: [ansible, package-vocabulary, naming-convention]
---

# ADR-<NNN>: Package Keys Are Named After Roles, Values Keyed by Manager

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Every role needs its package list, and that list is the one thing that genuinely differs per
distro. Free-form package keys were rejected: with no convention, answering "which packages does
this role install?" means opening the role and following a variable.

## Decision

`packages.<role_name>` is a hard convention: the key in `group_vars/<distro>.yml` matches the
role name (`packages.component_bar` ↔ `roles/component_bar`), and every leaf is a flat
`{<manager>: [<pkg>, ...]}` dict. Depth varies where a role has variants — `packages.base` is two
levels, `packages.gpu.amd` three — and each role resolves its own path before handing a flat
manager dict downward. Native group syntax (`@core`, `@workstation-product-environment`) is used
where the manager really supports it.

## Consequences

Roles read one key and never learn which distro or manager answered: Fedora can route VLC through
flatpak while Arch uses pacman with no role change. The mapping is greppable in both directions.
The costs: a role rename is a two-file rename (role directory plus every distro's package key),
and a missing key fails at lookup rather than being skipped — deliberately loud, fixed by one
entry in the distro file.

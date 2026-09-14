---
tags: [ansible, null-sentinel, config-schema]
---

# ADR-<NNN>: The `~` Null Sentinel Is the Only Subtraction Operator

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Role defaults are merged into inventory values with `combine`, so omitting a key does not remove
it — the default survives. Something must be able to say "explicitly none". Alternatives: treat
omission as removal (impossible once defaults merge back in) and the literal `none` (rejected —
YAML parses it as the string `"none"`, which survives filtering and then fails looking up a role
by that name).

## Decision

`~` (equivalently `null` or an empty value) is the only way to subtract. Absence means "whatever
the default said". The sentinel works identically at all three levels: a desktop component
(`desktop_overrides: {bar: ~}`), a whole module (`modules: {gaming: ~}`), and a single app inside
a module (`neovim: ~`). `~` is the spelling used consistently; `none` is never used.

## Consequences

One concept covers three layers, and removing anything is a one-line inventory delta. The cost:
`neovim: {}` and an absent `neovim` are identical, so inventory alone never shows the full roster
— the roster lives in role defaults and must be read there. Every consumer of a merged dict must
also filter nulls (see the reject-filter ADR), or a nulled key resolves to a role named `None`.

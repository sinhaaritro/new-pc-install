---
tags: [ansible, ui-mode, single-select, derivation]
---

# ADR-NNN: ui_mode is a derived single-select, never a boolean

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

Apps should appear in TUI/GUI form only when the machine has a desktop. The obvious encoding is an
`install_gui: true` flag in inventory, but `wm_choice` already states whether a desktop exists, and
a second key restating the same fact drifts from the first.

## Decision

`group_vars/all.yml` derives `ui_mode: "{{ 'gui' if (wm_choice | default(None)) is not none else 'cli' }}"`,
a single-select of the same class as `wm_choice`, and everything downstream dispatches on it.

## Consequences

A headless machine sets `wm_choice: ~` and every consumer automatically resolves to `cli` with no
further edits. The cost is that `ui_mode` cannot be set independently: a headless box can never
deliberately install a GUI app, because there is no override key by design.

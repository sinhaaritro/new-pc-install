---
tags: [ansible, roster, ui-mode, modules]
---

# ADR-NNN: desktop-only apps are gated at the roster, never with when:

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

An app that only makes sense with a desktop (VS Code) must vanish on a headless box. Gating it with
`when: ui_mode == 'gui'` on the include leaves the task rendering in output and leaves a roster that
no longer states what the machine actually has.

## Decision

Workflow roles declare two rosters and combine them in defaults:
`module_defaults: "{{ module_cli | combine(module_gui if ui_mode == 'gui' else {}) }}"`.
An app placed in `module_gui` simply does not exist in the merged roster on a CLI box.

## Consequences

No `when:` appears in any workflow or app task for UI reasons, and `--list-tasks` output matches
reality. The roster is split across two dict keys, so "which apps does this workflow install?" is
read from the combination rather than from one list.

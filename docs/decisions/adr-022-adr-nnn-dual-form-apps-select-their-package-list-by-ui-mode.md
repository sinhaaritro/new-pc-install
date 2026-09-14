---
tags: [ansible, packages, ui-mode, vocabulary]
---

# ADR-NNN: dual-form apps select their package list by ui_mode

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

Some apps exist in both a CLI and a desktop form (git alone versus git plus lazygit and meld). The
role behaves identically in both cases; only the package list differs, so a second role per form
would duplicate tasks to express a data difference.

## Decision

`packages.<role_name>` may carry `cli:` and `gui:` sub-keys, and the role consumes
`package_source: "{{ packages.<role_name>[ui_mode] }}"`.

## Consequences

One role, one behaviour, two package lists — consistent with packages already being keyed by role
name. Package keys are no longer uniformly `{manager: [pkgs]}`: a consumer must know whether a key
is dual-form before indexing it.

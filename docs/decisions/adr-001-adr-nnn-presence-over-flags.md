---
tags: [ansible, presence-over-flags, config-schema]
---

# ADR-<NNN>: Presence Over Flags

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Configuration needs to answer two questions per thing: whether it runs and how it is configured.
The obvious encoding is a boolean beside the data (`install_hyprland: true` next to a Hyprland
block). Rejected: the boolean and the data are two keys for one fact and drift apart, and the
truth becomes "whichever key the role happened to read".

## Decision

A thing runs because a key exists and has a value; never because a separate boolean said so.
`wm_choice: hyprland` replaces `install_hyprland: true`; `modules.gaming: {steam: {}}` replaces
`gaming_enabled: true` plus a list elsewhere; `bar: ~` replaces `use_waybar: false`.

## Consequences

One key answers both questions, so drift is structurally impossible and inventory reads as a
description of the machine rather than a switchboard. The cost: there is no runtime toggle —
enabling or disabling anything is an inventory edit, and no `--extra-vars` boolean can skip a
component. Roles must therefore never test for an `*_enabled` variable.

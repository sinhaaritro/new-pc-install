---
tags: [ansible, role-archetypes, naming-convention]
---

# ADR-<NNN>: Four Role Archetypes With Prefix-Encoded Names

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

A repo of sixty roles needs a shape a reader can predict. The previous tree used flat,
unprefixed names (`browser`, `clipboard`, `gaming_steam`, `dev_neovim`) with no consistent
relationship between a role's name and its position in the run. Rejected: without a prefix
convention, plays cannot dispatch by string interpolation and must enumerate roles by hand.

## Decision

Every role is exactly one of four archetypes:

- **A — shared installer:** `install_packages`, dispatching by manager filename.
- **B — package-only:** one `include_role: install_packages` with a `package_source` path
  (`gpu`, `audio`, `network`, `firewall`, `ssh`, `base`, `snapshots`).
- **C — role with actual work:** packages plus its own tasks (`component_bar` stows waybar;
  `desktop_gnome` enables gdm).
- **D — orchestrator:** merges defaults with inventory, filters nulls, dispatches by name
  (`workflow_*`).

Names encode the layer: `desktop_<wm>`, `component_<name>`, `workflow_<module>`, `app_<name>`,
and bare names for system roles. Utility roles (`stow`, `dotfiles`) are named for what they do.

## Consequences

Plays dispatch by interpolation (`desktop_{{ wm_choice }}`, `workflow_{{ mod.key }}`,
`app_{{ app.key }}`) and never enumerate members, so adding a member touches no play. A reader
predicts a role's contents from its prefix, and the role↔package-key mapping stays one-to-one.
The cost: the prefixes are conventions with no mechanical enforcement — a misnamed role fails at
include time, and renaming one means renaming its package key and any `desktop_profile` /
`module_defaults` entry that points at it.

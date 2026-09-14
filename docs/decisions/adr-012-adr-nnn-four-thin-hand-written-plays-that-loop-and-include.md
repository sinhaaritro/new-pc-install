---
tags: [ansible, playbooks, orchestration]
---

# ADR-<NNN>: Four Thin, Hand-Written Plays That Loop and Include

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Plays are where data and logic tend to accumulate. Two alternatives were considered: per-machine
playbooks (duplication that drifts) and generating playbooks from a manifest, which the previous
tree did via `generators/manifest_to_playbook.py`. Both rejected — a generated playbook is a
second source of truth, and debugging happens in the generated file while fixes have to land in
the generator.

## Decision

Four numbered, hand-written plays hold no data and no logic; they loop and include:
`01_bootstrap.yml`, `02_harden.yml`, `03_desktop.yml`, `04_workflows.yml`. Play 03 includes
`desktop_{{ wm_choice }}` and then loops `desktop_components` — that order is load-bearing,
because `desktop_components` only exists once the desktop role has been included. Play 04 loops
`modules`. Both loops carry the null filter. No conditionals appear in plays 02–04.

## Consequences

The same play file provisions a Hyprland box (one desktop role plus five components) and a GNOME
box (one desktop role plus an empty loop) with no branching. Playbooks are readable in full in
under a screen each, and the generator and its Python dependency disappear. The cost: run
structure is fixed at four phases — anything that must happen between them is a manual step
(the reboot after play 01) or a new play.

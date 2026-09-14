---
tags: [ansible, plays, finalise, structure]
---

# ADR-NNN: five plays — 05_finalise is split out of the workflow play

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

ADR-012 fixed the tree at four thin plays. Reboot-adjacent, whole-machine work — `enable-linger`,
the default systemd target, the audit of enabled user units, the resolved-config summary — was
landing at the tail of the workflow play, where it is neither workflow work nor guaranteed to run
after every module.

## Decision

A fifth play, `plays/05_finalise.yml`, holds `user_services`, `default_target` and `summary`, and
runs after `04_workflows.yml` on every converge.

## Consequences

Amends ADR-012: the plays are thin as before, there are now five of them. Finalisation is
re-runnable on its own, independent of which modules are installed. Every document and runbook line
that says "plays 02-04" must be read as "02-05".

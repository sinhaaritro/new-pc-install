---
tags: [ansible, idempotence, check-mode, aur]
---

# ADR-<NNN>: Real Modules Over `command:`, With a Named Escape Hatch

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Every install could be a `command:` invocation, which is uniform and needs no collections.
Rejected: `command:` reports `changed` unconditionally and does not honour `--check`, so plays
become "always green, always noisy" and dry runs tell you nothing.

## Decision

Use real Ansible modules everywhere a proper one exists (`pacman`, `dnf`, `flatpak`,
`systemd_service`, `user`, `git`). Only managers without a module get a command, and their
command line lives in `group_vars` as `commands.<mgr>.install` (today: `paru` for the AUR), with
an honest `changed_when` derived from the tool's output. AUR tasks run `become_user:
{{ target_user }}` — not `become: false`, which in a play already running as root stays root, and
`paru` refuses to run as root.

## Consequences

Plays 02–04 are genuinely re-runnable and `--check` is meaningful, which makes the dry run a real
verification command. Change reporting reflects reality instead of noise. The costs: a dependency
on `community.general` (installed from `requirements.yml` on the live ISO), and the one
command-based manager needs hand-written `changed_when` logic that must be revisited if the
tool's output strings change.

---
tags: [ansible, phase-4, become, user-context, gates]
---

# ADR-021: Play 4 reuses the Play 3 pre_tasks gate and the sudo -u user-context wrapper

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

Play 4, like Plays 2 and 3, runs on the booted system and mixes root work
(pacman, usermod, ufw, /usr/local/bin) with user-session work (systemd --user
enables, podman system migrate, npm globals, ~/models downloads, ~/dotfiles
git init). The established pattern (spec 004 D1, sound role) is a play-level
`become: true` plus a `sudo -u <user> env XDG_RUNTIME_DIR=/run/user/<uid> …`
wrapper for user-context commands, and a pre_tasks gate (no live USB,
invoker in wheel, end_user exists). Options: extract the gate into a shared
role now, or keep it as per-play pre_tasks.

## Decision

Play 4 is a single play on localhost with play-level `become: true`; the
Play 3 gate pre_tasks are copied verbatim (failure messages kept per-play);
all user-session commands use the sudo -u XDG_RUNTIME_DIR wrapper so the
play works whether invoked by root or by the user.

## Consequences

The play remains self-contained and the house pattern stays uniform across
plays 2-4; the user-context wrapper covers every user-session surface
without role-local ad-hoc become juggling. Costs: the gate block is now
triplicated (plays 2, 3, 4) — accepted at three copies; a shared gate role
is the follow-up if a fourth copy appears. The wrapper requires the user's
XDG runtime dir to exist (the user logged in at least once), which the
post-Phase-3 bring-up guarantees.

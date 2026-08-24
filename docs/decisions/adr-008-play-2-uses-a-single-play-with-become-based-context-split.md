---
tags: [ansible, phase-2, become, context]
---

# ADR-001: Play 2 Uses a Single Play with become-Based Context Split

Status: Accepted
Date: 2026-08-23
Source: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md

## Context

Phase 2 runs on the booted system as the normal user (in `wheel`), and its modules
mix root and regular-user commands. The user asked whether mixing root and normal-user
commands was hard enough to warrant two separate plays (one as root, one as user). The
genuine user-context needs are shallow — only `aur`, `ssh`, and the PipeWire user
sockets in `sound` — while the rest is `sudo`/root. Ansible cannot express `systemctl
--user` natively.

## Decision

Play 2 is a single playbook (`20-hardening.yml`). Root tasks set `become: true`;
user-context tasks run as the user with `become: false`. `systemctl --user` is invoked
via a `shell` task wrapping `sudo -u <user> XDG_RUNTIME_DIR=/run/user/<uid> systemctl
--user …`. Two plays are not used.

## Consequences

One inventory and one run cover both contexts; the shallow split stays simple. The
cost is a small `sudo -u` wrapper idiom for user-systemd, which assumes the user is
logged in (true post first-reboot). It avoids the double-inventory/double-run overhead
of a root-play + user-play split.

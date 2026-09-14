---
tags: [ansible, systemd, user-services, linger]
---

# ADR-<NNN>: User-Scope Services Are Enabled, Never Started

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Components such as `hypridle` run as user services, but provisioning happens when the target user
has no graphical session and possibly no session at all. `state: started` was rejected: it
requires a live user bus and fails or hangs during provisioning.

## Decision

User-scope units are declared with `systemd_service: {scope: user, enabled: true}` under
`become_user: {{ target_user }}` with `XDG_RUNTIME_DIR: /run/user/{{ target_uid }}` in the task
environment. `enabled: true` works without a session; `state: started` is never used — the final
manual reboot starts them. `target_uid` is read with the `getent` module after user creation
rather than hardcoding 1000. Play 02 runs `loginctl enable-linger {{ target_user }}` for anything
that must run without a login.

## Consequences

Provisioning never depends on a logged-in session, and the enable step is idempotent. The costs:
nothing a role enables is running when the play finishes, so a final reboot is part of the
documented procedure, and any role that enables a user unit must carry the `XDG_RUNTIME_DIR`
environment block and depend on `target_uid` having been resolved.

---
tags: [ansible, bootstrap, idempotence, live-iso]
---

# ADR-<NNN>: Play 01 Is the Only Non-Re-Runnable, Distro-Branching Play

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Disk partitioning, bootstrapping and first-user creation cannot be expressed idempotently in any
useful sense — the play wipes a disk. Making it re-runnable was rejected as meaningless work, and
so was folding it into play 02, which would make every routine run one typo away from a wipe.

## Decision

`plays/01_bootstrap.yml` runs from the live ISO, as root, for disaster recovery only. It is not
re-runnable and is not expected to be. It is also the only place the distro is branched on, via
`include_role: bootstrap_{{ distro }}`. It contains no `become:` anywhere — the ISO session is
already root and `target_user` does not exist yet — and it guards itself with a `lsblk` display
plus a typed `YES` confirmation before wiping, and a hidden password prompt hashed with
`password_hash('sha512')` under `no_log: true`. Plays 02–04 are idempotent and re-runnable.
Machines installed another way (Fedora via Anaconda) simply start at play 02.

## Consequences

The dangerous operation is isolated in one file with an explicit human gate, while everyday
provisioning is safely repeatable. The distro seam exists for `bootstrap_<distro>` without any
other role knowing about distros. The costs: the reboot between plays 01 and 02 is manual
(Ansible's `reboot` module cannot survive leaving the live ISO), the final reboot after play 04
is manual too, and a partially failed play 01 is restarted from a clean wipe rather than resumed.

---
tags: [ansible, chroot, live-usb, two-stage, no-sudo]
---

# ADR-004: Two-Stage Install Pattern (Live-USB Host → Chroot Target)

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

Ansible cannot run inside the not-yet-existing target system. The install therefore has two
privilege/environments: work done on the live USB against `/mnt` (partition, format,
pacstrap, write configs) and work that needs the new system's `pacman`/`systemctl`
(NetworkManager, user/sudo, GRUB). We had to decide how to express the second stage and
whether to split the play by sudo vs non-sudo.

## Decision

Use a two-stage pattern in a single play: a host stage on the live USB (plain tasks against
`/mnt`), and a chroot stage where target-system commands run via a `shell` task wrapping
`arch-chroot /mnt`. No `become`/sudo is used anywhere — on the live USB the operator is
already root, so there is no privilege boundary to split on.

## Consequences

Keeps Phase 1 as one coherent play with no artificial sudo/non-sudo split; the chroot stage
is a clean, well-supported Ansible pattern. Costs a convention that target-system commands
must be wrapped in `arch-chroot` (and a note that `become` only becomes relevant in a later
play that runs on the installed system as a normal user). Rejected splitting into separate
sudo/non-sudo plays — on the live USB everything is root, so the split would add no value.

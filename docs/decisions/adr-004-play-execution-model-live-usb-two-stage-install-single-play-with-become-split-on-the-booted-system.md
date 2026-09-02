---
tags: [ansible, chroot, live-usb, two-stage, become, context, user-context]
---

# ADR-004: Play Execution Model — Live-USB Two-Stage Install; Single Play with become Split on the Booted System

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

Ansible cannot run inside the not-yet-existing target system, so the install has two
privilege/environments: work done on the live USB against `/mnt` (partition, format,
pacstrap, write configs) and work that needs the new system's `pacman`/`systemctl`
(NetworkManager, user/sudo, GRUB). We had to decide how to express the second stage
and whether to split the play by sudo vs non-sudo. Later, Plays 2 and 4 run on the
*booted* system as the normal user (in `wheel`) and mix root and regular-user
commands; the question was whether that mixing warranted two separate plays (one as
root, one as user), and how to cover user-session work (systemd `--user`, npm
globals, `~/models` downloads) uniformly.

## Decision

**Play 1 (live USB):** a two-stage pattern in a single play — a host stage on the
live USB (plain tasks against `/mnt`), and a chroot stage where target-system
commands run via a `shell` task wrapping `arch-chroot /mnt`. No `become`/sudo
anywhere: on the live USB the operator is already root, so there is no privilege
boundary to split on. Target-system commands must be wrapped in `arch-chroot`.

**Plays 2-4 (booted system):** each is a single play on localhost with play-level
`become: true`. Root tasks set `become: true`; user-context tasks run as the user
with `become: false`. `systemctl --user` — the one thing Ansible cannot express
natively — is invoked via a `shell` task wrapping `sudo -u <user> env
XDG_RUNTIME_DIR=/run/user/<uid> systemctl --user …`; the same wrapper covers every
user-session surface (npm globals, podman migrate, `~/models` downloads, `~/dotfiles`
git). All user-session commands use it, so the play works whether invoked by root or
by the user. Two plays are not used. The per-play pre_tasks gate (no live USB,
invoker in `wheel`, `end_user` exists) is kept per-play with play-specific failure
messages; extracting a shared gate role is the follow-up if a fourth copy appears.

## Consequences

Phase 1 stays one coherent play with no artificial sudo/non-sudo split; the chroot
stage is a clean, well-supported Ansible pattern. On the booted system, one
inventory and one run cover both contexts; the shallow split (only `aur`, `ssh`, and
the PipeWire user sockets in `sound` truly need user context in Play 2) stays simple,
and the house pattern is uniform across Plays 2-4. Costs: the `arch-chroot` wrapping
convention in Play 1; a small `sudo -u` wrapper idiom that assumes the user's XDG
runtime dir exists (the user logged in at least once — guaranteed post first-reboot
/ post Phase 3 bring-up); the gate block is triplicated (Plays 2, 3, 4), accepted at
three copies. Rejected: separate sudo/non-sudo plays for Play 1 (on the live USB
everything is root — no value), and a root-play + user-play split for Plays 2-4
(double inventory/double run for a shallow split).

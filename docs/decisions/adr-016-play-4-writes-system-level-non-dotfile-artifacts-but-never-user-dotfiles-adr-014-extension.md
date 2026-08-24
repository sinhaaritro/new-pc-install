---
tags: [ansible, phase-4, stow, dotfiles, config-boundary]
---

# ADR-016: Play 4 writes system-level non-dotfile artifacts but never user dotfiles (ADR-014 extension)

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

ADR-014 (Play 3) established that automation writes no user dotfiles — stow
owns config. Phase 4 modules, however, require a few artifacts that are not
preference content: the devpod binary (root-owned, /usr/local/bin), the
rootless-podman subuid/subgid range (/etc/subuid state), the ufw 8080 rule,
and the llama-server user systemd unit (a service definition whose model
list is delegated to the stow-owned ~/models/config.ini by path). Options:
strict config-free (leaves llama-server unenableable as a service, which
the inference doc's Path B explicitly wants) or writing configs (collides
with stow, violates ADR-014).

## Decision

Play 4 writes exactly four named system-level, non-dotfile artifacts — the
devpod binary, the podman subuid/subgid range, the ufw 8080/tcp rule, and
the llama-server.service user unit file — and prints "your stow package
should provide X" notes for everything else. The unit-file role notes that
the user may prefer stow ownership and delete it.

## Consequences

The inference and devpod modules are fully operable (service enabled, LAN
reachable, binary on PATH) while the user's stow repo remains the single
source of truth for all preference content. Costs: a named exception class
("service unit definitions and root-owned system artifacts") must stay
closed — any future Phase 4+ artifact must be classified as either that
class or stow-owned, case by case. The duplicate-ownership edge case for
the unit file (playbook writes, stow may also ship it) is resolved by
print-not-fail: the role states the stow option.

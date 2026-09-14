---
tags: [ansible, install-packages, filename-dispatch]
---

# ADR-<NNN>: One Shared Installer Dispatching by Manager Filename

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Packages must be installed by whichever manager the distro file named. The alternative is a
`when: ansible_distribution == ...` chain inside each role — which the previous tree used (for
example `gpu/tasks/{amd,intel,nvidia}.yml` selected by conditionals). Rejected: adding a distro
or a manager then edits every role that installs anything.

## Decision

A single `install_packages` role takes `package_source: {<manager>: [<pkg>, ...]}`, loops the
manager keys, and includes `managers/{{ mgr.key }}.yml` with `pkg_list` set. Each manager file
contains exactly one task: `community.general.pacman`, `ansible.builtin.dnf`,
`community.general.flatpak`, and the `aur` command wrapper. No `when:` chains, no distro
branching anywhere outside play 01.

## Consequences

Adding zypper is adding `managers/zypper.yml`; nothing else in the repo changes. Roles shrink to
one include and stay ignorant of manager syntax, and the dispatch is readable from a directory
listing. The cost: a manager key present in a distro file with no matching file fails at include
time, and the loop is per-manager rather than per-package, so a single bad package name fails the
whole manager batch for that role.

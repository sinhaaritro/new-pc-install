---
tags: [ansible, live-iso, bootstrap-script, arch-linux]
---

# ADR-<NNN>: A `bootstrap.sh` Carries the Live-ISO Preamble

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Before Ansible can run at all, the Arch live ISO needs a handful of steps that Ansible itself
cannot perform: enlarging the tiny `cowspace` ramdisk, bringing up networking, refreshing the
keyring, installing `git` and `ansible`, and installing the Galaxy collections. Documenting them
in a README was rejected — they are executed from a bare TTY on someone else's machine, and the
`cowspace` remount in particular will not be remembered.

## Decision

A `bootstrap.sh` at the repo root holds the preamble verbatim:

```bash
mount -o remount,size=2G /run/archiso/cowspace
iwctl
pacman -Sy archlinux-keyring
pacman -S --noconfirm git ansible
git clone <repo> && cd repo/ansible
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i inventory/hosts.yml plays/01_bootstrap.yml
```

## Consequences

The ISO-side procedure is executable rather than remembered, and it is versioned with the tree it
bootstraps. The costs: it is Arch-ISO specific (other distros never run it, matching the play-01
boundary), it duplicates a few package names that also appear in `group_vars`, and the interactive
`iwctl` step means it is a guided script rather than a fully unattended one.

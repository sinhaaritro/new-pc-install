---
tags: [ansible, group-vars, distro-vocabulary]
---

# ADR-<NNN>: Distro Var Files Are Self-Contained, With No Shared `all.yml`

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Arch and Fedora share key *names* and almost nothing else. The obvious DRY move is a shared
`group_vars/all.yml` holding the common parts — which is what the previous tree (`ansible_bck`)
did. Rejected: Ansible replaces rather than merges dicts across `all.yml` and
`group_vars/<distro>.yml`, so the "shared" `packages` dict is silently clobbered whole by the
distro file, and the file that looks authoritative is the one being ignored.

## Decision

Each `group_vars/<distro>.yml` is complete and self-contained; nothing is shared between distro
files and no `all.yml` exists. Both desktop stacks, all components and all apps live in the same
file; only the selected keys are ever read, and unused keys cost nothing.

## Consequences

Small duplication is accepted in exchange for the absence of silent clobbering: one file per
distro is the whole truth for that distro, readable top to bottom. Adding a distro is adding one
file in the same shape and moving the host to that group — no existing file changes. The cost:
a package added to one distro must be remembered for the others, and a key missing on a distro
fails loudly at lookup time (correct behaviour — the fix is one entry in that distro file).

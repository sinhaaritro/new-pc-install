---
tags: [ansible, inventory, distro-groups]
---

# ADR-<NNN>: One Inventory File, One Host, Distro as the Group Name

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Each run provisions exactly one machine, and the distro must select the right vocabulary file.
The alternative was a plain `distro:` variable plus an `include_vars` lookup in every play.
Rejected: it is lookup logic that must be repeated and kept in sync, when Ansible already loads
`group_vars/<group>.yml` for free.

## Decision

`inventory/hosts.yml` holds one host under a group named after its distro
(`all.children.arch.hosts.thispc`), which auto-loads `group_vars/arch.yml` with zero lookup
logic. Swapping machines means swapping this one file. `ansible_connection: local` is declared
once on the host, covering the live ISO and every later play. The distro string is *also*
declared as `distro:` inside the distro file for the one place that needs it — `include_role:
bootstrap_{{ distro }}` in play 01.

## Consequences

A second machine is the same file with different values: no `target_disk`/`partitions` on an
already-installed box, no `desktop_overrides` where the profile is empty. Group membership is the
only distro switch in the repo. The cost: multi-machine fleets are not supported by this
inventory shape — each machine is its own file (or its own checkout), and shared facts between
machines have nowhere to live by design.

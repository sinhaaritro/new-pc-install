---
tags: [ansible, variable-precedence, layering, architecture]
---

# ADR-<NNN>: Four Variable Layers on Ansible's Native Precedence

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Variables need a single obvious home so "where does X go?" is answerable without reading the
whole repo. Alternatives considered: a custom vars plugin, and Ansible's global
`hash_behaviour=merge`. Both were rejected — global merge semantics are invisible at the call
site, change behaviour for every collection in the run, and replace a documented precedence
ladder with bespoke rules.

## Decision

Four layers, resolved by Ansible's built-in precedence (higher wins), with no custom merge logic
anywhere except the explicit two-variable trick:

1. `inventory/hosts.yml` — changes every machine: "what is THIS box?"
2. `group_vars/<distro>.yml` — changes per distro: "how is it spelled here?"
3. `roles/*/defaults/main.yml` — almost never changes: "what if nobody said?"
4. `roles/*/tasks/*.yml` — logic, not data: "how is it done?"

Placement is decided by the first "yes": differs between two machines on the same distro →
inventory; differs between two distros on the same machine → `group_vars`; otherwise → role
defaults.

## Consequences

Precedence is a property of Ansible rather than of this repo, so it survives upgrades and is
familiar to anyone who knows Ansible. Four boundaries give four responsibilities: inventory never
knows a package name, the distro file never knows play order, the role never knows a package
manager's syntax. The cost is that dicts are *replaced* across layers rather than merged, which
forces the two-variable trick wherever a partial override is needed.

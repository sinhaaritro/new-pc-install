---
tags: [ansible, greenfield, rebuild, legacy-tree]
---

# ADR-<NNN>: Greenfield Rebuild — the Old Tree Is Ignored Entirely

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

A previous implementation exists in `ansible_bck/`: a shared `group_vars/all.yml`, distro
branching inside roles, a `manifest_to_playbook.py` generator, a Makefile, and roughly sixty flat
unprefixed roles. Two alternatives were considered and rejected: an incremental in-place refactor
(every one of those traits contradicts a decision in this spec, so it would be a rewrite carried
out under the constraint of never being broken), and keeping the old tree as a reference corpus to
copy package lists and quirks from (that is how the old shape leaks back in — the point of the
rebuild is to have no baggage).

## Decision

Build the new `ansible/` tree from scratch against the pattern alone. `ansible_bck/` is **not**
consulted: no file, package list, role name or task is migrated or copied from it, and no
decision in this spec cites it as a source. The pattern document is the only input. The old
directory is dead weight in the tree and may be deleted at any time without affecting this spec.

## Consequences

Every file in the new tree obeys the pattern from commit one, with no half-translated leftovers
and no naming inherited from the old scheme. Review is simple: anything that does not fit the
four layers and the four archetypes is wrong, with no "that came from the old tree" exemption.
The cost: package lists, distro quirks and hardware workarounds that the old tree had already
gotten right are re-derived from scratch, so the first provisioning run is expected to surface
gaps that were previously solved.

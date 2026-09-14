---
tags: [ansible, variants, inventory, filename-dispatch]
---

# ADR-<NNN>: Mutually-Exclusive Implementations Are Inventory-Selected Variants

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Some concerns have several implementations of which a machine wants exactly one: a GPU driver
stack (amd/intel/nvidia), an audio server, a snapshot mechanism (snapper/timeshift). The
alternative — one role per implementation (`roles/snapper`, `roles/timeshift`) chosen by whoever
includes it — was rejected: the choice then lives in the play as well as in the data, so two
places know about it and adding an implementation edits the play.

## Decision

The role ships every implementation and inventory names one through a `<concern>_variant` key:
`gpu_variant`, `audio_variant`, `snapshot_variant`. The role resolves its own packages through
the variant (`packages.snapshots[snapshot_variant]`) and, when the implementations need their own
configuration, includes `variants/{{ <concern>_variant }}.yml` — the same filename dispatch the
package managers use. Suitability (does this filesystem support snapshots?) is the inventory
author's judgement, not a runtime check. `~` selects nothing and the role is skipped, so
"disabled" needs no extra mechanism.

## Consequences

Adding an implementation is one `variants/<name>.yml` file plus one
`packages.<role>.<variant>` key; no play and no other role changes, and the set of supported
choices is readable from a directory listing. The whole configuration of a machine stays in
inventory — which driver, which audio server, which snapshot tool, or none. The costs: a variant
name with no matching packages key or variant file fails at lookup/include time rather than being
skipped (deliberately loud), and nothing validates that the named variant makes sense for the
machine — choosing `snapper` on a non-btrfs root fails during the run, not at plan time.

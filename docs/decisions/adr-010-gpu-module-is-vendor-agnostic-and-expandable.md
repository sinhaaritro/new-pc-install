---
tags: [ansible, gpu, nvidia, vendor-agnostic]
---

# ADR-003: GPU Module Is Vendor-Agnostic and Expandable

Status: Accepted
Date: 2026-08-23
Source: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md

## Context

The Phase 2 GPU module is written for NVIDIA, but the user wants `amd`, `intel`, and
`none` to be first-class, expandable options even though no driver code exists for them
yet. A per-vendor role would create N-fold role sprawl before a second vendor has real
code.

## Decision

A `gpu_vendor` inventory var (`nvidia` | `amd` | `intel` | `none`) selects the path in
a single `gpu` role. `nvidia` and `none` are implemented; `amd` and `intel` are
declared and hit a clear "not implemented yet" gate. All per-vendor values (packages,
mkinitcpio modules, GRUB cmdline, hook content) live in `vars/distros/archlinux.yml`
under a `gpu:` map. Adding a vendor is data plus one task branch.

## Consequences

Later vendors (AMD, Intel) are added without a role rewrite, mirroring the existing
`fstype`/`bootloader` (spec 003) and `cpu_vendor` (spec 002) selectable patterns. The
cost is an unimplemented-option gate that must be kept honest (clear message, no
silent no-op) until a vendor lands.

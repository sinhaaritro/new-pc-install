---
tags: [ansible, microcode, cpu-vendor, inventory]
---

# ADR-<NNN>: CPU Microcode Is An Optional Inventory-Selected Vendor Variant

Status: Accepted
Date: 2026-09-17
Source: docs/specs/006-cpu-microcode-nvidia-initramfs-robustness-and-host-overridable-fonts.md

## Context

Arch installs CPU microcode via a vendor-specific package (`amd-ucode` or `intel-ucode`). The
alternative was to hardcode `amd-ucode` in the base package list or to make `cpu_vendor` a required,
asserted variable. Hardcoding ignores the vendor; a required assert breaks any host that
deliberately declares no vendor, when "install nothing" is a legitimate choice for a box whose
vendor is unknown or whose microcode is handled elsewhere.

## Decision

Microcode is an inventory-selected vendor variant resolved through a shared `x_packages.ucode` map
(`amd` -> `amd-ucode`, `intel` -> `intel-ucode`). `cpu_vendor` is OPTIONAL: an absent or `~` value
installs nothing (no default, no assert). It is installed at the chroot pacstrap (`base_install`)
and again in the converge path (`base_packages`); both steps no-op when `cpu_vendor` is unset.

## Consequences

A host names its vendor with one key and the correct microcode lands at first boot and is
re-converged on live runs; a host that omits the key cleanly installs no microcode rather than
failing. The cost: there is no runtime check that the declared vendor matches the actual silicon —
an Intel box mis-labelled `cpu_vendor: amd` would install the wrong (and inert) package, the same
"suitability is the inventory author's judgement" stance ADR-018 takes for other variants.

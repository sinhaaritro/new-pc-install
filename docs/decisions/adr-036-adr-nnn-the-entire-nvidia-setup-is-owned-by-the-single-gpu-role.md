---
tags: [ansible, nvidia, gpu, initramfs, single-owner]
---

# ADR-<NNN>: The Entire NVIDIA Setup Is Owned By The Single Gpu Role

Status: Accepted
Date: 2026-09-17
Source: docs/specs/006-cpu-microcode-nvidia-initramfs-robustness-and-host-overridable-fonts.md

## Context

A correct NVIDIA setup is more than installing the driver package: it needs the GRUB kernel cmdline
(`nvidia_drm.modeset=1 nvidia_drm.fbdev=1`), the initramfs `MODULES`, removal of the `kms` hook, and
a `PostTransaction` pacman hook that rebuilds the initramfs on every future driver/kernel
transaction — otherwise the first `linux` update breaks the box. The alternatives were to split the
GRUB cmdline into `bootloader` (which writes `/etc/default/grub` at bootstrap in play 01) or to
revive the old tree's per-vendor role files (`gpu/tasks/{amd,intel,nvidia}.yml`). A split owner
means two roles must stay in sync for one driver; per-vendor role files are rejected by ADR-009.

## Decision

The `gpu` role is the single owner of the whole NVIDIA setup, gated on `gpu_variant` matching
`nvidia.*`. All NVIDIA specifics live in a `gpu_nvidia` distro-data block in
`group_vars/arch.yml` (grub_cmdline, mkinitcpio_modules, per-variant hook_target). The `gpu` role
sets the GRUB cmdline, writes `/etc/pacman.d/hooks/nvidia.hook`, sets the initramfs `MODULES`,
removes the `kms` hook, and runs `mkinitcpio -P` only when an edit changed. The `bootloader` role is
not modified.

## Consequences

One role owns one driver end-to-end, so the GRUB, initramfs, and rebuild-hook changes can never
drift apart, and adding a non-NVIDIA vendor is a `gpu_nvidia`-block plus data change, not a play
change. The cost is an accepted timing trade-off: the `gpu` role runs in play 02 (post-boot), so the
very first boot carries a generic initramfs without the NVIDIA `MODULES`; the `PostTransaction` hook
carries them in on the next driver/kernel transaction. That is acceptable for a normal NVMe root
where the GPU is not needed inside the initramfs, but a machine that must load the GPU pre-init
would need the modules in the first initramfs.

---
tags: [ansible, fonts, fontconfig, three-level, layering]
---

# ADR-<NNN>: Fonts Resolve Across Three Levels - Host, Arch-Group, Role Default

Status: Accepted
Date: 2026-09-17
Source: docs/specs/006-cpu-microcode-nvidia-initramfs-robustness-and-host-overridable-fonts.md

## Context

Fonts have two distinct concerns: which font *packages* to install, and how the installed fonts are
*layered* (which is the primary, what the fallback order is). The alternatives were to fold fonts
into `theming` (spec 002's wording) with a static `/etc/fonts/local.conf`, or a two-level
(host-overrides-arch) list. Folding conflates theme config with font installation and a static
`local.conf` cannot change the primary font per host; ADR-011 says the system `local.conf` is owned
by the role that installs fonts. A two-level list cannot express "the arch group ships a sensible
default, the role ships a last-resort default, and the host tunes on top of both."

## Decision

A dedicated `fonts` role (play 02, after `aur_helper`) resolves BOTH the package list and the
fontconfig profile across three levels, highest priority first: host (`hosts.yml`), arch-group
(`x_packages.fonts` + `x_packages.fonts.profile` in `group_vars/arch.yml`), and role default
(`fonts_profile` in the role's `defaults`). The main font (`mono`/`sans`) is the first non-empty
value walking host -> arch-group -> role. The fallback chain is the host + arch-group + role lists
concatenated with per-name dedupe (the first/highest-priority occurrence wins) and order preserved
within each level. The role renders the resolved profile to `/etc/fonts/local.conf` and runs
`fc-cache -fv`. The font packages currently in `theming` move into this role so one role owns all
font installation.

## Consequences

A host tunes the primary font or prepends a fallback with a small override and never edits the
config file; a host that sets nothing inherits the arch-group default, and a host that even omits
the arch-group key inherits the role default. The dedupe keeps a font from appearing twice at two
priorities, and per-level order is preserved so a curated fallback chain stays curated. The cost:
the resolution is a custom three-level merge (not the stock ADR-007 two-variable combine), so it is
slightly more code to get right and to read — the fallback concatenation/dedupe is the non-obvious
part and is pinned by the role's defaults contract.

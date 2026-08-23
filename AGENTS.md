# Project - New PC Install Guide

## Description
A modular PC installation and configuration guide. Documentation is split into logical domains (OS, hardware, peripherals, software) so components can be mixed and matched without clutter.

## Tech Stack

- Markdown documentation (domain-split)
- QMK/VIA keyboard firmware definitions (JSON)
- Shell scripts for interactive install/visualization helpers

## Repo map

- `os/` - OS installation & setup (Arch Linux, Windows)
- `hardware/` - BIOS, lighting, motherboard config
- `peripherals/` - keyboards, mice, accessories (QMK/VIA definitions)
- `software/` - app configs per OS (audio, graphics, etc.)
- `docs/` - shared space: `docs/specs/`, `docs/decisions/`, `docs/reference/`, and `docs/temp/` (gitignored scratchpad); human landing page at `docs/README.md`
- `.agents/` - machine space: `MAP.md` (generated skill index), `.agents/rules/`, `.agents/skills/`, `.agents/scripts/`
- `README.md` - human landing page / domain index

## Commands

- Build: n/a (documentation repo - no build step)
- Test: n/a (no test suite; verify links and scripts manually)
- Lint: n/a

# DEV AGENT

Read `.agents/rules/system.md` (behavioral contract - read it and obey)

---
tags: [ansible, aur, opencode, packaging]
---

# ADR-NNN: prefer the prebuilt AUR package where upstream ships one

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

opencode is available from the AUR both as a source package and as `opencode-bin`. Building it from
source adds a second compile toolchain that must be maintained and re-run on every release, for a
binary upstream already publishes.

## Decision

`app_opencode` installs `opencode-bin` through the existing `aur:` manager key. Source builds are
reserved for apps whose build flags are the reason for installing them, such as llama.cpp.

## Consequences

Converge time stays short and no build dependency enters the package vocabulary for this app. The
trade-off is trusting the packager's binary and accepting whatever build options it was compiled
with; switching to a source build later is a one-line change to `packages.app_opencode`.

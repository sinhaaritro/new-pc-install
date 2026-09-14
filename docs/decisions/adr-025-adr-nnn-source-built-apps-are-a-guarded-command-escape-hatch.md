---
tags: [ansible, source-build, cmake, idempotence]
---

# ADR-NNN: source-built apps are a guarded command escape hatch

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

llama.cpp must be compiled locally because its CUDA and AVX-512 flags are the whole point of
installing it, and no Ansible module builds a CMake project. ADR-010 allows `command:` only as a
named escape hatch (the AUR helper); an unguarded cmake call would also recompile on every converge.

## Decision

Source-built apps use the `git` module plus two `command:` cmake calls (configure, build), both
guarded by `when: src.changed or not <artifact>.stat.exists`, where `src` is the registered result
of the `git` task.

## Consequences

Extends ADR-010's escape-hatch list beyond the AUR command. A no-op `git pull` costs nothing, and a
missing build directory still triggers a rebuild. The cost is that this role's real effect is
invisible to `--check`: the cmake tasks are commands, so the only proof of a working build is the
artifact on disk.

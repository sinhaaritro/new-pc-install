---
tags: [ansible, llama-cpp, cmake-flags, defaults]
---

# ADR-NNN: CMake flags are a YAML list in role defaults

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

The llama.cpp build is defined by its flags (`-DGGML_CUDA=ON`, `-DCMAKE_CUDA_ARCHITECTURES=89`,
the AVX-512 set). Holding them as one shell string means a machine with a different GPU cannot
change them without editing the role, and a diff cannot show which flag moved.

## Decision

`app_llamacpp/defaults/main.yml` holds `cmake_flags` as a list, joined at call time with
`{{ cfg.cmake_flags | join(' ') }}`; inventory replaces or extends the list through `app_params`.

## Consequences

A second machine overrides one key in inventory and the Ada box is untouched. The defaults are
deliberately machine-specific — `-DGGML_NATIVE=ON` bakes in the build host's CPU features and
`-DCMAKE_CUDA_ARCHITECTURES=89` is Ada-only — so build artifacts are never portable or cacheable
between machines, and the role file carries a comment saying so.

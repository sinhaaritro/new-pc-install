---
tags: [ansible, ai, model-storage, configuration]
---

# ADR-NNN: model storage is one key owned by ai_model_store

Status: Accepted
Date: 2026-09-14
Source: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md

## Context

Several AI apps need the same model directory, and its final location is undecided — it will likely
move to dedicated storage. If each app carried its own path default, relocating the models would be
an edit in every AI role.

## Decision

`ai_model_store` owns `model_dir` (default `/home/{{ target_user }}/.local/share/models`), creates
and chowns the directory, and exports it from `/etc/profile.d/ai-models.sh`. Every other AI role
reads `model_dir` and hardcodes no path.

## Consequences

Moving models to a dedicated NVMe is one line in inventory. Until that line exists the models live
on the root filesystem under the user's home, which is the wrong place for tens of gigabytes; the
default is a placeholder, not a recommendation.

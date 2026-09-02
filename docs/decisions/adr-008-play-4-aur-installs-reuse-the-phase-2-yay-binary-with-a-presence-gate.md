---
tags: [ansible, phase-4, aur, yay, dependencies]
---

# ADR-008: Play 4 AUR installs reuse the Phase 2 yay binary with a presence gate

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

Three Phase 4 modules need AUR packages (inference: llama-cpp-cuda;
containers: lazydocker; agents: claude-desktop). The `yay` AUR helper is
built by the Phase 2 `aur` role (not a pacman package). Options: a dedicated
AUR helper role for Play 4 (duplicates the house pattern), a silent skip
when yay is absent (hides the dependency), or a presence gate with a clear
failure message. The claude-desktop AUR build is also known-flaky upstream
(the doc itself falls back to a manual AppImage).

## Decision

Play 4 pre_tasks check `which yay`; absent = hard failure with "run Play 2
with enable_aur: true first". Module roles invoke `yay -S --noconfirm <pkg>`
following the Phase 2 `aur` role's build pattern. The agents role treats a
claude-desktop build failure as a warning: it prints the manual AppImage
instructions and continues instead of failing the play.

## Consequences

No new AUR machinery; the Phase 2 helper remains the single AUR path. The
presence gate makes the Play 2 dependency explicit at the top of the run.
Costs: the one warning-not-fail exception (claude-desktop) means the agents
module can report "applied" with a known gap — the printed instructions
are the contract for closing it. If more flaky AUR packages appear, the
warn-and-print pattern generalizes.

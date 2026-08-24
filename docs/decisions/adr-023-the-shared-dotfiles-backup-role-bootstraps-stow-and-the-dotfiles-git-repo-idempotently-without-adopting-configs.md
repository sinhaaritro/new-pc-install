---
tags: [ansible, phase-4, stow, dotfiles, git]
---

# ADR-023: The shared dotfiles-backup role bootstraps stow and the dotfiles git repo idempotently, without adopting configs

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

The Phase 4 shared module (dotfiles-backup.md) sets up GNU Stow + a git
repo at ~/dotfiles as the ownership boundary for all dotfiles (ADR-014/016
depend on it existing). Its doc's Step 3-5 (move existing configs into the
repo, `stow --adopt`, `git checkout -- .`) are interactive,
user-judgment steps: --adopt moves live files into the repo and can
overwrite repo versions. Options: automate the adopt/move (destructive to
user state), do nothing (the boundary the other roles' stow notes point at
never gets created), or bootstrap the safe parts only.

## Decision

The dotfiles_backup role installs stow (pacman), creates ~/dotfiles as a
git repo only if it does not already exist (never `git init` over an
existing repo), and prints the naming convention, the suggested stow
package list, and the adopt/checkout workflow as instructions. It moves no
files and writes no stow package contents.

## Consequences

The stow boundary the other 18 roles' notes reference is guaranteed to
exist after a Play 4 run, idempotently and non-destructively. Costs: the
user still performs the per-package adopt/move by hand (exactly the
judgment ADR-014 assigns to the user), and an existing ~/dotfiles repo with
a different layout is left untouched — the role's prints assume the
doc's convention. Follow-up: if the adopt workflow is ever deemed safe to
script (e.g. repo empty, target files untracked), a flag-gated task can
extend this role.

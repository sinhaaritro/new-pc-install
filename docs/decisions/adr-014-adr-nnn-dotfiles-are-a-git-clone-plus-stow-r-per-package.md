---
tags: [ansible, dotfiles, stow, utility-roles]
---

# ADR-<NNN>: Dotfiles Are a Git Clone Plus `stow -R` Per Package

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Configuration files have to reach the home directory. Templating or copying each one from the
Ansible repo was rejected: it makes Ansible a second home for configs that already live in a
dotfiles repository, and every edit then has to be made twice.

## Decision

Two utility roles. `dotfiles` clones `dotfiles_repo` to `dotfiles_path` once, in play 02, as
`target_user`. `dotfiles_repo` is a **machine fact and lives in inventory** (layer 1), not in role
defaults — every user has a different config repo, and a repo URL that differs between two
machines on the same distro is inventory data by the layering rule. The role's defaults carry only
the convention (`dotfiles_path`), never a URL. `stow` runs
`stow -d {{ dotfiles_path }} -t {{ stow_target }} -R {{ stow_package }}` as `target_user`, with
`changed_when: "'LINK' in r.stderr"`. Component and app roles call `stow` with `stow_package`
named identically to their own key, so the role↔stow-package mapping needs no lookup table.

## Consequences

The dotfiles repo stays the single source of truth; `-R` (restow) makes the operation
re-runnable, and the stderr-based `changed_when` keeps reports honest instead of "changed" on
every run. Pointing a machine at a different dotfiles repo is a one-line inventory edit with no
role change. The costs: GNU `stow` becomes a hard dependency of every archetype-C role,
`dotfiles_repo` is undefined until inventory supplies it (play 02 fails loudly on a host that
omits it — deliberate, since there is no sensible default), symlink conflicts with pre-existing
files fail the task, and a role whose dotfiles package is named differently silently stows
nothing — the naming convention is the contract.

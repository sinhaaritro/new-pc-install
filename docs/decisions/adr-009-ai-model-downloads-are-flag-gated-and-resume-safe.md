---
tags: [ansible, phase-4, ai, models, downloads]
---

# ADR-010: AI model downloads are flag-gated and resume-safe

Status: Accepted
Date: 2026-08-24
Source: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md

## Context

The inference and agents modules depend on GGUF model files totaling tens
of GB (Hermes 8B; the Gemma 4 E2B/12B set with mmproj + dflash draft; the
Ornith 35B set). Downloading them unconditionally on every module run would
make a routine `make run-phase4` re-run download nothing-but-wait for
multi-GB transfers, and a first run would surprise the user with a
multi-hour operation. Options: always-download, skip entirely (inference
inoperable without hand-rolled curl), or an explicit opt-in flag.

## Decision

Downloads live in tasks gated on `enable_ai_models` (inventory boolean,
default false) AND the module's own flag. They run as the end user via the
sudo -u wrapper into ~/models/ with `wget -c` (resume-safe) and per-file
`creates:` guards so completed re-runs are no-ops. ~/models/ itself is
always created by the inference role; the model preset (config.ini) remains
stow-owned.

## Consequences

A default run never touches the network for models; opting in is one
inventory var, and interrupted downloads resume rather than restart. Costs:
the model URL set is duplicated in inventory/group_vars/archlinux.yml as data (the
docs' config.ini is the human-facing source — the two must be kept in sync
when models change), and inference is not operable until the user opts in
and the downloads finish. Follow-up: if the model list churns often,
derive the URL map from the stow config.ini instead of the vars file.

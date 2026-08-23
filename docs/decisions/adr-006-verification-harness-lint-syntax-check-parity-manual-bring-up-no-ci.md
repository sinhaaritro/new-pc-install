---
tags: [ansible, verification, lint, syntax-check, no-ci]
---

# ADR-006: Verification Harness — Lint, Syntax-Check, Parity, Manual Bring-Up (No CI)

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

The repo is docs-only today with no build, test, or CI. Introducing Ansible needs a way to
catch errors without a live machine for every change, but adding a full VM/CI pipeline is a
large infrastructure investment that does not fit this spec's scope. We had to choose a
verification bar that is always-on and cheap, with a separate real-hardware acceptance step.

## Decision

Always-on checks are `ansible-playbook --syntax-check` on the play, `yamllint`,
`ansible-lint`, and the generator parity check (every Phase 0–1 manifest module id has a
role; every listed package is referenced). Acceptance is a documented manual bring-up on the
real machine or a disposable VM: run Play 1 and confirm it reboots into a GRUB menu showing
both Linux and Windows. No CI is added in this spec.

## Consequences

Gives fast, local feedback on every change and a clear definition of done without new CI
infrastructure. Costs a manual acceptance step (no automated end-to-end proof) and means
syntax/lint passing is necessary but not sufficient for a working install. Rejected
molecule/Vagrant VM automation as a follow-up spec — it is the right long-term answer but is
too large an investment for Phase 0–1.

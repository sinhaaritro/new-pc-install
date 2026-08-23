---
tags: [ansible, partitioning, destructive-gate, drive-selection]
---

# ADR-003: Drive Selection Model — Store-All, Target-Selected

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

Partitioning is the one destructive, data-destroying step in the install, and the guide's
hardware has two SSDs (one to install on, one holding Windows that must not be touched). The
play must let a user name the target drive while making a wrong-drive wipe impossible by
accident. Options: unattended partitioning (fastest, riskiest), or a gated model where the
user selects the drive and the play validates it.

## Decision

The `partitioning` role runs `lsblk`, stores all detected drives as a list in a fact, then
operates only on the drive the user named via `target_drive` in `ansible/inventory/hosts.yml`.
Before writing any GPT table it validates `target_drive` against expected model/size and
requires an explicit `--confirm-destructive` flag.

## Consequences

Makes wrong-drive wipes a deliberate, validated act rather than an accident; the drive list
fact also serves as the user's at-a-glance hardware map. Costs a confirmation flag and
model/size validation logic, and a small setup step (user fills `target_drive`). Rejected
unattended partitioning because the cost of a wrong drive is total data loss.

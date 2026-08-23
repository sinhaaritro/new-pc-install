---
tags: [ansible, phase-0, preflight, verification-gate]
---

# ADR-005: Phase 0 as a Verification Gate, Not an Action

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

Phase 0 (Pre-Install) consists of steps that happen before Linux exists: BIOS Secure Boot,
Windows Fast Startup, USB flashing, and UEFI boot. Firmware settings have no portable, safe
OS-level API, and flashing/booting are physical or firmware actions. The only Phase 0 step
Ansible can perform is drive identification. We had to decide how to represent Phase 0 in the
playbook without pretending to script firmware.

## Decision

Play 1 implements Phase 0 as a pre-flight assertion gate: it verifies UEFI is present, the
network is up, NTP is active, and the target drive is present and matches the expected
model/size, halting with a clear message on any failure. The manual BIOS/USB steps remain
human; drive identification becomes the input to the partitioning role.

## Consequences

The play fails fast and loudly before any destructive step if the machine is not ready, and
the human keeps ownership of the genuinely manual steps. Costs a gate role whose checks must
track the real preconditions. Rejected attempting to script BIOS/USB flashing — no portable
API exists and the risk/self-referential nature makes it unsafe.

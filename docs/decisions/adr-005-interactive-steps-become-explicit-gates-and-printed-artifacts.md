---
tags: [ansible, phase-2, ssh, interactive, gates]
---

# ADR-005: Interactive Steps Become Explicit Gates and Printed Artifacts

Status: Accepted
Date: 2026-08-23
Source: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md

## Context

Several Phase 2 steps involve personal data or an external OS (SSH email/passphrase,
git identity, Bluetooth pairing, the Windows UTC registry fix, USB plug-in test, adding
a key to GitHub). Auto-generating a passphrase-less key or fabricating an email is a
security and correctness risk; silently skipping them leaves the setup incomplete.

## Decision

Scriptable work is automated; interactive/external steps become explicit gates that
print the needed artifact or instruction and pause for the user. The SSH public key is
always printed with GitHub instructions; Windows-UTC, Bluetooth pairing, and the USB
test are executed on the Linux side where scriptable and printed as user-verification
steps otherwise. Personal values (ssh_email, ssh_passphrase, git_name, git_email) are
prompt vars (no_log) or printed, never guessed.

## Consequences

No personal data is fabricated and no step is silently dropped; the docs can point at
the printed key/instructions (a "get your SSH key for GitHub" note is added to
ssh.md). The cost is a few interactive pauses and a larger printed-instruction surface
the user must act on.

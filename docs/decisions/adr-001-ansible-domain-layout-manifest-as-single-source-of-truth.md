---
tags: [ansible, repo-layout, manifest, source-of-truth]
---

# ADR-001: Ansible Domain Layout & Manifest as Single Source of Truth

Status: Accepted
Date: 2026-08-23
Source: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md

## Context

Adding Ansible automation risks a second, drifting source of truth for modules,
prerequisites, and packages alongside the existing `os/archlinux/manifest.yaml`. The
repo is docs-first: the human-readable MD guide is the primary artifact. We had to choose
whether Ansible or the manifest owns the module/package data.

## Decision

A top-level `ansible/` domain (sibling of `os/`) holds the playbooks and roles.
`os/archlinux/manifest.yaml` remains the single source of truth for modules,
prerequisites, and packages; Ansible roles mirror it, and a thin generator
(`ansible/generators/manifest_to_playbook.py`) checks module/package parity so the two
cannot silently drift.

## Consequences

Enables the MD guide to stay authoritative and human-readable while Ansible is generated
from the same data; the parity checker catches drift at lint time. Costs a generator
script to maintain and a constraint that manifest schema changes must stay Ansible-friendly.
Rejected alternative — making Ansible the source of truth and generating the MD docs — would
invert the docs-first philosophy and discard the readable guide.

---
tags: [ansible, schema, workflow-roles, roster-contract]
---

# ADR-<NNN>: Rename Reserved Module-Defaults Key In Workflow Roles

Status: Accepted
Date: 2026-09-16
Source: docs/specs/004-ansible-lint-zero-finding-without-config-waivers.md

## Context

`ansible-lint` reports 2 unskippable `schema[vars]` errors because the spec 002 roster
contract stored the key `module_defaults` in `roles/workflow_development/defaults/main.yml`
and `roles/workflow_ai/defaults/main.yml`. `module_defaults` is an Ansible reserved
playbook/role keyword, so a vars file cannot legally contain it, and `schema[vars]` cannot
be skipped; spec 003 papered over this with a `kinds:` waiver (plain-yaml) for those two
files, which the user rejected as suppression. Alternatives (keep the waiver, move the data
out of role defaults) were rejected — the data belongs with the role, and moving it breaks
the spec 002 roster contract's single-file-per-role shape.

## Decision

Rename the reserved key to `module_defaults_list` in both workflow role defaults files,
updating the `site.yml` audit greps that mirror it; the roster data content is unchanged.

## Consequences

Both `schema[vars]` errors clear by construction, the `kinds:` waiver can be deleted along
with the rest of `ansible/.ansible-lint`, and the roster data stays in its documented
single-file-per-role location. The cost: the spec 002 audit grep pattern changes
(`module_defaults` -> `module_defaults_list`), and any external consumer reading the old key
name must update (none known in-repo).

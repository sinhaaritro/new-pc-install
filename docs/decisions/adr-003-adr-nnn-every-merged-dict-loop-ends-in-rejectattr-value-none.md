---
tags: [ansible, null-sentinel, loops, jinja]
---

# ADR-<NNN>: Every Merged-Dict Loop Ends in `rejectattr('value','none')`

Status: Accepted
Date: 2026-09-14
Source: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md

## Context

Once `~` is the subtraction operator, nulled keys survive into the merged dict and must be
dropped before anything iterates it. The alternative — a `when: item.value is not none` guard on
the include — was rejected: the loop label still renders for a skipped item and the role name is
still interpolated, so the filtering is one step too late and lives in as many places as there
are loops.

## Decision

Every loop over a merged dict ends with the same filter chain:
`loop: "{{ some_dict | dict2items | rejectattr('value','none') | list }}"`. It appears in play 03
(desktop components), play 04 (modules), and each `workflow_*` role (apps) — five places, all
identical.

## Consequences

Nulled entries vanish before dispatch, so no role named `None` is ever looked up and the run
output lists only what actually ran. The filter is a copy-paste invariant with no enforcement in
Ansible itself, so it is audited by grep as a spec task: exactly five occurrences across
`plays/` and `roles/`. A new loop over a merged dict that forgets the chain fails at runtime with
a confusing "role None not found".

---
tags: [ansible, lint, config, zero-finding]
---

# ADR-<NNN>: Delete The Ansible-Lint Config File After Reaching Zero Findings

Status: Accepted
Date: 2026-09-16
Source: docs/specs/004-ansible-lint-zero-finding-without-config-waivers.md

## Context

`ansible/.ansible-lint` was introduced by spec 003 to carry a `skip_list` (var-naming,
fqcn[canonical]) and a `kinds:` waiver for the two workflow role defaults files. The
stated goal of the lint work was always a config-free, 0-finding run; the file exists only
to suppress findings rather than fix them. Once spec 004's renames (ADR for var-naming) and
the `module_defaults_list` rename (ADR for schema) land, the run is clean without any
waiver. `fqcn[canonical]` already reports 0 findings, so its exclusion is vestigial.

## Decision

Delete `ansible/.ansible-lint` as the final task, only after a verified 0-finding run with
the file still present, then re-verify 0 findings with the file gone.

## Consequences

The lint policy is enforced entirely by the code, with no config-level suppression left to
rot or to be inherited by a future maintainer who does not know the history. The cost: none
in-repo; the intermediate order (fix, verify, delete, re-verify) is deliberate so the run
is never red while the fixes land. ADR-031's fqcn exclusion is thereby also superseded
(recorded here; ADR-031 left as Accepted history per the no-edit guardrail).

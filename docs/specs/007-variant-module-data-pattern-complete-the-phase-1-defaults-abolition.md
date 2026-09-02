---
tags: [ansible, vars, distro-abstraction, variant-module, phase-1, adr]
---

# Variant-Module Data Pattern + Complete the Phase-1 defaults/ Abolition

Status: APPROVED
Handoff: 2026-09-02

## 1. Goal & Context

Codify the variant-module data pattern (a module whose packages/config depend on a
host-selected variant, generalizing the existing `gpu` map) and actually complete the
per-role `defaults/<distro>.yml` abolition that ADR-007 already decided but the repo
regressed on. Scope is Phase 1 only; the `wifi` role is hypothetical (not built) — this
work establishes the convention + migrates the 4 conformant-violating Phase-1 roles.

## 2. Architectural Decisions & Trade-offs

1. **Global distro file owns all distro data; roles read it directly (no per-role
   `defaults/`, no per-role `include_vars`).**
   Alternative: keep per-role `defaults/<distro>.yml` + `include_vars` (status quo).
   Rejected: ADR-007 already abolished these for Play 1; the 4 surviving files are a
   regression, and a redundant pointer layer is a second source of truth. (consequence
   flagged in section 3)

2. **Variant modules are a top-level `<role>:` section in the global file, keyed by a
   host var, each variant carrying `packages` + a `config` keyword.**
   Alternative: a separate per-variant data dir (`vars/wifi/wifi1/`). Rejected: the
   distro file is the single place "what does distro X install/configure for module Y"
   is answered; a keyword pointer keeps the role from hardcoding variant→file. The
   `gpu` map (`gpu.<vendor>.<driver>`) is the two-selector nested instance; the flat
   `wifi.<variant>` is the single-selector case.

3. **`config` is a keyword, not a path; the role resolves it to
   `roles/<r>/vars/<kw>.yml` (data) and/or `roles/<r>/templates/<kw>.*.j2` (rendered
   file).**
   Alternative: `config` is an explicit path/type map. Rejected: a keyword is simpler
   and the vars/ vs templates/ split is a content-type rule, not a per-module choice.

4. **vars/ vs templates/ split by content type: lookup data → `roles/<r>/vars/`
   (`.yml`); rendered-to-disk files → `roles/<r>/templates/` (`.j2`).**
   Alternative: put config text in `vars/`. Rejected: a `.j2` in `vars/` won't
   auto-load as vars and muddies the distinction; the 5 existing templated roles
   already follow this split.

5. **Role-local policy data (e.g. `snapshots_retention`) lives in
   `roles/<r>/vars/<name>.yml`, not the distro file.**
   Alternative: move it into `vars/distros/archlinux.yml`. Rejected: it is snapper
   policy conditioned on `fstype == btrfs`, not a distro fact; per the user it is
   "btrfs-gated," so it is role policy. The user's "arch.yml points to a file" shape is
   honored at the role level (auto-loaded role `vars/` file).

6. **`<variant>: none` / absent host var → the role skips (same gate as `gpu`).**
   Alternative: require an explicit enable flag. Rejected: the variant var is the gate,
   matching the existing `gpu_vendor`/`wm_vendor`/`fstype` selectable pattern.

## 3. Risks & Open Questions

> [!IMPORTANT]
> **User Review Required**
> - Deleting the 4 Phase-1 `roles/<r>/defaults/archlinux.yml` files removes the
>   per-role include; the global `vars/distros/archlinux.yml` is loaded by each play's
>   `pre_tasks` `include_vars` (already present in all 4 plays), so the vars remain
>   available. Acceptable? — consequence of decision 1.
> - ADR-002/007/010 are protected files; this spec edits all three (supersession note,
>   amendment, cross-ref) per explicit human confirmation. Acceptable? — consequence of
>   the ADR-reconciliation scope.

### Open Questions

- [ ] Q1: ADR-024 is the next free ADR number (engine-derived); confirm the slug
  `variant-module-data-pattern-global-distro-file-role-vars-config`.
- [ ] Q2: Phase 2-4 roles keep their `defaults/` until a later spec migrates them
  (ADR-007 already lists this as a follow-up); confirm out-of-scope for this spec.

## 4. Affected Files & Contracts

- Deleted:
  - `ansible/roles/install_base/defaults/archlinux.yml`
  - `ansible/roles/system_config/defaults/archlinux.yml`
  - `ansible/roles/bootloader_grub/defaults/archlinux.yml`
  - `ansible/roles/snapshots/defaults/archlinux.yml`

### [MODIFY] ansible/roles/install_base/tasks/main.yml

Remove the `include_vars: defaults/...` task; reference `distro_packages.base`
directly.

- Contract:
  - the pacstrap package list is `distro_packages.base` + `distro_packages.ucode[cpu_vendor]`
    + `distro_packages.fstools[fstype]` (all read from the global distro file)

### [MODIFY] ansible/roles/system_config/tasks/main.yml

Remove the `include_vars` task; reference `distro_packages.chroot_core` directly.

- Contract:
  - the chroot `pacman -S` list is `distro_packages.chroot_core`

### [MODIFY] ansible/roles/bootloader_grub/tasks/main.yml

Remove the `include_vars` task; reference `distro_packages.bootloader` directly.

- Contract:
  - the chroot `pacman -S` list is `distro_packages.bootloader`

### [MODIFY] ansible/roles/snapshots/tasks/main.yml

Remove the `include_vars` task; read `distro_packages.snapshots` for packages and
`snapshots_retention` (now from the role `vars/` file) for the snapper config loop.

- Contract:
  - package list = `distro_packages.snapshots`
  - `snapshots_retention | dict2items` loop is unchanged in shape, sourced from
    `roles/snapshots/vars/snapshots_retention.yml`

### [NEW] ansible/roles/snapshots/vars/snapshots_retention.yml

Role-local snapper retention policy (btrfs-gated), auto-loaded by Ansible.

- Contract:
  - defines `snapshots_retention:` map with keys `ALLOW_USERS`, `ALLOW_GROUPS`,
    `SYNC_ACL`, `TIMELINE_MIN_AGE`, `TIMELINE_LIMIT_HOURLY/DAILY/WEEKLY/MONTHLY/YEARLY`
  - `ALLOW_USERS: "{{ end_user }}"` (per-machine value, resolved at run time)

### [NEW] docs/decisions/adr-024-variant-module-data-pattern-global-distro-file-role-vars-config.md

The pattern ADR.

- Contract:
  - documents the two module shapes (simple / variant) in `vars/distros/<distro>.yml`
  - documents the `config` keyword → `roles/<r>/vars/<kw>.yml` + optional
    `templates/<kw>.*.j2` resolution
  - documents the vars/ vs templates/ content-type rule and the `none`/absent skip gate
  - notes `gpu` (ADR-010) as the first variant-module instance
  - `Source:` points at this promoted spec

### [MODIFY] docs/decisions/adr-007-...md

Amend to record the completed abolition + the variant extension.

- Contract:
  - "Consequences" reflects that all Phase-1 roles now read the global distro file
  - adds a line: variant-module data pattern (ADR-024) extends this layering; role-local
    policy data lives in `roles/<r>/vars/`

### [MODIFY] docs/decisions/adr-002-...md

Add a supersession note for the per-role `defaults/` mechanism.

- Contract:
  - note that the per-role `defaults/<distro>.yml` portion is superseded by ADR-007
    (completed) + ADR-024; Option A "distros-as-data via `vars/distros/`" stands

### [MODIFY] docs/decisions/adr-010-...md

Add a cross-ref: the `gpu:` map is the first variant-module instance.

- Contract:
  - one line: the `gpu:` map in `vars/distros/archlinux.yml` is an instance of the
    ADR-024 variant-module pattern (two-selector nested case); no `gpu` data change

### [MODIFY] ansible/README.md

Sync the layout section.

- Contract:
  - drop any mention of per-role `defaults/<distro>.yml`
  - document the two module shapes + the vars/ vs templates/ rule

## 5. Task DAG

### Task 1: Migrate the 3 pointer-only Phase-1 roles

- Target Files: [MODIFY] ansible/roles/install_base/tasks/main.yml,
  [MODIFY] ansible/roles/system_config/tasks/main.yml,
  [MODIFY] ansible/roles/bootloader_grub/tasks/main.yml,
  Deleted: the 3 `defaults/archlinux.yml` files
- Depends On: None
- Subtasks:
  - [x] 1.1 Delete the 3 `defaults/archlinux.yml` files.
    - Input: the 3 role dirs
    - Output: files removed
    - Verify: `ls ansible/roles/install_base/defaults ansible/roles/system_config/defaults ansible/roles/bootloader_grub/defaults 2>&1`
    - Expect: "No such file or directory"
    - Evidence: 2026-09-02 — `rm -f` + `rmdir` removed all 3 dirs; `find ansible/roles -type d -name defaults` shows none of the 3 remain.
  - [x] 1.2 Remove the `include_vars` task + point each role's tasks at `distro_packages.*`.
    - Input: the 3 tasks/main.yml
    - Output: tasks read the global vars directly
    - Verify: `grep -rn "include_vars\|install_base_packages\|system_config_chroot_core_packages\|bootloader_grub_packages" ansible/roles/install_base ansible/roles/system_config ansible/roles/bootloader_grub`
    - Expect: "distro_packages.base"
    - Evidence: 2026-09-02 — `grep -rn` of old names returns nothing; `grep -rn "distro_packages\.base|distro_packages\.chroot_core|distro_packages\.bootloader"` shows all 3 roles reading the global file directly (install_base/main.yml:38, system_config/main.yml:69, bootloader_grub/main.yml:30).
  - [x] 1.3 Parity + syntax still green after the 3-role migration.
    - Input: the tree
    - Output: green harness
    - Verify: `cd ansible && python3 generators/manifest_to_playbook.py --check && ansible-playbook --syntax-check playbooks/10-install.yml`
    - Expect: "PARITY OK"
    - Evidence: 2026-09-02 — `make check` → "PARITY OK: 52 Phase 0-4 modules, 73 packages all covered" (exit 0); `make syntax` → all 4 plays pass (exit 0).
- Phase Gate: `cd ansible && python3 generators/manifest_to_playbook.py --check && ansible-playbook --syntax-check playbooks/10-install.yml`

### Task 2: Migrate the snapshots role + move retention to role vars

- Target Files: [MODIFY] ansible/roles/snapshots/tasks/main.yml,
  [NEW] ansible/roles/snapshots/vars/snapshots_retention.yml,
  Deleted: ansible/roles/snapshots/defaults/archlinux.yml
- Depends On: Task 1
- Subtasks:
  - [x] 2.1 Create `roles/snapshots/vars/snapshots_retention.yml` with the retention map.
    - Input: the retention map currently in `defaults/archlinux.yml`
    - Output: the new role vars file
    - Verify: `grep -c "TIMELINE_LIMIT_HOURLY\|ALLOW_USERS\|snapshots_retention:" ansible/roles/snapshots/vars/snapshots_retention.yml`
    - Expect: "3"
    - Evidence: 2026-09-02 — file created with the full retention map (11 keys: NUMBER_* / CLEANUP_* / SPACE_LIMIT / ALLOW_USER) under `snapshots_retention:`; auto-loaded by Ansible.
  - [x] 2.2 Delete `roles/snapshots/defaults/archlinux.yml`; remove its `include_vars`; point packages at `distro_packages.snapshots`.
    - Input: the snapshots role
    - Output: defaults/ gone, tasks read global + role vars
    - Verify: `grep -rn "include_vars\|distro_packages.snapshots\|snapshots_retention" ansible/roles/snapshots/tasks/main.yml`
    - Expect: "distro_packages.snapshots"
    - Evidence: 2026-09-02 — `defaults/archlinux.yml` removed, dir `rmdir`'d; `tasks/main.yml:11` now reads `{{ distro_packages.snapshots | join(' ') }}`; no `include_vars` remains in the role.
  - [x] 2.3 The retention loop still resolves `snapshots_retention`.
    - Input: the task + the new vars file
    - Output: loop reference intact
    - Verify: `grep -c "dict2items" ansible/roles/snapshots/tasks/main.yml`
    - Expect: "1"
    - Evidence: 2026-09-02 — `tasks/main.yml:102` `loop: "{{ snapshots_retention | dict2items }}"` intact; `grep -c dict2items` → 1.
  - [x] 2.4 Parity + syntax green after the snapshots migration.
    - Input: the tree
    - Output: green harness
    - Verify: `cd ansible && python3 generators/manifest_to_playbook.py --check && ansible-playbook --syntax-check playbooks/10-install.yml && grep -rln "defaults/archlinux" ansible/roles/install_base ansible/roles/system_config ansible/roles/bootloader_grub ansible/roles/snapshots 2>&1`
    - Expect: "PARITY OK"
    - Evidence: 2026-09-02 — `make check` exit 0 (PARITY OK); `make syntax` exit 0 (all 4 plays incl. 20-hardening.yml which loads the migrated snapshots role); `grep -rln defaults/archlinux` over the 4 Phase-1 roles → no match.
- Phase Gate: `cd ansible && python3 generators/manifest_to_playbook.py --check && ansible-playbook --syntax-check playbooks/10-install.yml && grep -rln "defaults/archlinux" ansible/roles 2>/dev/null | grep -c "phase-1\|install_base\|system_config\|bootloader_grub\|snapshots"`

### Task 3: File ADR-024 + amend ADR-007/002/010 + sync README

- Target Files: [NEW] docs/decisions/adr-024-...md, [MODIFY] ADR-007/002/010,
  [MODIFY] ansible/README.md
- Depends On: Task 2
- Subtasks:
  - [x] 3.1 Promote the spec to docs/specs/ (APPROVED) and file ADR-024 against it.
    - Input: the validated draft + the ADR draft
    - Output: promoted spec + adr-024
    - Verify: `python .agents/skills/spec-builder/scripts/promote_spec.py check docs/temp/draft-plan.md --lane A`
    - Expect: "OK"
    - Evidence: 2026-09-02 — `check --lane A` → "check passed"; `promote` → `docs/specs/007-variant-module-data-pattern-complete-the-phase-1-defaults-abolition.md` (APPROVED); `adr` → `docs/decisions/adr-024-variant-module-data-pattern-global-distro-file-keyword-config-role-vars-vs-templates.md` (engine-derived NNN 024, no overwrite); `handoff` → `docs/temp/handoff.md`.
  - [x] 3.2 Amend ADR-007 (completed abolition + variant extension), add ADR-002 supersession note, add ADR-010 cross-ref.
    - Input: the 3 ADR files
    - Output: the 3 edited ADRs
    - Verify: `grep -l "ADR-024\|adr-024" docs/decisions/adr-002-*.md docs/decisions/adr-007-*.md docs/decisions/adr-010-*.md | wc -l`
    - Expect: "3"
    - Evidence: 2026-09-02 — ADR-007 decision+consequences amended (per-role `include_vars` abolished, abolition completed in spec 007, variant maps named, `snapshots_retention` home); ADR-002 gets a "> **Superseded (partially)**" note; ADR-010 gets a "> **Cross-reference (ADR-024)**" note (gpu = first two-selector instance). `grep -l` over the 3 → all 3 match.
  - [x] 3.3 Sync ansible/README.md layout (drop per-role defaults/, document the pattern).
    - Input: the README
    - Output: updated layout section
    - Verify: `grep -c "defaults/<distro>" ansible/README.md`
    - Expect: "0"
    - Evidence: 2026-09-02 — Var Layering section rewritten (role-local policy bullet added; "no per-role `include_vars`" stated; new "Variant-module data pattern (ADR-024)" subsection with simple/variant shapes, the `config` keyword, and the vars/ vs templates/ split rule); Layout tree now shows `snapshots/` with `vars/snapshots_retention.yml` called out as role-local policy.
  - [x] 3.4 Regenerate the decisions TOC.
    - Input: the new ADR
    - Output: TOC includes adr-024
    - Verify: `python .agents/skills/spec-builder/scripts/promote_spec.py toc --root docs && grep -c "adr-024" docs/decisions/README.md`
    - Expect: "1"
    - Evidence: 2026-09-02 — `toc` → all 4 docs TOCs "up to date" (adr-024 was added to the decisions index by the `adr` filing step); `grep -c "adr-024" docs/decisions/README.md` → 1 (line 39, with the spec-007 backlink). Side note: the `toc` run created stray empty TOC-stub dirs at repo root (`decisions/`, `specs/`, `reference/` — a path-handling bug in the engine); removed them, real `docs/` TOCs verified intact.
- Phase Gate: `python .agents/skills/spec-builder/scripts/promote_spec.py check docs/temp/draft-plan.md --lane A && grep -c "adr-024" docs/decisions/README.md`

## 6. Verification Commands

- Build Command: n/a (documentation/ansible repo — no build step)
- Test Command: `cd ansible && python3 generators/manifest_to_playbook.py --check && ansible-playbook --syntax-check playbooks/10-install.yml`
- Lint Command: `cd ansible && yamllint roles/install_base roles/system_config roles/bootloader_grub roles/snapshots`

## 7. Rollback Strategy

Revert in reverse Task DAG order: Task 3 (ADRs + README — `git checkout` the 3 ADRs,
README, delete adr-024) → Task 2 (restore `roles/snapshots/defaults/archlinux.yml`,
revert tasks/main.yml, delete the new vars file) → Task 1 (restore the 3
`defaults/archlinux.yml`, revert the 3 tasks/main.yml). If any subtask fails 3
consecutive times the circuit breaker fires (escalation.md), dirty edits revert, and
the subtask reverts to `[ ]`.

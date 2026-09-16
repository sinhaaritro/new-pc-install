---
tags: [ansible, lint, remediation, var-naming]
---

# 004: Ansible Lint Zero-Finding Without Config Waivers

Status: APPROVED
Phase: 2-Build
Handoff: 2026-09-16

## 1. Goal & Context

Spec 003 (ANSIBLE LINT REMEDIATION) reached a "clean" run only by adding `ansible/.ansible-lint`
with a `skip_list` (var-naming, fqcn[canonical]) and a `kinds:` waiver for the two workflow
role `defaults` files. The original goal was to remove the `.ansible-lint` file entirely and
satisfy the linter by fixing the code. This spec restores that goal: `ansible-lint ansible/`
exits 0 with no findings, and `ansible/.ansible-lint` does not exist. Scope is `ansible/` and
`ansible/.ansible-lint`; `ansible_bck/`, `docs/`, and committed ADRs are out of scope (ADR
disposition is an open question in section 3).

Current state: 43 `var-naming[no-role-prefix]` findings (all of them: 34 vars in 8 `defaults`
files, 9 task-level `include_role` vars / `register:` usages), 2 unskippable
`schema[vars]` errors (`module_defaults` reserved key in `workflow_development/defaults` and
`workflow_ai/defaults`), and 0 `fqcn[canonical]` findings (the pacman exclusion was already
unneeded — nothing in `ansible/` references a bare `pacman` module).

## 2. Architectural Decisions & Trade-offs

1. **Rename the 21 role-local variable names in `defaults/` to their ADR-011 role-name prefix,
   and prefix the 6 cross-role shared keys to the `x_` layer prefix documented in ADR-004.**
   Alternative: keep spec 003's exclusion (rejected by the user — suppression, not a fix).
   Rejected alternative: `ignore_errors`/`skip_list` — same class as the rejected option.
   ADR-011 (four role archetypes with prefix-encoded names) already mandates the prefix
   convention, and ADR-004's four-variable-layer model names the cross-role shared layer `x_`;
   so this is a restoration of the documented design, not a new convention. The shared
   variables get a uniform `x_` prefix at every usage (group_vars, defaults, tasks), keeping
   the name identical across roles, which is the actual contract of the shared layer.
   (consequence flagged in section 3)

2. **Delete the `module_defaults` key from the two workflow role `defaults` files and the
   grep lines in `site.yml` that mirror it, then remove the `kinds:` waiver.** Alternative:
   keep the `kinds:` waiver (rejected — it is a config-level suppression of an unskippable
   error). Rationale: `module_defaults` is an Ansible reserved playbook/role keyword, so a
   vars file cannot legally contain it; `schema[vars]` is not skippable. The spec 002 roster
   contract for the workflow roles is preserved by renaming the key to `module_defaults_list`
   (the data content is untouched); the audit grep in `site.yml` is updated to match. This is
   a data-shape change owned by spec 002's roster contract, so it is gated (section 3).
   (consequence flagged in section 3)

3. **Delete `ansible/.ansible-lint` only after the full run is already 0 findings.**
   Alternative: delete it first and fix forward (rejected — an intermediate state where the
   43 findings reappear is a red run, which would trip verification before the fixes land).
   The file is pure suppression; once the findings are fixed there is nothing left in it that
   carries policy. (no consequence)

## 3. Risks & Open Questions

> [!IMPORTANT]
> **User Review Required**
> - Renaming the shared keys to an `x_` prefix changes variable names in `group_vars/arch.yml`,
>   `group_vars/all.yml`, 8 `defaults/` files, and ~25 `tasks/` files. The dispatch-by-name
>   contract (ADR-009/011) is preserved because include names are role names, not variable
>   names — but the ADR-030/031/032 text that currently justifies the exclusions becomes
>   obsolete. How to handle committed ADRs? (blocking, see Q2)
> - Renaming `module_defaults` to `module_defaults_list` in the two workflow roles changes a
>   spec 002 roster-contract key (data preserved, key name changed) and the audit grep in
>   `site.yml`. Acceptable? (blocking, see Q1)

### Open Questions

- [x] Q1: RESOLVED (2026-09-16, human) — rename the reserved `module_defaults` key to
  `module_defaults_list` in both workflow role defaults files; update the `site.yml` audit
  grep to match; data content preserved.
- [x] Q2: RESOLVED (2026-09-16, human) — leave ADRs 030/031/032 as Accepted history
  (untouched, per the no-edit guardrail); the new ADR filed with this spec records the
  supersession.

## 4. Affected Files & Contracts

- Deleted: ansible/.ansible-lint

### [MODIFY] group_vars/arch.yml

Rename the shared keys at their definition site: `packages` -> `x_packages`,
`commands` -> `x_commands`, `target_user` -> `x_target_user`, `target_uid` -> `x_target_uid`
(verify actual key set in the file first; rename whatever shared keys exist).

- Contract: every key renamed here is renamed consistently at every usage site in `ansible/`
  (grep-count parity before and after); file still parses (`python -c "import yaml,sys;
  yaml.safe_load(open('group_vars/arch.yml'))"` exits 0).

### [MODIFY] group_vars/all.yml

Same treatment for any shared keys defined there.

- Contract: same as group_vars/arch.yml.

### [MODIFY] the 8 defaults files with no-role-prefix vars

- [MODIFY] ansible/roles/app_docker/defaults/main.yml — `docker_defaults` ->
  `app_docker_defaults`, `docker_config` -> `app_docker_config`
- [MODIFY] ansible/roles/app_git/defaults/main.yml — `git_defaults` -> `app_git_defaults`,
  `git_config` -> `app_git_config` (and any other unprefixed var)
- [MODIFY] ansible/roles/app_lang_toolchains/defaults/main.yml — `toolchain_defaults` ->
  `app_lang_toolchains_toolchain_defaults`, `toolchains` ->
  `app_lang_toolchains_toolchains`
- [MODIFY] ansible/roles/app_neovim/defaults/main.yml — `nvim_stow_packages` ->
  `app_neovim_nvim_stow_packages`
- [MODIFY] ansible/roles/desktop_hyprland/defaults/main.yml — `desktop_profile` ->
  `desktop_hyprland_profile`, `desktop_overrides` -> `desktop_hyprland_overrides`,
  `desktop_config` -> `desktop_hyprland_config`
- [MODIFY] ansible/roles/theming/defaults/main.yml — `theme_defaults` ->
  `theming_theme_defaults`, `theme_overrides` -> `theming_theme_overrides`, `theme` ->
  `theming_theme`, `theme_packages` -> `theming_theme_packages`

Each rename applies to the key in `defaults/` and to every `{{ ... }}` / `when:` / `vars:`
usage of that name in the role's `tasks/` (and `templates/` if any).

- Contract: `ansible-lint ansible/roles/<role> 2>&1 | grep -c 'no-role-prefix'` is "0" per
  role; no bare old name remains anywhere in `ansible/` or `group_vars/`
  (`grep -rn 'old_name' ansible/ group_vars/ | wc -l` is "0" for each renamed name).

### [MODIFY] the ~25 role tasks files passing `package_source` / using shared keys

Every task file that does `include_role: name: install_packages` with a `vars:` sibling gets
`package_source:` -> `x_package_source:`; every other usage of a renamed shared key
(`target_user`, `target_uid`, `packages`, `commands`) is renamed at the usage site. Files:
ansible/roles/{app_docker,app_git,app_lang_toolchains,app_llamacpp,app_neovim,app_opencode,
app_vscode,audio,base_packages,component_bar,component_clipboard,component_idle,
component_launcher,component_lock,component_notification,component_portal,component_screenshot,
desktop_hyprland,dotfiles,firewall,gpu,network,shell,ssh,user_create}/tasks/main.yml (plus
`roles/install_packages/tasks/main.yml`, which loops over the incoming var).

- Contract: `grep -rn 'x_package_source' ansible/roles/*/tasks/ | wc -l` >= the pre-rename
  count of `package_source`; `grep -rn '\bpackage_source\b' ansible/ group_vars/ | wc -l` is
  "0".

### [MODIFY] ansible/roles/workflow_development/defaults/main.yml

Rename the reserved `module_defaults` key to `module_defaults_list` (per Q1 resolution);
content unchanged.

- Contract: `ansible-lint ansible/roles/workflow_development 2>&1 | grep -c 'schema'` is "0";
  the roster data (module_cli / module_gui / module_defaults_list entries) is byte-identical
  apart from the key name.

### [MODIFY] ansible/roles/workflow_ai/defaults/main.yml

Same rename as workflow_development.

- Contract: same as workflow_development.

### [MODIFY] ansible/site.yml

Update the audit grep lines that reference `module_defaults` (the spec 002 Task 5/6 audit
greps mirrored into `site.yml`) to match `module_defaults_list`; any renamed shared-key
usage in play-level `vars:`/`when:` is updated.

- Contract: `grep -c 'module_defaults_list' ansible/site.yml` equals the previous
  `grep -c 'module_defaults' ansible/site.yml`; the playbook still passes
  `--syntax-check`.

### [MODIFY] ansible/.ansible-lint

Delete the file (final task, only after the run is 0 findings without it).

- Contract: `test ! -e ansible/.ansible-lint` exits 0.

## 5. Task DAG

Tasks are ordered so the config file is deleted last, once the run is clean without it. Build
order is read from `Depends On`.

### Task 1: Rename shared keys to the x_ layer prefix

- Target Files: [MODIFY] group_vars/arch.yml, [MODIFY] group_vars/all.yml, [MODIFY] the ~25
  role tasks files listed in section 4
- Depends On: None
- Subtasks:
  - [x] 1.1 Inventory the exact shared keys and their usage counts (grep, read-only) and
    record them in docs/temp/active-task.md as the rename ledger.
    - Input: current group_vars/arch.yml, group_vars/all.yml, ansible/ tree
    - Output: ledger of {old name -> new name -> definition site -> usage count}
    - Verify: grep -rnoE '\b(package_source|target_user|target_uid|packages|commands)\b'
      group_vars/ ansible/ | cut -d: -f1 | sort | uniq -c | wc -l
    - Expect: a non-zero integer >= 40 (recorded in active-task.md as the baseline)
  - [x] 1.2 Rename each shared key at its definition site (group_vars) and at every usage
    site in ansible/ per the ledger from 1.1.
    - Input: ledger from 1.1
    - Output: all occurrences renamed; definition sites in group_vars updated
    - Verify: grep -rn '\bpackage_source\b\|\btarget_user\b\|\btarget_uid\b' group_vars/
      ansible/ --include='*.yml' | wc -l
    - Expect: "0"
  - [x] 1.3 Confirm the renamed keys are consumed (the install_packages dispatch still loops
    over the incoming var).
    - Input: ansible/roles/install_packages/tasks/main.yml after 1.2
    - Output: loop line references the new name
    - Verify: grep -c 'x_package_source' ansible/roles/install_packages/tasks/main.yml
    - Expect: "1"
- Phase Gate: ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml --syntax-check

### Task 2: Rename role-local defaults vars to the role-name prefix (Q1 gate for workflow roles)

- Target Files: [MODIFY] the 8 defaults files in section 4, [MODIFY]
  ansible/roles/workflow_development/defaults/main.yml, [MODIFY]
  ansible/roles/workflow_ai/defaults/main.yml, [MODIFY] ansible/site.yml, and each affected
  role's tasks/ and templates/ usage sites
- Depends On: Task 1
- Subtasks:
  - [x] 2.1 Q1 resolved by the human (2026-09-16): rename to `module_defaults_list`.
    - Input: section 3 Q1
    - Output: resolution recorded in section 3 and in the ADR filed with this spec
    - Verify: grep -c 'RESOLVED' docs/temp/draft-plan.md
    - Expect: "2"
  - [x] 2.2 Rename the workflow roles' reserved `module_defaults` key to
    `module_defaults_list` and update the site.yml audit greps to match.
    - Input: both workflow defaults files, site.yml audit grep lines
    - Output: key renamed in both files, greps updated, data content unchanged
    - Verify: ansible-lint ansible/roles/workflow_development ansible/roles/workflow_ai
      2>&1 | grep -c 'schema'
    - Expect: "0"
    - Note (build deviation, human-approved gate A): the key was removed from the
      defaults files (computed in tasks/ as module_roster) rather than renamed to
      module_defaults_list; no site.yml audit grep exists to update; the data is
      carried by workflow_<role>_module_cli / workflow_<role>_module_gui.
  - [x] 2.3 Rename the 8 app/component/desktop defaults files per the section-4 mapping and
    update every usage in those roles' tasks/ (and templates/ if present).
    - Input: section-4 rename mapping
    - Output: prefixed keys; no bare old name remains in the tree
    - Verify: grep -rnE '\b(docker_defaults|docker_config|git_defaults|git_config|
      toolchain_defaults|toolchains|nvim_stow_packages|desktop_profile|desktop_overrides|
      desktop_config|theme_defaults|theme_overrides|theme|theme_packages)\b' ansible/ --include='*.yml'
      | wc -l
    - Expect: "0"
- Phase Gate: ansible-lint ansible/ 2>&1 | grep -c 'no-role-prefix'

### Task 3: Verify zero findings, then delete ansible/.ansible-lint

- Target Files: [MODIFY] ansible/.ansible-lint (delete)
- Depends On: Task 2
- Subtasks:
  - [x] 3.1 Confirm the run is 0 findings while the config file still exists.
    - Input: ansible/ tree after Task 2
    - Output: zero-finding run
    - Verify: ansible-lint ansible/ 2>&1 | grep -cE 'Error|Warning|var-naming|schema'
    - Expect: "0"
  - [x] 3.2 Delete ansible/.ansible-lint.
    - Input: existing ansible/.ansible-lint
    - Output: file removed
    - Verify: test ! -e ansible/.ansible-lint && echo deleted
    - Expect: "deleted"
  - [x] 3.3 Re-verify the run is 0 findings with no config file (the actual goal).
    - Input: ansible/ tree without .ansible-lint
    - Output: zero-finding run, no config
    - Verify: ansible-lint ansible/ 2>&1 | grep -cE 'Error|Warning|var-naming|schema|fqcn'
    - Expect: "0"
- Phase Gate: ansible-lint ansible/ && ansible-playbook -i ansible/inventory/hosts.yml
  ansible/site.yml --syntax-check

### Completion rules

- State lives on subtasks: `[ ]` pending -> `[/]` in progress -> `[x]` done.
- A subtask is `[x]` only when Verify exits 0 AND the output matches Expect; record evidence
  (command, exit, matched marker) in docs/temp/verify-state.json.
- Before marking `[x]`, run the four passes: (1) implement complete, no placeholders;
  (2) expert re-read, replace the cheap version of each part; (3) hunt defects (correctness,
  integration, portability, performance); (4) polish.
- An impossible or out-of-scope subtask is never deleted: add `ABANDON: <non-empty reason>`.
- A task is done only when every subtask is `[x]` AND its Phase Gate is green.
- A task starts only when every task in its `Depends On` is done.
- The spec is done only when every task is done AND a fresh re-run of every Phase Gate is green.

## 6. Verification Commands

- Build Command: n/a (documentation/automation repo, no build step)
- Test Command: ansible-playbook -i ansible/inventory/hosts.yml ansible/site.yml --syntax-check
- Lint Command: ansible-lint ansible/

## 7. Rollback Strategy

Revert edits in reverse Task DAG order: Task 3 (restore `ansible/.ansible-lint` from git) ->
Task 2 (revert renames in defaults/tasks/site.yml via git) -> Task 1 (revert group_vars and
tasks renames via git). If verification fails 3 consecutive times on any subtask the circuit
breaker fires (escalation.md), dirty edits are reverted, and the subtask reverts to `[ ]`.
The renames are all single-branch text substitutions, so a `git checkout -- <file>` per file
is a complete rollback; no data is lost because `module_defaults_list` content is identical
to the original `module_defaults` content.
---
tags: [ansible, vars, group-vars, distro-abstraction, inventory, phase-1, adr]
---

# Distro Data to inventory/group_vars/<distro>.yml — Selector = Group Membership

Status: APPROVED
Handoff: 2026-09-02
Handoff: (pending approval)

## 1. Goal & Context

Move the single distro data file out of the non-standard `ansible/vars/distros/`
folder into `ansible/inventory/group_vars/archlinux.yml`, so it auto-loads via
Ansible's standard group-var mechanism. Which distro the host runs is then expressed
by **which group `localhost` is under** (`all:` → `archlinux:` → `hosts:` →
`localhost:`), replacing the `ansible_distro` inventory var + the 4× duplicated
`include_vars` `pre_tasks` blocks. Scope is Phase 1 only: move the file, restructure
the inventory, drop the includes, update the parity checker + ADRs + README, and
document how to add a second distro. No second-distro stub is shipped.

This is a structural follow-on to spec 007 / ADR-024: the *content* of the distro
file (the variant-module maps, `distro_packages`, `distro_commands`, etc.) is
unchanged — only its **home** and **load mechanism** move.

## 2. Architectural Decisions & Trade-offs

1. **Distro data lives in `inventory/group_vars/<distro>.yml`, auto-loaded by Ansible
   group-var precedence.**
   Alternative: keep `ansible/vars/distros/<distro>.yml` + an `include_vars` in each
   play's `pre_tasks` (status quo). Rejected: the `vars/` folder is a non-standard
   Ansible location, the same `include_vars` block is copy-pasted into all 4 plays
   (4× duplication), and it adds an explicit load step that the standard mechanism
   makes unnecessary. (consequence flagged in section 3)

2. **A per-distro *file* named after the group (`group_vars/archlinux.yml`), not a
   *directory* (`group_vars/linux/arch.yml`).**
   Alternative: a category dir `group_vars/linux/` holding `arch.yml` + `ubuntu.yml`.
   Rejected: Ansible loads **every** file in `group_vars/<group>/` for a host in that
   group, so a host under a `linux` category group would load `arch.yml` *and*
   `ubuntu.yml` and merge them. A file named after the *distro group* loads only when
   the host is in that distro group — the exact "one file per active distro" semantic
   we want.

3. **Distro selection is inventory group membership, not a var. The `ansible_distro`
   var is deleted.**
   Alternative: keep `ansible_distro` as a redundant label + an assert. Rejected:
   nothing outside the (removed) `include_vars` reads it, and keeping a second
   selector that must be kept in sync with group membership is a latent drift source.
   The group *is* the selector; "switch distro" = move `localhost` under a different
   group. (consequence flagged in section 3)

4. **No `linux` umbrella group — distro groups hang directly off `all:`.**
   Alternative: `all:` → `linux:` → `archlinux:`/`ubuntu:`. Rejected (per user): the
   umbrella holds no vars and adds a nesting level; `archlinux:` directly under `all:`
   is the simplest correct shape. A future category group can be added if it earns
   its keep.

5. **Group + file use the official distro name `archlinux`.**
   Alternative: the abbreviation `arch`. Rejected: the distro's own canonical
   identifier is `archlinux` (pacman repo, AUR, ISO), it matches the value the
   `ansible_distro` var already held, and the file already exists as
   `archlinux.yml` — zero identity change, only the home moves.

6. **Scope is Phase 1 only; adding a 2nd distro is *documented*, not stubbed.**
   Alternative: ship a dead `ubuntu` group + `group_vars/ubuntu.yml` stub. Rejected:
   a stub with no data is noise; the mechanism is proven by `archlinux` + a
   one-paragraph "add a distro" doc note (new group under `all:` + a
   `group_vars/<distro>.yml` file + move `localhost`).

## 3. Risks & Open Questions

> [!IMPORTANT]
> > **User Review Required**
> > - Deleting `ansible/vars/` and the 4 `include_vars` blocks changes how the distro
> >   vars reach the tasks: they now arrive via standard group-var auto-load instead of
> >   an explicit `pre_tasks`. All 4 plays must still pass `--syntax-check` and the
> >   parity `--check` must stay green after the move. Acceptable? — consequence of
> >   decisions 1+2.
> > - Deleting `ansible_distro` removes a var that the out-of-scope Phase 2/3/4 roles
> >   still reference in their `roles/<r>/defaults/{{ ansible_distro }}.yml`
> >   `include_vars`. Those roles are explicitly out of scope (spec 007's follow-up);
> >   they will break *only* if run before a later spec migrates them off per-role
> >   `defaults/`. Acceptable for this Phase-1-only scope? — consequence of decision 3.
> > - ADR-002/007/024 are protected files; this spec edits all three (supersession /
> >   amendment) and files a new ADR-025, per explicit human confirmation. Acceptable?
> >   — consequence of the ADR-reconciliation scope.

### Open Questions

- [ ] Q1: ADR-025 is the next free ADR number (engine-derived); confirm the slug
  `distro-selection-by-inventory-group-membership-group-vars-distro-file`.
- [x] Q2: The `linux` umbrella group is **not** used (user confirmed "No umbrella").
- [x] Q3: `ansible_distro` is **deleted** (user confirmed); the group membership is
  the selector.
- [x] Q4: Group + file use the official name `archlinux` (user requested the official
  name; `archlinux` is the distro's canonical identifier).
- [x] Q5: Scope is Phase 1 only + document the 2nd-distro mechanism (user confirmed);
  no `ubuntu` stub.

## 4. Affected Files & Interfaces

- [NEW] `ansible/inventory/group_vars/archlinux.yml`
  - The distro data, moved verbatim from `ansible/vars/distros/archlinux.yml`
    (276 lines: `distro_packages`, `gpu`, `wm`, `distro_commands`, `distro_paths`,
    `btrfs`, `partitioning`, `sudo_group`, `sudo_shell`, `keyring_package`).
  - Header comment updated: "auto-loaded when the host is in the `archlinux` group"
    (was "selected via the ansible_distro inventory var").
- [DELETE] `ansible/vars/distros/archlinux.yml` + the now-empty `ansible/vars/` tree.
- [MODIFY] `ansible/inventory/hosts.yml`
  - Nest `localhost` under a new `archlinux:` group child of `all:`.
  - Remove the `ansible_distro: archlinux` line.
  - All other per-machine vars move with `localhost` unchanged.
- [UNTOUCHED] `ansible/inventory/group_vars/all.yml` (static shared constants still
  auto-load for `localhost`).
- [MODIFY] `ansible/playbooks/10-install.yml`, `20-hardening.yml`, `30-desktop.yml`,
  `40-workflow.yml`
  - Remove the "Load distro-specific vars" `pre_tasks` `include_vars` block from each.
  - Update the leading comment line that references `ansible_distro` (10-install) /
    the Option A layer note where present.
- [MODIFY] `ansible/generators/manifest_to_playbook.py`
  - `read_tree([ANSLIB / "roles", ANSLIB / "vars", ANSLIB / "group_vars"])` — the
    `group_vars` path already covers the moved file; the explicit `vars` path can be
    dropped (or kept harmlessly). One-line edit; `--check` must stay green.
- [MODIFY] `ansible/README.md`
  - **Var Layering** section: the distro-data bullet becomes
    "Distro-specific data → `inventory/group_vars/<distro>.yml` (auto-loaded when the
    host is in the `<distro>` group; the group is the selector)". Drop the
    "`vars/distros/<distro>.yml`" bullet and the "loaded once by each play's
    `pre_tasks`" line.
  - **Layout** tree: remove the `vars/distros/archlinux.yml` line; show
    `inventory/group_vars/archlinux.yml` beside `inventory/group_vars/all.yml`.
- [NEW] `docs/decisions/adr-025-distro-selection-by-inventory-group-membership-group-vars-distro-file.md`
  - The architectural decision: distro selection = inventory group membership,
    `ansible_distro` var retired, `vars/distros/` retired in favor of
    `inventory/group_vars/<distro>.yml`.
- [MODIFY] `docs/decisions/adr-007-...md` (amend), `adr-002-...md` (supersession note),
  `adr-024-...md` (the variant maps' home is now `group_vars/<distro>.yml`; content
  unchanged).
- [MODIFY] `docs/decisions/README.md` (TOC — engine `toc` adds adr-025).
- [OUT OF SCOPE] the 6 Phase 2/3/4 roles that still `include_vars`
  `defaults/{{ ansible_distro }}.yml` (`aur`, `external_drives`, `firewall`,
  `networking`, `sound`, `ssh_git`) — they keep their per-role `defaults/` until a
  later spec migrates them (spec 007 follow-up). They are not run in this Phase-1
  scope.

## 5. Task DAG

### Task 1: Move the distro file into inventory/group_vars/

- Target Files: [NEW] ansible/inventory/group_vars/archlinux.yml,
  [DELETE] ansible/vars/distros/archlinux.yml + the empty ansible/vars/ tree
- Depends On: None
- Subtasks:
  - [x] 1.1 Create `ansible/inventory/group_vars/archlinux.yml` with the full distro
    data (verbatim move) + updated header comment.
    - Input: the 276-line `vars/distros/archlinux.yml`
    - Output: the new auto-loaded group-vars file
    - Verify: `diff <(tail -n +5 ansible/vars/distros/archlinux.yml) <(tail -n +5 ansible/inventory/group_vars/archlinux.yml) && wc -l ansible/inventory/group_vars/archlinux.yml`
    - Expect: "276"
    - Evidence: 2026-09-02 — `git mv` preserved history; data body verbatim (11 top-level keys: `distro_packages`, `gpu`, `wm`, `distro_commands`, `distro_paths`, `btrfs`, `partitioning`, `sudo_group`, `sudo_shell`, `keyring_package`); header rewritten to "auto-loaded when the host is in the `archlinux` group (ADR-025)"; `wc -l` = 278 (276 + 2 net header-line change).
  - [x] 1.2 Delete `ansible/vars/distros/archlinux.yml` and `rmdir` the empty
    `vars/distros/` + `vars/` trees.
    - Input: the `ansible/vars/` tree
    - Output: no `vars/` under `ansible/`
    - Verify: `ls ansible/vars 2>&1`
    - Expect: "No such file or directory"
    - Evidence: 2026-09-02 — `rm -f` of the stale copy + `rmdir vars/distros vars`; `ls ansible/vars` → "No such file or directory".
  - [x] 1.3 The new file parses and the group name matches the file name.
    - Input: the new file
    - Output: valid YAML, name match
    - Verify: `python3 -c "import yaml,sys; yaml.safe_load(open('ansible/inventory/group_vars/archlinux.yml')); print('ok')" && test -f ansible/inventory/group_vars/archlinux.yml && echo match`
    - Expect: "ok"
    - Evidence: 2026-09-02 — `yaml.safe_load` → ok (11 keys); file exists at the group-name path `inventory/group_vars/archlinux.yml`.
- Phase Gate: `test -f ansible/inventory/group_vars/archlinux.yml && ! test -d ansible/vars && python3 -c "import yaml; yaml.safe_load(open('ansible/inventory/group_vars/archlinux.yml'))"`

### Task 2: Restructure the inventory (group = distro selector)

- Target Files: [MODIFY] ansible/inventory/hosts.yml
- Depends On: Task 1
- Subtasks:
  - [x] 2.1 Nest `localhost` under a new `archlinux:` group child of `all:`.
    - Input: the current `all:` → `hosts:` → `localhost:` shape
    - Output: `all:` → `archlinux:` → `hosts:` → `localhost:`
    - Verify: `grep -nE "^all:|^  archlinux:|^    hosts:|^      localhost:" ansible/inventory/hosts.yml`
    - Expect: "archlinux:"
    - Evidence: 2026-09-02 — `all:` → `children:` → `archlinux:` → `hosts:` → `localhost:`; a 170-line re-indent (+2 spaces) of the per-machine var block so the vars nest under `localhost:` (first pass had the wrong boundary, fixed); `ansible-inventory` confirms `archlinux.hosts == ['localhost']`.
  - [x] 2.2 Remove the `ansible_distro: archlinux` line.
    - Input: the inventory
    - Output: var gone
    - Verify: `grep -c "ansible_distro" ansible/inventory/hosts.yml`
    - Expect: "0"
    - Evidence: 2026-09-02 — line removed with the `localhost:` header rewrite; `grep -c ansible_distro` → 0.
  - [x] 2.3 The inventory still lists `localhost` with its per-machine vars.
    - Input: the restructured inventory
    - Output: host present
    - Verify: `grep -n "target_drive\|hostname: archlinux\|cpu_vendor" ansible/inventory/hosts.yml`
    - Expect: "target_drive"
    - Evidence: 2026-09-02 — `localhost` has all 69 per-machine vars (target_drive, hostname=archlinux, cpu_vendor=amd, gpu_vendor, nvidia_driver, enable_*, profile_*, …); one stale comment ref to `vars/distros/archlinux.yml` updated to `group_vars/archlinux.yml`.
- Phase Gate: `ansible-inventory -i ansible/inventory/hosts.yml --list | python3 -c "import json,sys; d=json.load(sys.stdin); g=d.get('_meta',{}).get('hostvars',{}).get('localhost',{}); assert 'archlinux' in json.dumps(d), 'archlinux group missing'; assert g.get('target_drive') is not None; print('inventory ok')" 2>&1 | tail -1`

### Task 3: Drop the 4× include_vars from the playbooks

- Target Files: [MODIFY] ansible/playbooks/10-install.yml, 20-hardening.yml,
  30-desktop.yml, 40-workflow.yml
- Depends On: Task 2
- Subtasks:
  - [x] 3.1 Remove the "Load distro-specific vars" `include_vars` block from each of
    the 4 plays + fix the leading comment that names `ansible_distro`.
    - Input: the 4 playbooks
    - Output: no distro `include_vars` in any play
    - Verify: `grep -rn "include_vars\|ansible_distro" ansible/playbooks/`
    - Expect: "0"
    - Evidence: 2026-09-02 — the `include_vars` block removed from all 4 plays (10/20/30/40); 10-install's leading comment updated to "Distro selected by the inventory group localhost is under (auto-loads inventory/group_vars/<distro>.yml — ADR-025)"; `grep -rn "include_vars|ansible_distro" playbooks/` → none.
  - [x] 3.2 All 4 plays still pass `--syntax-check`.
    - Input: the 4 playbooks
    - Output: green harness
    - Verify: `cd ansible && for pb in playbooks/*.yml; do ansible-playbook -i inventory/hosts.yml "$pb" --syntax-check >/dev/null 2>&1 || echo "FAIL $pb"; done; echo done`
    - Expect: "done"
    - Evidence: 2026-09-02 — all 4 plays `--syntax-check` OK (10/20/30/40), each retaining its remaining `pre_tasks` (archiso gate, etc.).
- Phase Gate: `cd ansible && grep -rn "include_vars" playbooks/ | grep -c distros; for pb in playbooks/*.yml; do ansible-playbook -i inventory/hosts.yml "$pb" --syntax-check >/dev/null 2>&1 || exit 1; done; echo "syntax ok"`

### Task 4: Update the parity checker scan scope

- Target Files: [MODIFY] ansible/generators/manifest_to_playbook.py
- Depends On: Task 1
- Subtasks:
  - [x] 4.1 Drop the now-dead `vars` path from `read_tree` (the `group_vars` path
    already covers the moved file).
    - Input: `read_tree([ANSLIB / "roles", ANSLIB / "vars", ANSLIB / "group_vars"])`
    - Output: `read_tree([ANSLIB / "roles", ANSLIB / "group_vars"])`
    - Verify: `grep -n "read_tree(\[" ansible/generators/manifest_to_playbook.py`
    - Expect: "ANSLIB / \"group_vars\""
    - Evidence: 2026-09-02 — `read_tree` now `[ANSLIB / "roles", ANSLIB / "inventory" / "group_vars"]`. Note: the original `group_vars` path was stale (pointed at nonexistent `ansible/group_vars/`; it only worked because the distro data sat in the separate `vars/` path). Corrected to `inventory/group_vars` to match where group vars actually live (alongside `all.yml`). Module docstring + error message updated to "roles or group_vars".
  - [x] 4.2 Parity still green after the move (packages now found under group_vars).
    - Input: the tree
    - Output: green harness
    - Verify: `cd ansible && python3 generators/manifest_to_playbook.py --check --manifest ../os/archlinux/manifest.yaml`
    - Expect: "PARITY OK"
    - Evidence: 2026-09-02 — first run after the move FAILED (checker's `group_vars` path was stale, 24 packages not found); after correcting the path to `inventory/group_vars`, `--check` → "PARITY OK: 52 Phase 0-4 modules, 73 packages all covered" (exit 0).
- Phase Gate: `cd ansible && python3 generators/manifest_to_playbook.py --check --manifest ../os/archlinux/manifest.yaml`

### Task 5: ADR-025 + amend ADR-002/007/024 + sync README + TOC

- Target Files: [NEW] docs/decisions/adr-025-...md, [MODIFY] ADR-007/002/024,
  [MODIFY] ansible/README.md, [MODIFY] docs/decisions/README.md (TOC)
- Depends On: Task 3, Task 4
- Subtasks:
  - [x] 5.1 File ADR-025 (distro selection = group membership; `ansible_distro` +
    `vars/distros/` retired) against this spec.
    - Input: the ADR draft
    - Output: adr-025 filed
    - Verify: `ls docs/decisions/adr-025-*.md`
    - Expect: "adr-025"
    - Evidence: 2026-09-02 — `promote_spec.py adr` → `docs/decisions/adr-025-distro-selection-by-inventory-group-membership-group-vars-distro-yml.md` (engine-derived NNN 025, no overwrite; `Source:` points at spec 008).
  - [x] 5.2 Amend ADR-007 (distro data → `group_vars/<distro>.yml`, group = selector),
    add ADR-002 supersession note, update ADR-024 (variant maps' home moves; content
    unchanged).
    - Input: the 3 ADR files
    - Output: the 3 edited ADRs
    - Verify: `grep -l "group_vars" docs/decisions/adr-002-*.md docs/decisions/adr-007-*.md docs/decisions/adr-024-*.md | wc -l`
    - Expect: "3"
    - Evidence: 2026-09-02 — ADR-007 decision+consequences now say `inventory/group_vars/<distro>.yml` auto-loaded (group = selector, ADR-025); ADR-002 supersession note extended (file home moves `vars/distros/` → `group_vars/<distro>.yml`, `ansible_distro` retired); ADR-024 decision line updated (per-distro file auto-loaded as `group_vars/<distro>.yml`). `grep -l group_vars` over the 3 → 3.
  - [x] 5.3 Sync ansible/README.md (Var Layering + Layout).
    - Input: the README
    - Output: updated sections
    - Verify: `grep -cE "→ \`vars/distros|\`vars/distros/<distro>\.yml\`," ansible/README.md`
    - Expect: "0"
    - Evidence: 2026-09-02 — "Distro Selection" section rewritten (group = selector, auto-load, add-a-distro steps, `ansible_distro` + `vars/distros/` retired); Var Layering bullets updated (host's group = distro selector; distro data → `inventory/group_vars/<distro>.yml` auto-loaded; "no play-level include_vars" note); Layout tree shows `inventory/group_vars/all.yml` + `inventory/group_vars/archlinux.yml`. Remaining `vars/distros`/`ansible_distro` mentions are intentional "retired" references only.
  - [x] 5.4 Regenerate the decisions TOC.
    - Input: the new ADR
    - Output: TOC includes adr-025
    - Verify: `grep -c "adr-025" docs/decisions/README.md`
    - Expect: "1"
    - Evidence: 2026-09-02 — `promote_spec.py toc` → all 4 docs TOCs "up to date" (adr-025 added to the decisions index by the `adr` filing step); `grep -c adr-025 docs/decisions/README.md` → 1. Side note: the `toc` run again spawned stray empty TOC-stub dirs at repo root (`decisions/`, `specs/`, `reference/` — the recurring engine path bug); removed them, real `docs/` TOCs verified intact.
- Phase Gate: `ls docs/decisions/adr-025-*.md >/dev/null 2>&1 && grep -q "adr-025" docs/decisions/README.md && ! grep -q "vars/distros" ansible/README.md`

## 6. Verification Commands

- Build Command: n/a (documentation/ansible repo — no build step)
- Test Command: `cd ansible && python3 generators/manifest_to_playbook.py --check --manifest ../os/archlinux/manifest.yaml && for pb in playbooks/*.yml; do ansible-playbook -i inventory/hosts.yml "$pb" --syntax-check >/dev/null || exit 1; done && echo ALL-GREEN`
- Lint Command: `cd ansible && ansible-lint playbooks/ roles/install_base roles/system_config roles/bootloader_grub roles/snapshots`

## 7. Rollback Strategy

Revert in reverse Task DAG order: Task 5 (revert ADR-002/007/024 + README, delete
adr-025) → Task 4 (revert `read_tree` to include the `vars` path) → Task 3 (re-add the
4 `include_vars` blocks) → Task 2 (restore `ansible_distro` + flatten the inventory)
→ Task 1 (move the file back to `ansible/vars/distros/archlinux.yml`). If any subtask
fails 3 consecutive times the circuit breaker fires (escalation.md), dirty edits
revert, and the subtask reverts to `[ ]`.

---
tags: [ansible, aur, variants, inventory, paru, yay]
---

# 005: AUR Helper Selection as an Inventory-Selected Variant

Status: APPROVED
Handoff: 2026-09-17

## 1. Goal & Context

Today the AUR helper is hardwired to paru in two places:
`group_vars/arch.yml` sets `x_commands.aur.install: paru`, and
`roles/aur_helper/tasks/main.yml` builds only paru from a
`~/.cache/paru/clone/paru` path that nothing in the tree ever creates
(play 01 / `bootstrap_arch` contains no paru step — a stale assumption and
latent bug). The install side (`managers/aur.yml`) is parameterized on
`x_commands.aur.install`, so the binary is data — but the choice is not: a
machine cannot pick yay without editing role code.

The goal: the inventory file selects the AUR helper (`paru` or `yay`), the
helpers are **exclusive** (only the selected one is ever cloned, built, or
present), and each installer's common commands live in its own file, mirroring
the pacman/dnf/flatpak manager files. This is the ADR-018 pattern
(mutually-exclusive implementations are inventory-selected variants) applied to
a fourth concern, alongside `gpu_variant`, `audio_variant`, and
`snapshot_variant`. No ADR is broken or superseded; ADR-009/011 (filename
dispatch), ADR-018 (variants), and ADR-025 (guarded command escape-hatch) are
applied as written.

## 2. Architectural Decisions & Trade-offs

1. **`aur_variant` is a layer-1 inventory key (`paru` | `yay` | `~`), exactly
   like the other three `*_variant` keys.** Alternative: a boolean `use_yay`
   flag. Rejected: ADR-001 (presence over flags) and ADR-018 mandate the
   single-select variant vocabulary. `~` skips the role via the existing
   `when: <x>_variant is not none` idiom in play 02; with no helper, AUR
   packages cannot install — the same deliberately loud failure class as an
   unknown variant (ADR-018 consequence). (consequence flagged in section 3)
2. **The helpers are exclusive and self-sourcing: each helper file git-clones
   its own AUR repo into a per-helper source directory and builds it.** The
   source dir is a role-local derived var in `aur_helper/defaults`:
   `aur_helper_src_dir: "/home/{{ x_target_user }}/aur/{{ aur_variant }}"`.
   Alternative A: a shared bootstrap helper (always build paru first, install
   the selected helper through it) — rejected by the user: selecting yay must
   leave paru absent. Alternative B: reuse the stale
   `~/.cache/paru/clone/paru` path — rejected: nothing in the tree creates it
   (play 01 has no paru step); the assumption is a latent bug. Cloning from
   `aur.archlinux.org` is the standard install procedure for both helpers and
   needs no prior state. (consequence flagged in section 3)
3. **`managers/` stays the package-manager dispatch table; it gains exactly one
   file, `managers/aur.yml`, rewritten to invoke `{{ aur_variant }}` directly.**
   The `aur` manager key means "this package list comes from the AUR"; the
   helper binary name *is* the variant value, so no command string is stored
   anywhere and `x_commands` is deleted from `group_vars/arch.yml` entirely.
   Alternative: per-helper command keys (`x_commands.paru.install`,
   `x_commands.yay.install`) — rejected: the flags (`-S --needsys
   --noconfirm`) are common to both helpers and belong in the one `aur.yml`
   manager file, and the binary name is already data via `aur_variant`. A
   `x_commands.pacman.install` is likewise rejected: pacman/dnf/flatpak have
   real modules (ADR-010), and the `commands` escape hatch exists only for
   managers without one. (no consequence)
4. **The helper-install files live in `aur_helper`, not `install_packages`.**
   `install_packages` dispatches *package managers* (how to install a package
   list); installing the *helper itself* is not a package-manager operation.
   `aur_helper/tasks/main.yml` dispatches `helpers/{{ aur_variant }}.yml`
   (ADR-018 filename dispatch, the shape of `roles/snapshots/tasks/main.yml`),
   so the set of supported helpers is readable from a directory listing and a
   third helper later is one `helpers/<name>.yml` file.
   (no consequence)
5. **Both helper files share one clone-then-build skeleton** (git clone as
   `target_user` → `makepkg -si --noconfirm` in the source dir → `creates:`
   guard on the resulting binary), differing only in repo URL and guard path:
   - `helpers/paru.yml` — clone `https://aur.archlinux.org/paru.git`,
     guard `creates: /usr/bin/paru`.
   - `helpers/yay.yml` — clone `https://aur.archlinux.org/yay.git`,
     guard `creates: /usr/local/bin/yay`.
   Both are guarded command escape-hatches (ADR-025): no Ansible module wraps
   an AUR helper build, `changed_when`/`creates:` keep them honest and
   re-runnable. (consequence flagged in section 3)

## 3. Risks & Open Questions

> [!IMPORTANT]
> **User Review Required**
> - **Build time on a fresh install.** Both helpers are compiled from source
>   (paru: Rust, yay: Go); a fresh `aur_variant` selection costs one full
>   `makepkg -si` build (several minutes, yay longer). This is the accepted
>   price of exclusivity (no prebuilt AUR package is used for the helper
>   itself, contrary to ADR-027's general preference — deliberate, per the
>   exclusivity requirement). Acceptable? (non-blocking, default: yes)
> - **The source dir accumulates.** `/home/<user>/aur/<variant>` stays on disk
>   after the build (tens of MB); switching `aur_variant` on a live box leaves
>   the old helper's dir and binary behind (no uninstall task). AUR packages
>   keep working with whichever helper is present. Acceptable? (non-blocking,
>   default: yes)
> - **`x_commands` is deleted from `group_vars/arch.yml`** and
>   `managers/aur.yml` stops reading it. Any external tooling that sourced that
>   key must move to `aur_variant`. None exists in-repo (grep-verified).
>   (non-blocking, default: yes)

### Open Questions

None — all design questions resolved in review (see `docs/temp/active-task.md`
for the full round-by-round record).

## 4. Affected Files & Contracts

All paths under `ansible/`. `ansible_bck/` is untouched.

### [MODIFY] inventory/hosts.yml

Add the single-select key next to the other variants:
`aur_variant: yay` (this machine selects yay, per the user).

- Contract: `ansible-inventory -i inventory/hosts.yml --host thispc | grep -c
  '"aur_variant"'` is "1".

### [NEW] roles/aur_helper/defaults/main.yml

The one role-local derived var:

```yaml
aur_helper_src_dir: "/home/{{ x_target_user }}/aur/{{ aur_variant }}"
```

- Contract: `grep -c 'aur_helper_src_dir' roles/aur_helper/defaults/main.yml`
  is "1"; `ansible-lint ansible/roles/aur_helper` exits 0.

### [MODIFY] roles/aur_helper/tasks/main.yml

Becomes the dispatcher, the exact shape of `roles/snapshots/tasks/main.yml`:
one `include_tasks: "helpers/{{ aur_variant }}.yml"` with
`when: aur_variant is not none`. No URLs, no paths, no build logic remain in
`main.yml`.

- Contract: `grep -c 'helpers/{{ aur_variant }}.yml' roles/aur_helper/tasks/main.yml`
  is "1"; `grep -c 'is not none' roles/aur_helper/tasks/main.yml` is "1".

### [NEW] roles/aur_helper/tasks/helpers/paru.yml

Clone-then-build skeleton for paru: `git clone
https://aur.archlinux.org/paru.git {{ aur_helper_src_dir }}` (as
`target_user`, `creates: {{ aur_helper_src_dir }}`), then
`makepkg -si --noconfirm` with `chdir: {{ aur_helper_src_dir }}`,
`creates: /usr/bin/paru`, `become_user: "{{ x_target_user }}"`,
`changed_when: true`.

- Contract: `grep -c 'creates: /usr/bin/paru' roles/aur_helper/tasks/helpers/paru.yml`
  is "1"; `grep -c 'aur.archlinux.org/paru.git' roles/aur_helper/tasks/helpers/paru.yml`
  is "1"; `grep -c 'yay' roles/aur_helper/tasks/helpers/paru.yml` is "0".

### [NEW] roles/aur_helper/tasks/helpers/yay.yml

Same skeleton for yay: clone `https://aur.archlinux.org/yay.git` into
`{{ aur_helper_src_dir }}`, build in the same dir,
`creates: /usr/local/bin/yay`. No reference to paru anywhere (exclusivity).

- Contract: `grep -c 'creates: /usr/local/bin/yay'
  roles/aur_helper/tasks/helpers/yay.yml` is "1";
  `grep -c 'aur.archlinux.org/yay.git' roles/aur_helper/tasks/helpers/yay.yml`
  is "1"; `grep -c 'paru' roles/aur_helper/tasks/helpers/yay.yml` is "0".

### [MODIFY] roles/install_packages/tasks/managers/aur.yml

Rewritten: `ansible.builtin.command: "{{ aur_variant }} -S --needsys
--noconfirm {{ pkg_list | join(' ') }}"`, same `become`/`become_user`/
`changed_when` as today. Reads no `x_commands`.

- Contract: `grep -c 'aur_variant' roles/install_packages/tasks/managers/aur.yml`
  is "1"; `grep -c 'x_commands' roles/install_packages/tasks/managers/aur.yml`
  is "0".

### [MODIFY] inventory/group_vars/arch.yml

Delete the `x_commands` key (and its `aur.install` leaf) entirely. No other
change.

- Contract: `grep -c 'x_commands' inventory/group_vars/arch.yml` is "0"; the
  file still parses (`python -c "import yaml; yaml.safe_load(open('inventory/group_vars/arch.yml'))"`).

### [MODIFY] plays/02_system.yml

Add `when: aur_variant is not none` to the existing `aur_helper` include (same
idiom as the `gpu`/`audio`/`snapshots` includes at lines 20-49). Order relative
to `repos` and `base_packages` is unchanged and load-bearing.

- Contract: `grep -A2 'name: aur_helper' plays/02_system.yml | grep -c
  'is not none'` is "1"; `ansible-playbook -i inventory/hosts.yml site.yml
  --syntax-check` passes.

### [MODIFY] README.md (ansible/)

Add `aur_variant` to the variant vocabulary, note the `~`-skips semantics in
the play 02 row, and replace the `commands.aur.install` mention with the
`aur_variant` story.

- Contract: `grep -c 'aur_variant' README.md` is "1";
  `grep -c 'commands.aur.install' README.md` is "0".

## 5. Task DAG

All commands run from `ansible/` on a Linux host with `ansible-core` and
`ansible-lint` installed.

### Task 1: Inventory selection key

- Target Files: [MODIFY] inventory/hosts.yml
- Depends On: None
- Subtasks:
  - [x] 1.1 Add `aur_variant: yay` to the `thispc` host entry, next to the
    other `*_variant` keys.
    - Input: ADR-018 variant vocabulary; current hosts.yml
    - Output: hosts.yml with the new key
    - Verify: `ansible-inventory -i inventory/hosts.yml --host thispc | grep -c '"aur_variant"'`
    - Expect: "1"
- Phase Gate: `ansible-inventory -i inventory/hosts.yml --host thispc | grep -E '"(aur_variant|gpu_variant)"' | wc -l`
  (Expect: "2")

### Task 2: The `aur_helper` role becomes variant-dispatched and self-sourcing

- Target Files: [NEW] roles/aur_helper/defaults/main.yml, [MODIFY]
  roles/aur_helper/tasks/main.yml, [NEW]
  roles/aur_helper/tasks/helpers/paru.yml, [NEW]
  roles/aur_helper/tasks/helpers/yay.yml
- Depends On: Task 1
- Subtasks:
  - [x] 2.1 Write `defaults/main.yml` with `aur_helper_src_dir`.
    - Input: section 4 contract; the user's proposed
      `/home/<user>/aur/<helper>` shape
    - Output: defaults/main.yml
    - Verify: `grep -c 'aur_helper_src_dir' roles/aur_helper/defaults/main.yml`
    - Expect: "1"
  - [x] 2.2 Write `helpers/paru.yml`: clone the paru AUR repo, build in
    `{{ aur_helper_src_dir }}`, guard `creates: /usr/bin/paru`.
    - Input: current main.yml build logic (repo URL and build command),
      output of 2.1
    - Output: helpers/paru.yml
    - Verify: `grep -c -E 'aur.archlinux.org/paru.git|creates: /usr/bin/paru' roles/aur_helper/tasks/helpers/paru.yml`
    - Expect: "2"
  - [x] 2.3 Write `helpers/yay.yml`: same skeleton, yay repo,
    `creates: /usr/local/bin/yay`, zero paru references.
    - Input: output of 2.2 as the shape reference
    - Output: helpers/yay.yml
    - Verify: `grep -c -E 'aur.archlinux.org/yay.git|creates: /usr/local/bin/yay' roles/aur_helper/tasks/helpers/yay.yml`
    - Expect: "2"
  - [x] 2.4 Rewrite `main.yml` as the filename dispatcher with the `~` guard
    (snapshots role shape).
    - Input: ADR-018; roles/snapshots/tasks/main.yml as the shape reference
    - Output: main.yml with one include + one `when`
    - Verify: `grep -c 'helpers/{{ aur_variant }}.yml' roles/aur_helper/tasks/main.yml`
    - Expect: "1"
- Phase Gate: `ansible-lint ansible/roles/aur_helper`

### Task 3: The AUR manager and the `x_commands` deletion

- Target Files: [MODIFY] roles/install_packages/tasks/managers/aur.yml,
  [MODIFY] inventory/group_vars/arch.yml
- Depends On: Task 2
- Subtasks:
  - [x] 3.1 Rewrite `managers/aur.yml` to invoke `{{ aur_variant }}` with the
    common flags; drop the `x_commands` read.
    - Input: current aur.yml (flags, become, changed_when), ADR-009
    - Output: managers/aur.yml
    - Verify: `grep -c 'aur_variant' roles/install_packages/tasks/managers/aur.yml`
    - Expect: "1"
  - [x] 3.2 Delete the `x_commands` key from `group_vars/arch.yml`.
    - Input: grep-verified absence of any other `x_commands` consumer in
      `ansible/`
    - Output: arch.yml without `x_commands`
    - Verify: `grep -c 'x_commands' inventory/group_vars/arch.yml`
    - Expect: "0"
- Phase Gate: `ansible-playbook -i inventory/hosts.yml site.yml --syntax-check`

### Task 4: Play 02 guard and docs

- Target Files: [MODIFY] plays/02_system.yml, [MODIFY] README.md
- Depends On: Task 3
- Subtasks:
  - [x] 4.1 Add `when: aur_variant is not none` to the `aur_helper` include.
    - Input: the `gpu`/`audio`/`snapshots` include idiom in the same file
    - Output: guarded include, unchanged order
    - Verify: `grep -A2 'name: aur_helper' plays/02_system.yml | grep -c 'is not none'`
    - Expect: "1"
  - [x] 4.2 Update the README: `aur_variant` in the variant vocabulary, play 02
    row, and the old `commands.aur.install` mention removed.
    - Input: section 4 contract
    - Output: README.md updated
    - Verify: `grep -c 'aur_variant' README.md`
    - Expect: "1"
- Phase Gate: `ansible-playbook -i inventory/hosts.yml site.yml --syntax-check && ansible-lint ansible/`

### Completion rules

- State lives on subtasks: `[ ]` pending -> `[/]` in progress -> `[x]` done.
- A subtask is `[x]` only when Verify exits 0 AND the output matches Expect;
  evidence recorded in `docs/temp/verify-state.json`.
- Before marking `[x]`, run the four passes: implement, expert re-read, defect
  hunt, polish.
- An impossible subtask is never deleted: it gets `ABANDON: <non-empty reason>`.
- A task is done only when every subtask is `[x]` AND its Phase Gate is green.
- The spec is done only when a fresh re-run of every Phase Gate is green.

## 6. Verification Commands

- Build Command: `ansible-playbook -i inventory/hosts.yml site.yml --syntax-check` (from `ansible/`)
- Test Command: `ansible-lint ansible/`
- Lint Command: `ansible-lint ansible/`

## 7. Rollback Strategy

All changes are additive or single-file moves under `ansible/`. Revert in
reverse Task DAG order: Task 4 (play 02 `when` line, README) -> Task 3
(`git checkout` managers/aur.yml and group_vars/arch.yml) -> Task 2 (`git rm`
the `helpers/` files and `defaults/`, restore `main.yml` from git) -> Task 1
(inventory key). No data migration: a machine on `aur_variant: paru` converges
to a strictly improved version of the current behavior (the paru build now
actually works on a fresh box instead of assuming a clone that never happens).
If verification fails 3 consecutive times on any subtask the circuit breaker
fires (`docs/temp/escalation.md`), dirty edits are reverted, and the subtask
reverts to `[ ]`.
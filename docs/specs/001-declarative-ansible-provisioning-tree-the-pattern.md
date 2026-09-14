---
tags: [ansible, provisioning, arch-linux, declarative-config, architecture]
---

# 001: Declarative Ansible Provisioning Tree (The Pattern)

Status: APPROVED

## 1. Goal & Context

Rebuild machine provisioning from scratch as a new `ansible/` tree governed by one rule —
presence over flags — and four variable layers (inventory → `group_vars/<distro>` → role
defaults → role tasks), so adding a package, app, module, component, window manager, distro
or package manager touches no existing code. The build is greenfield: the previous implementation
in `ansible_bck/` is ignored entirely — nothing is migrated from it and it is not consulted as a
reference.

## 2. Architectural Decisions & Trade-offs

1. **Presence over flags: a key's value answers *what*, its existence answers *whether*.**
   Alternative: separate `install_x: true` booleans beside the data. Rejected: two keys for
   one fact drift apart. (consequence flagged in section 3)
2. **`~` is the only subtraction operator; absence means "take the default".**
   Alternative: treat omission as removal. Rejected: `combine` merges defaults back in, so
   omission cannot subtract; `none` is also rejected — YAML reads it as the string `"none"`.
   (consequence flagged in section 3)
3. **Every loop over a merged dict ends in `| dict2items | rejectattr('value','none') | list`.**
   Alternative: `when: item.value is not none` on the include. Rejected: the loop label still
   renders and a nulled key can still resolve a role name; filtering at the source is one place.
4. **Four layers, using Ansible's native precedence — no custom merge logic beyond decision 7.**
   Alternative: a custom vars plugin or `hash_behaviour=merge`. Rejected: global merge
   semantics are invisible at the call site and break other people's roles.
5. **One inventory file, one host; the distro is the Ansible group name.**
   Alternative: a `distro:` variable plus `include_vars` lookup. Rejected: the group name
   auto-loads `group_vars/<distro>.yml` with zero lookup logic. `distro:` is still declared
   inside the distro file for play 01, the one place that needs the string.
6. **Each `group_vars/<distro>.yml` is self-contained; nothing is shared between distro files.**
   Alternative: a shared `group_vars/all.yml` (what `ansible_bck` did). Rejected: Ansible
   overwrites rather than merges those dicts; duplication is cheaper than silent clobbering.
7. **The two-variable trick: `X_defaults` + empty `X_overrides` → lazily-evaluated `X`.**
   Alternative: inventory writes the full dict. Rejected: dicts are replaced across precedence
   levels, so a one-line inventory delta would delete the rest of the set.
8. **Package vocabulary is keyed by role name: `packages.<role_name>` → `{manager: [pkgs]}`.**
   Alternative: free-form package keys. Rejected: matching key to role name makes "what does
   this role install?" answerable without opening the role.
9. **One shared `install_packages` role dispatching by filename: `managers/<mgr>.yml`.**
   Alternative: `when: ansible_distribution == ...` chains inside each role. Rejected: every
   new distro would edit every role.
10. **Real Ansible modules, never `command:`, except managers with no module.**
    Alternative: shell out uniformly. Rejected: modules report `changed` honestly and support
    `--check`, which is what makes plays 02–04 re-runnable. The escape hatch is a
    `commands.<mgr>.install` string in `group_vars` (AUR/`paru` today).
11. **Four role archetypes with prefix-encoded names:** `desktop_*`, `component_*`,
    `workflow_*`, `app_*`, plus bare system roles. Alternative: flat unprefixed names (as in
    `ansible_bck`). Rejected: the prefix is what lets plays dispatch by string interpolation.
12. **Plays are thin: four numbered plays that loop and include, holding no data and no logic.**
    Alternative: per-machine playbooks, or generating playbooks from a manifest (the
    `generators/manifest_to_playbook.py` of the old tree). Rejected: generated playbooks are a
    second source of truth. (consequence flagged in section 3)
13. **Play 01 is the only non-re-runnable, distro-branching play; 02–04 are idempotent.**
    Alternative: make bootstrap idempotent too. Rejected: it wipes a disk; re-runnability is
    not a meaningful property there, and already-installed hosts simply start at 02.
14. **Dotfiles are a git clone plus GNU `stow -R` per package, named after the role key; the repo
    URL is a machine fact declared in inventory.** Alternative: `copy`/`template` each config, and
    a `dotfiles_repo` default in the role. Rejected: the dotfiles repo stays the source of truth
    and restow is re-runnable; and since every user has a different config repo, the URL differs
    between machines on the same distro and is therefore layer-1 data, not a role default.
15. **User-level services are enabled, never started, with `XDG_RUNTIME_DIR` set and
    `loginctl enable-linger` in play 02.** Alternative: `state: started`. Rejected: it requires
    a live session; the final manual reboot starts them.
16. **`bootstrap.sh` at the repo root carries the live-ISO preamble** (cowspace remount, keyring,
    ansible install, galaxy requirements). Alternative: documentation only. Rejected: it is run
    at 2am from a live ISO and the cowspace line will not be remembered.
17. **Greenfield build; `ansible_bck/` is ignored entirely and never consulted.**
    Alternative: incremental refactor in place, or keeping the old tree as a reference corpus for
    package lists and quirks. Rejected: the old tree's branching and generator conflict with every
    decision above, and copying from it is how the old shape leaks back in — the rebuild exists to
    carry no baggage. (consequence flagged in section 3)
18. **Mutually-exclusive implementations are variants: the role ships all of them and inventory
    names one (`gpu_variant`, `audio_variant`, `snapshot_variant`).** Alternative: a separate role
    per implementation (`roles/snapper`, `roles/timeshift`) selected by the caller. Rejected: the
    choice is then encoded in whoever includes the role, so two places know about it; a variant
    key keeps "which one" in inventory where every other machine fact lives, and `~` disables the
    role entirely with no extra mechanism.

## 3. Risks & Open Questions

> [!IMPORTANT]
> **User Review Required**
> - Every enable/disable becomes an inventory edit; there is no boolean to flip and no
>   `--extra-vars` toggle for skipping a component — consequence of decision 2.1. Acceptable?
> - `neovim: {}` and an absent `neovim` key are identical, so inventory alone never shows the
>   full roster; the roster lives in role defaults — consequence of decision 2.2. Acceptable?
> - The old `generators/manifest_to_playbook.py` workflow disappears; playbooks are hand-written
>   and static — consequence of decision 2.12. Acceptable?
> - Package lists, distro quirks and hardware workarounds already solved in the old tree are
>   re-derived from scratch, so the first provisioning run is expected to surface gaps that were
>   previously fixed — consequence of decision 2.17. Acceptable?
> - Verification cannot run on this Windows workstation. Python 3.14.7 is installed and
>   `ansible-core` + `ansible-lint` were installed into it, but neither runs here: `ansible`
>   aborts with "requires the locale encoding to be UTF-8; Detected 1252" and `ansible-lint`
>   with "No module named 'grp'" (a POSIX-only module) — Windows is not a supported Ansible
>   controller, and WSL is not installed. Every Task DAG `Verify` command is therefore executable
>   only on a Linux host or after `wsl.exe --install` — consequence of decision 2.17 (greenfield
>   Ansible dependency). Acceptable?

### Open Questions

- [x] Q1: RESOLVED — Fedora is shape only. `group_vars/fedora.yml` exists to prove the vocabulary
  shape holds for a second distro and package manager; it is not required to be package-accurate
  and is not a supported target until someone makes it one.
- [x] Q2: RESOLVED — `dotfiles_repo` is not a role default at all; it is declared per machine in
  `inventory/hosts.yml`, because every user has a different config repo (decision 2.14). The
  concrete URL is supplied by whoever writes the inventory entry, not by this spec.
- [x] Q3: RESOLVED — parked. The current goal is the decision record, not the tree; no
  implementation code is written from this spec yet. `workflow_gaming` and `workflow_creative`
  are follow-up work and are not in Task 9.
- [x] Q4: RESOLVED — `snapshots` ships all mechanisms and the machine selects one, exactly like
  `gpu` and `audio`: `snapshot_variant` in inventory picks the implementation (snapper, timeshift,
  …), `packages.snapshots.<variant>` supplies its packages, and `~` means no snapshots at all.
  Filesystem suitability is the inventory author's call, not a runtime check.
- [x] Q5: RESOLVED — Python 3.14.7 is installed (`py`); the framework engines run. Ansible itself
  still cannot run on this workstation (see the verification risk above), so Task DAG execution
  needs a Linux host or WSL.

## 4. Affected Files & Contracts

All paths are under the repo root. `ansible_bck/**` is out of scope: not read, not modified, not
deleted by this spec (decision 2.17).

- Deleted: none

### [NEW] ansible/ansible.cfg

Inventory path, role path, `interpreter_python: auto_silent`, stdout callback.

- Contract:
  - `[defaults] inventory = inventory/hosts.yml`, `roles_path = roles`

### [NEW] ansible/requirements.yml

Galaxy collections installed on the live ISO before play 01.

- Contract:
  - lists `community.general` (pacman, flatpak, aur command deps)

### [NEW] bootstrap.sh

Live-ISO preamble: cowspace remount, `iwctl` reminder, keyring, `git`+`ansible`, galaxy install,
`ansible-playbook plays/01_bootstrap.yml`.

### [NEW] ansible/inventory/hosts.yml

Layer 1. One file, one host; group name == distro; machine facts, single-select choices,
`desktop_overrides` deltas, `modules` tree.

- Contract:
  - `all.children.<distro>.hosts.<hostname>` with `ansible_connection: local`
  - keys: `target_disk`, `target_user`, `hostname`, `timezone`, `locale`, `partitions`,
    `dotfiles_repo`, `wm_choice`, `gpu_variant`, `audio_variant`, `snapshot_variant`,
    `desktop_overrides`, `modules`

### [NEW] ansible/group_vars/arch.yml

Layer 2. Arch vocabulary; `distro: arch`, bootstrap mechanics, `commands.aur.install`,
`packages.*` keyed by role name.

- Contract:
  - `distro`, `target_root`, `chroot_prefix`, `bootstrap_cmd`, `commands`, `packages`
  - every `packages.<key>` leaf is `{<manager>: [<pkg>, ...]}`

### [NEW] ansible/group_vars/fedora.yml

Layer 2, same key shape, dnf/flatpak values, no bootstrap keys, `commands: {}`.

### [NEW] ansible/roles/install_packages/tasks/main.yml

Archetype A. Loops `package_source` and includes one file per manager key.

- Contract:
  - input var `package_source: {<manager>: [<pkg>, ...]}`
  - includes `managers/{{ mgr.key }}.yml` with `pkg_list` set

### [NEW] ansible/roles/install_packages/tasks/managers/pacman.yml

`community.general.pacman`, `state: present`, `become: true`.

### [NEW] ansible/roles/install_packages/tasks/managers/dnf.yml

`ansible.builtin.dnf`, `state: present`, `become: true`.

### [NEW] ansible/roles/install_packages/tasks/managers/flatpak.yml

`community.general.flatpak`, `state: present`, `become: true`.

### [NEW] ansible/roles/install_packages/tasks/managers/aur.yml

`ansible.builtin.command: "{{ commands.aur.install }} ..."`, `become_user: target_user`,
`changed_when` on paru's "there is nothing to do".

### [NEW] ansible/roles/dotfiles/{defaults,tasks}/main.yml

Clones the inventory-supplied `dotfiles_repo` to `dotfiles_path` as `target_user`; runs once in
play 02.

- Contract:
  - defaults expose `dotfiles_path` only; `dotfiles_repo` is required from inventory (layer 1)
    and has no default

### [NEW] ansible/roles/stow/{defaults,tasks}/main.yml

`stow -d {{ dotfiles_path }} -t {{ stow_target }} -R {{ stow_package }}`; `changed_when` on
`'LINK' in r.stderr`.

- Contract:
  - input var `stow_package` (named identically to the calling component/app key)

### [NEW] ansible/roles/bootstrap_arch/tasks/main.yml

Play-01 only: partition `target_disk` per `partitions`, format, mount at `target_root`,
`bootstrap_cmd`, fstab, chroot config (locale, timezone, hostname), user + `user_password_hash`,
bootloader.

### [NEW] ansible/roles/{base,network,firewall,ssh}/tasks/main.yml

Archetype B. Each includes `install_packages` with `package_source: "{{ packages.<role> }}"`;
`network`/`firewall`/`ssh` additionally enable their unit via `systemd_service`.

### [NEW] ansible/roles/gpu/tasks/main.yml

Archetype B with a variant path: `package_source: "{{ packages.gpu[gpu_variant] }}"`.

### [NEW] ansible/roles/audio/tasks/main.yml

Archetype B with a variant path: `package_source: "{{ packages.audio[audio_variant] }}"`.

### [NEW] ansible/roles/snapshots/tasks/main.yml

Archetype C with a variant path (decision 18): installs
`packages.snapshots[snapshot_variant]`, then includes `variants/{{ snapshot_variant }}.yml` for
that mechanism's own configuration.

- Contract:
  - skipped entirely when `snapshot_variant` is `~`

### [NEW] ansible/roles/snapshots/tasks/variants/{snapper,timeshift}.yml

One file per mechanism, dispatched by filename exactly as the package managers are; a new
mechanism is a new file and one `packages.snapshots.<variant>` key.

### [NEW] ansible/roles/desktop_hyprland/{defaults,tasks}/main.yml

Holds the Hyprland component roster via the two-variable trick.

- Contract:
  - `desktop_profile` (6 keys → `component_*` role names), `desktop_overrides: {}`,
    `desktop_components: "{{ desktop_profile | combine(desktop_overrides, recursive=True) }}"`

### [NEW] ansible/roles/desktop_gnome/{defaults,tasks}/main.yml

Same three variables with `desktop_profile: {}`; tasks install `packages.desktop_gnome` and
enable `gdm`.

### [NEW] ansible/roles/component_{screenshot,notification,bar,lock,idle,launcher}/tasks/main.yml

Archetype C. Install `packages.component_<name>`, then `stow` the like-named dotfiles package;
`component_idle` additionally enables a user-scope unit.

### [NEW] ansible/roles/workflow_{development,ai,entertainment}/{defaults,tasks}/main.yml

Archetype D. `module_defaults` in defaults; tasks merge with `modules.<name>`, reject nulls,
include `app_{{ app.key }}` with `app_params`.

### [NEW] ansible/roles/app_{git,docker,neovim,vscode,llamacpp,opencode,vlc,firefox}/{defaults,tasks}/main.yml

Merge `app_defaults` with `app_params` into `cfg`, install `packages.app_<name>`, then do the
app's own work (docker: service + group; neovim: stow the `distro_config`; llamacpp: build with
`cmake_flags`).

### [NEW] ansible/plays/01_bootstrap.yml

Disk confirmation pause, password prompt + `password_hash('sha512')` with `no_log`,
`include_role: bootstrap_{{ distro }}`. No `become:` anywhere.

### [NEW] ansible/plays/02_harden.yml

Includes `dotfiles`, `network`, `firewall`, `ssh`, `audio`, `snapshots`; runs
`loginctl enable-linger {{ target_user }}`.

### [NEW] ansible/plays/03_desktop.yml

Includes `desktop_{{ wm_choice }}`, then loops `desktop_components` with the null filter. Task
order is load-bearing.

### [NEW] ansible/plays/04_workflows.yml

Loops `modules` with the null filter, including `workflow_{{ mod.key }}`.

### [MODIFY] AGENTS.md

`Tech Stack` gains Ansible; `Repo map` gains `ansible/`; `Commands` replaces `n/a` with the
section-6 commands.

### [NEW] ansible/README.md

Layer map, the `~` rule, the "where does variable X go?" ladder, and the live-ISO checklist.

## 5. Task DAG

All commands run from the repo root on a Linux host (or WSL) with `ansible-core`,
`ansible-lint` and `community.general` installed — see the section-3 risk.

### Task 1: Ansible plumbing and live-ISO entrypoint

- Target Files: [NEW] ansible/ansible.cfg, [NEW] ansible/requirements.yml, [NEW] bootstrap.sh
- Depends On: None
- Subtasks:
  - [ ] 1.1 Write `ansible/ansible.cfg` with `inventory`, `roles_path`, `interpreter_python`.
    - Input: decision 2.4 (native precedence, no custom merge)
    - Output: ansible/ansible.cfg
    - Verify: `ansible-config dump --only-changed -c ansible/ansible.cfg`
    - Expect: "roles_path"
  - [ ] 1.2 Write `ansible/requirements.yml` pinning `community.general`.
    - Input: manager modules used in Task 4
    - Output: ansible/requirements.yml
    - Verify: `ansible-galaxy collection install -r ansible/requirements.yml --force`
    - Expect: "community.general"
  - [ ] 1.3 Write `bootstrap.sh` (cowspace remount, keyring, ansible install, galaxy, play 01).
    - Input: decision 2.16
    - Output: bootstrap.sh
    - Verify: `bash -n bootstrap.sh && grep -c 'cowspace' bootstrap.sh`
    - Expect: "1"
- Phase Gate: `bash -n bootstrap.sh && ansible-config dump --only-changed -c ansible/ansible.cfg`

### Task 2: Layer 1 — inventory

- Target Files: [NEW] ansible/inventory/hosts.yml
- Depends On: Task 1
- Subtasks:
  - [ ] 2.1 Write the single host entry: connection, hardware facts, `partitions`, and the
        per-machine `dotfiles_repo`.
    - Input: decisions 2.5, 2.4, 2.14
    - Output: ansible/inventory/hosts.yml
    - Verify: `ansible-inventory -i ansible/inventory/hosts.yml --host <hostname> | grep -c -E '"(ansible_connection|target_disk|dotfiles_repo)"'`
    - Expect: "3"
  - [ ] 2.2 Add the single-select choices `wm_choice`, `gpu_variant`, `audio_variant`,
        `snapshot_variant`.
    - Input: output of 2.1; decision 2.18
    - Output: choice keys in hosts.yml
    - Verify: `ansible-inventory -i ansible/inventory/hosts.yml --host <hostname> | grep -c -E '"(wm_choice|gpu_variant|audio_variant|snapshot_variant)"'`
    - Expect: "4"
  - [ ] 2.3 Add `desktop_overrides` deltas and the `modules` tree, including one `~` entry.
    - Input: decisions 2.1, 2.2
    - Output: override + module keys in hosts.yml
    - Verify: `ansible-inventory -i ansible/inventory/hosts.yml --host <hostname> | grep -c 'null'`
    - Expect: "1"
- Phase Gate: `ansible-inventory -i ansible/inventory/hosts.yml --graph`

### Task 3: Layer 2 — distro vocabularies

- Target Files: [NEW] ansible/group_vars/arch.yml, [NEW] ansible/group_vars/fedora.yml
- Depends On: Task 2
- Subtasks:
  - [ ] 3.1 Write `arch.yml`: `distro`, bootstrap mechanics, `commands.aur.install`.
    - Input: decisions 2.5, 2.6, 2.10
    - Output: ansible/group_vars/arch.yml
    - Verify: `ansible-inventory -i ansible/inventory/hosts.yml --host <hostname> | grep -c 'chroot_prefix'`
    - Expect: "1"
  - [ ] 3.2 Add every `packages.<role_name>` key (base, gpu, audio, network, firewall, ssh,
        desktop_*, component_*, app_*) with manager-keyed leaves.
    - Input: decision 2.8; role roster from Tasks 6-9
    - Output: `packages` tree in arch.yml
    - Verify: `grep -c '^  [a-z_]*:' ansible/group_vars/arch.yml`
    - Expect: "26"
  - [ ] 3.3 Write `fedora.yml` mirroring the same keys with dnf/flatpak values and no
        bootstrap keys. Shape-proving only (Q1): key coverage matters, package accuracy does not.
    - Input: output of 3.2, decision 2.6
    - Output: ansible/group_vars/fedora.yml
    - Verify: `diff <(grep -o '^  [a-z_]*:' ansible/group_vars/arch.yml | sort) <(grep -o '^  [a-z_]*:' ansible/group_vars/fedora.yml | sort) | grep -c '^>'`
    - Expect: "0"
- Phase Gate: `ansible-inventory -i ansible/inventory/hosts.yml --host <hostname> | grep packages`

### Task 4: The shared installer

- Target Files: [NEW] ansible/roles/install_packages/tasks/main.yml, [NEW] ansible/roles/install_packages/tasks/managers/{pacman,dnf,flatpak,aur}.yml
- Depends On: Task 3
- Subtasks:
  - [ ] 4.1 Write `main.yml` dispatching `managers/{{ mgr.key }}.yml` over `package_source`.
    - Input: decision 2.9
    - Output: install_packages/tasks/main.yml
    - Verify: `grep -c 'managers/{{ mgr.key }}.yml' ansible/roles/install_packages/tasks/main.yml`
    - Expect: "1"
  - [ ] 4.2 Write the four manager files, module-based except `aur`.
    - Input: decision 2.10
    - Output: managers/{pacman,dnf,flatpak,aur}.yml
    - Verify: `ls ansible/roles/install_packages/tasks/managers/*.yml | wc -l`
    - Expect: "4"
  - [ ] 4.3 Confirm `aur.yml` runs as `target_user` with an honest `changed_when`.
    - Input: output of 4.2
    - Output: corrected aur.yml
    - Verify: `grep -c -E 'become_user|changed_when' ansible/roles/install_packages/tasks/managers/aur.yml`
    - Expect: "2"
- Phase Gate: `ansible-lint ansible/roles/install_packages`

### Task 5: Utility roles — dotfiles and stow

- Target Files: [NEW] ansible/roles/dotfiles/{defaults,tasks}/main.yml, [NEW] ansible/roles/stow/{defaults,tasks}/main.yml
- Depends On: Task 4
- Subtasks:
  - [ ] 5.1 Write `dotfiles`: defaults carry `dotfiles_path` only, tasks clone the
        inventory-supplied `dotfiles_repo` as `target_user`; no URL anywhere in the role.
    - Input: decision 2.14 (Q2 resolved: the repo URL is inventory data)
    - Output: roles/dotfiles/
    - Verify: `grep -c 'dotfiles_repo' ansible/roles/dotfiles/defaults/main.yml; grep -c 'dotfiles_repo' ansible/roles/dotfiles/tasks/main.yml`
    - Expect: "0\n1"
  - [ ] 5.2 Write `stow` with `-R` and `changed_when: "'LINK' in r.stderr"`.
    - Input: decision 2.14
    - Output: roles/stow/
    - Verify: `grep -c "LINK" ansible/roles/stow/tasks/main.yml`
    - Expect: "1"
- Phase Gate: `ansible-lint ansible/roles/dotfiles ansible/roles/stow`

### Task 6: System roles and play 02

- Target Files: [NEW] ansible/roles/{base,gpu,audio,network,firewall,ssh,snapshots}/tasks/main.yml, [NEW] ansible/plays/02_harden.yml
- Depends On: Task 5
- Subtasks:
  - [ ] 6.1 Write the seven system roles; `gpu`, `audio` and `snapshots` resolve their variant
        key, and `snapshots` also dispatches `variants/{{ snapshot_variant }}.yml`.
    - Input: decisions 2.8, 2.11, 2.18
    - Output: seven roles/*/tasks/main.yml plus snapshots/tasks/variants/
    - Verify: `ls -d ansible/roles/{base,gpu,audio,network,firewall,ssh,snapshots} | wc -l; ls ansible/roles/snapshots/tasks/variants/*.yml | wc -l`
    - Expect: "7\n2"
  - [ ] 6.2 Write `plays/02_harden.yml` including them in order plus `enable-linger`.
    - Input: decisions 2.12, 2.15
    - Output: ansible/plays/02_harden.yml
    - Verify: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/02_harden.yml --syntax-check`
    - Expect: "playbook: ansible/plays/02_harden.yml"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/02_harden.yml --syntax-check`

### Task 7: Bootstrap role and play 01

- Target Files: [NEW] ansible/roles/bootstrap_arch/tasks/main.yml, [NEW] ansible/plays/01_bootstrap.yml
- Depends On: Task 6
- Subtasks:
  - [ ] 7.1 Write `bootstrap_arch` (partition, format, mount, bootstrap_cmd, fstab, chroot
        config, user, bootloader).
    - Input: decision 2.13; `group_vars` bootstrap mechanics from 3.1
    - Output: roles/bootstrap_arch/tasks/main.yml
    - Verify: `grep -c -E 'chroot_prefix|bootstrap_cmd' ansible/roles/bootstrap_arch/tasks/main.yml`
    - Expect: "2"
  - [ ] 7.2 Write `plays/01_bootstrap.yml` with the wipe confirmation, hidden password prompt,
        `password_hash('sha512')` under `no_log`, and `include_role: bootstrap_{{ distro }}`.
    - Input: output of 7.1
    - Output: ansible/plays/01_bootstrap.yml
    - Verify: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/01_bootstrap.yml --syntax-check && grep -c 'no_log' ansible/plays/01_bootstrap.yml`
    - Expect: "1"
  - [ ] 7.3 Confirm play 01 contains no `become:` directive.
    - Input: output of 7.2
    - Output: verified play 01
    - Verify: `grep -c 'become' ansible/plays/01_bootstrap.yml || echo 0`
    - Expect: "0"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/01_bootstrap.yml --syntax-check`

### Task 8: Desktops, components and play 03

- Target Files: [NEW] ansible/roles/desktop_{hyprland,gnome}/{defaults,tasks}/main.yml, [NEW] ansible/roles/component_{screenshot,notification,bar,lock,idle,launcher}/tasks/main.yml, [NEW] ansible/plays/03_desktop.yml
- Depends On: Task 7
- Subtasks:
  - [ ] 8.1 Write both desktop roles using the two-variable trick
        (`desktop_profile` + `desktop_overrides` → `desktop_components`).
    - Input: decision 2.7
    - Output: roles/desktop_hyprland/, roles/desktop_gnome/
    - Verify: `grep -c 'desktop_profile | combine(desktop_overrides, recursive=True)' ansible/roles/desktop_hyprland/defaults/main.yml ansible/roles/desktop_gnome/defaults/main.yml | grep -c ':1'`
    - Expect: "2"
  - [ ] 8.2 Write the six `component_*` roles (install + stow, `component_idle` also enables a
        user-scope unit).
    - Input: decisions 2.11, 2.15
    - Output: six component roles
    - Verify: `ls -d ansible/roles/component_* | wc -l`
    - Expect: "6"
  - [ ] 8.3 Write `plays/03_desktop.yml` — desktop include first, then the filtered component
        loop (order is load-bearing).
    - Input: decisions 2.3, 2.12
    - Output: ansible/plays/03_desktop.yml
    - Verify: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/03_desktop.yml --syntax-check`
    - Expect: "playbook: ansible/plays/03_desktop.yml"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/03_desktop.yml --syntax-check`

### Task 9: Workflows, apps and play 04

- Target Files: [NEW] ansible/roles/workflow_{development,ai,entertainment}/{defaults,tasks}/main.yml, [NEW] ansible/roles/app_{git,docker,neovim,vscode,llamacpp,opencode,vlc,firefox}/{defaults,tasks}/main.yml, [NEW] ansible/plays/04_workflows.yml
- Depends On: Task 8
- Subtasks:
  - [ ] 9.1 Write the three orchestrator roles (merge `module_defaults` with `modules.<name>`,
        reject nulls, include `app_<key>` with `app_params`).
    - Input: decisions 2.3, 2.7; open question Q3
    - Output: three workflow roles
    - Verify: `grep -rc "rejectattr('value','none')" ansible/roles/workflow_*/tasks/main.yml | grep -c ':1'`
    - Expect: "3"
  - [ ] 9.2 Write the eight `app_*` roles merging `app_defaults` with `app_params` into `cfg`.
    - Input: output of 9.1
    - Output: eight app roles
    - Verify: `grep -rlc 'app_defaults | combine(app_params' ansible/roles/app_*/tasks/main.yml | wc -l`
    - Expect: "8"
  - [ ] 9.3 Write `plays/04_workflows.yml` looping `modules` with the null filter.
    - Input: decision 2.12
    - Output: ansible/plays/04_workflows.yml
    - Verify: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/04_workflows.yml --syntax-check`
    - Expect: "playbook: ansible/plays/04_workflows.yml"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/04_workflows.yml --syntax-check`

### Task 10: Pattern audit and documentation

- Target Files: [MODIFY] AGENTS.md, [NEW] ansible/README.md
- Depends On: Task 9
- Subtasks:
  - [ ] 10.1 Audit the null sentinel: every merged-dict loop carries the reject filter
        (plays 03 and 04, three workflow roles).
    - Input: decision 2.3
    - Output: audit result
    - Verify: `grep -rc "rejectattr('value','none')" ansible/plays ansible/roles | grep -v ':0' | wc -l`
    - Expect: "5"
  - [ ] 10.2 Lint the whole tree.
    - Input: Tasks 1-9
    - Output: clean lint run
    - Verify: `ansible-lint ansible/`
    - Expect: "Passed"
  - [ ] 10.3 Update `AGENTS.md` (tech stack, repo map, commands) and write `ansible/README.md`.
    - Input: section 6 commands
    - Output: AGENTS.md, ansible/README.md
    - Verify: `grep -c 'ansible-lint' AGENTS.md`
    - Expect: "1"
- Phase Gate: `ansible-lint ansible/ && for p in ansible/plays/0*.yml; do ansible-playbook -i ansible/inventory/hosts.yml "$p" --syntax-check; done`

### Completion rules

- State lives on subtasks: `[ ]` pending → `[/]` in progress → `[x]` done.
- A subtask is `[x]` only when Verify exits 0 AND the output matches Expect; evidence recorded
  in `docs/temp/verify-state.json`. Exit 0 alone is never enough.
- Before marking `[x]`, run the four passes: implement, expert re-read, defect hunt, polish.
- An impossible subtask is never deleted: it gets `ABANDON: <non-empty reason>`, never `[x]`.
- A task is done only when every subtask is `[x]` AND its Phase Gate is green.
- The spec is done only when a fresh re-run of every Phase Gate is green.

## 6. Verification Commands

- Build Command: `for p in ansible/plays/0*.yml; do ansible-playbook -i ansible/inventory/hosts.yml "$p" --syntax-check; done`
- Test Command: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/02_harden.yml --check`
- Lint Command: `ansible-lint ansible/`

## 7. Rollback Strategy

Revert edits in reverse Task DAG order: Task 10 (docs) → Task 9 (workflows/apps/play 04) →
Task 8 (desktop/components/play 03) → Task 7 (bootstrap_arch/play 01) → Task 6 (system
roles/play 02) → Task 5 (dotfiles/stow) → Task 4 (install_packages) → Task 3 (group_vars) →
Task 2 (inventory) → Task 1 (plumbing). The whole spec is additive under `ansible/` plus one
`AGENTS.md` edit, so `git rm -r ansible/ bootstrap.sh && git checkout -- AGENTS.md` restores the
pre-spec tree; `ansible_bck/` is never touched by this spec, but it is not a fallback either —
per decision 2.17 it is ignored. If any subtask
fails verification 3 consecutive times the circuit breaker fires (`docs/temp/escalation.md`),
dirty edits are reverted and the subtask reverts to `[ ]`.
---
tags: [ansible, plays, roles, arch-linux, hyprland, llama-cpp, ui-mode]
---

# 002: Plays and Roles — Current Target: Arch + Hyprland + Dev + AI

Status: APPROVED
Phase: 2-Build
Handoff: 2026-09-15

## 1. Goal & Context

Instantiate the pattern approved in spec 001 as a concrete roster: five plays, the named roles
inside each, and the first real module contents for this machine — Arch + Hyprland, a
`development` module carrying VS Code from pacman, and an `ai` module carrying a CUDA source
build of llama.cpp, `opencode-bin` from the AUR, and a model directory that is one config key.
Every app that only makes sense with a desktop disappears on a headless box through a single
derived `ui_mode`, with no `when:` on any task.

## 2. Architectural Decisions & Trade-offs

1. **`ui_mode` is a derived single-select (`cli` | `gui`), not a boolean.**
   `ui_mode: "{{ 'gui' if (wm_choice | default(None)) is not none else 'cli' }}"`. Alternative:
   an `install_gui: true` flag in inventory. Rejected: it is a second key stating a fact
   `wm_choice` already states, and spec 001 decision 1 forbids flags beside data. It is a
   single-select of the same class as `wm_choice`, so it dispatches like one.
   (consequence flagged in section 3)
2. **`group_vars/all.yml` exists, and holds cross-distro derivations only — no packages, no
   distro facts, no machine facts.** Alternative: repeat the `ui_mode` expression in every
   `group_vars/<distro>.yml` (what ADR-006 implies). Rejected: the derivation is not distro
   vocabulary, it is arithmetic on layer-1 data; duplicating it is how the two copies drift.
   The ADR-006 hazard — Ansible overwriting rather than merging `packages`-shaped dicts — does
   not apply because no dict in `all.yml` is redefined downstream. (consequence flagged in section 3)
3. **Desktop-only apps are gated at the roster, never with `when:`:**
   `module_defaults: "{{ module_cli | combine(module_gui if ui_mode == 'gui' else {}) }}"` in the
   workflow role's defaults. Alternative: `when: ui_mode == 'gui'` on the app include. Rejected:
   the skipped task still renders in output and the roster no longer states the truth; building
   the roster correctly means the app simply does not exist on a CLI box.
4. **Apps that exist in both forms are gated at the package key:**
   `packages.<role>: {cli: {...}, gui: {...}}` consumed as `packages.<role>[ui_mode]`.
   Alternative: two roles, `app_git_cli` and `app_git_gui`. Rejected: the role's behaviour is
   identical; only the package list differs, and spec 001 decision 8 already keys packages by
   role name.
5. **Five plays, not four: `05_finalise.yml` is split out of the workflow play.** Alternative:
   keep linger, default target and the resolved-config summary at the tail of `04_workflows.yml`
   (ADR-012's four-play shape). Rejected: reboot-adjacent, whole-machine work is not workflow
   work, and it must run after every module regardless of which modules ran.
   (consequence flagged in section 3)
6. **`bootstrap_arch` is an orchestrator over six ordered sub-roles** (`disk_partition`,
   `base_install`, `system_identity`, `user_create`, `bootloader`, `initial_network`), not one
   long task file. Alternative: a single `bootstrap_arch/tasks/main.yml`. Rejected: a second
   distro reuses `system_identity` and `user_create` verbatim; only partitioning and the
   base-install command are genuinely distro-specific.
7. **Source-built apps are a named escape hatch: `git` module + two `command:` cmake calls,
   guarded by `src.changed` or a missing build artifact.** Alternative: a shell script, or
   rebuilding unconditionally. Rejected: a no-op `git pull` must not trigger a half-hour CUDA
   compile, and the `git` module's `changed` is the only honest signal available. This extends
   ADR-010's escape-hatch list beyond the AUR command. (consequence flagged in section 3)
8. **CMake flags live as a YAML list in role defaults, not as a shell string.** Alternative: one
   `cmake_args: "-DGGML_CUDA=ON ..."` string. Rejected: inventory must be able to replace or
   extend the set for a different GPU without the role being edited; a list merges and diffs, a
   string does not. (consequence flagged in section 3)
9. **Where upstream ships a prebuilt AUR package, install it rather than build from source
   (`opencode-bin`).** Alternative: `opencode` (source AUR package). Rejected: a second
   compile-on-every-release toolchain buys nothing for a shipped binary; llama.cpp is built from
   source only because its flags are the point.
10. **Model storage is one key, `model_dir`, owned by `ai_model_store` and exported via
    `/etc/profile.d`; no AI role hardcodes a path.** Alternative: each AI app carries its own
    model path default. Rejected: moving the models to a dedicated NVMe would then be an edit in
    every AI role instead of one line in inventory. (consequence flagged in section 3)

## 3. Risks & Open Questions

> [!IMPORTANT]
> **User Review Required**
> - A headless box can never install a GUI or TUI-preferred app, even deliberately — `ui_mode` is
>   derived from `wm_choice` and there is no override key — consequence of decision 2.1. Acceptable?
> - `group_vars/all.yml` re-enters the tree after ADR-006 rejected it; the restriction to
>   derivations is a convention this spec enforces by review, not by a mechanism — consequence of
>   decision 2.2. Acceptable?
> - The play count in ADR-012 (four) no longer matches the tree (five); `site.yml` and every
>   runbook line that says "plays 02-04" must be read as "02-05" — consequence of decision 2.5.
>   Acceptable?
> - `app_llamacpp` is the first role whose correctness cannot be checked by `--check` mode: the
>   cmake calls are `command:` and their real effect is a compiled binary — consequence of
>   decision 2.7. Acceptable?
> - `-DGGML_NATIVE=ON` bakes in this CPU's feature set and `-DCMAKE_CUDA_ARCHITECTURES=89` is
>   Ada-only, so the build output is not portable between machines and artifacts can never be
>   cached across boxes — consequence of decision 2.8. Acceptable?
> - Until `model_dir` is pointed at real storage it defaults to
>   `/home/<user>/.local/share/models`, i.e. models land on the root filesystem — consequence of
>   decision 2.10. Acceptable?

### Open Questions

- [ ] Q1: Which filesystem path is `model_dir` on this machine? — parked by explicit instruction:
  the role default stands until storage is chosen; answer before Task 6 or accept the default.
- [ ] Q2: `display_manager` — greetd/tuigreet, or `~` and `Hyprland` from a tty? — decides whether
  play 03 enables a system unit; answer before Task 4, default `~` (start from tty).
- [ ] Q3: Does `snapshots` stay in play 02 for this machine, given the root filesystem is `ext4`
  in the current inventory? — answer before Task 3, or set `snapshot_variant: ~`.

## 4. Affected Files & Contracts

All paths are under the repo root, all additive on top of spec 001's tree. `ansible_bck/**` is
out of scope (spec 001, decision 2.17).

- Deleted: none

### [NEW] ansible/inventory/group_vars/all.yml

Cross-distro derivations only (decision 2.2). Currently one key.

- Contract:
  - `ui_mode: "{{ 'gui' if (wm_choice | default(None)) is not none else 'cli' }}"`
  - contains no `packages`, no `commands`, no machine facts

### [MODIFY] ansible/inventory/hosts.yml

The `thispc` entry for this machine: `wm_choice: hyprland`, `gpu_variant: nvidia_open`,
`audio_variant: pipewire`, and a `modules` tree with `development: {vscode: {}, docker: ~}` and
`ai: {llamacpp: {}, opencode: {}}`.

- Contract:
  - every module key is either `{}` (take defaults), a params dict, or `~` (subtract)

### [MODIFY] ansible/inventory/group_vars/arch.yml

Adds the package keys this roster needs.

- Contract:
  - `packages.app_llamacpp: {pacman: [cmake, base-devel, git, cuda, curl]}`
  - `packages.app_opencode: {aur: [opencode-bin]}`
  - `packages.app_vscode: {pacman: [code]}`
  - dual-form keys are shaped `{cli: {<mgr>: [...]}, gui: {<mgr>: [...]}}`

### [NEW] ansible/plays/01_bootstrap.yml

Live-ISO play. No `become:` (already root), not re-runnable; includes `bootstrap_{{ distro }}`.

### [NEW] ansible/roles/bootstrap_arch/tasks/main.yml

Orchestrator: includes `disk_partition` → `base_install` → `system_identity` → `user_create` →
`bootloader` → `initial_network` in that order.

### [NEW] ansible/roles/{disk_partition,base_install,system_identity,user_create,bootloader,initial_network}/tasks/main.yml

`disk_partition` confirms and wipes `target_disk`, creates ESP/swap/root from `partitions`,
formats, mounts `/mnt`. `base_install` runs `bootstrap_cmd` with `packages.base` and generates
fstab. `system_identity` sets hostname, timezone, locale, keymap, `/etc/hosts` in chroot.
`user_create` creates `target_user` with `user_password_hash`, wheel group, sudoers drop-in, and
registers `target_uid`. `bootloader` installs the boot manager, kernel params and microcode,
reading `gpu_variant` for `nvidia_drm.modeset=1`. `initial_network` installs and enables
NetworkManager.

- Contract:
  - `user_create` registers `target_uid` via `getent`; every later `become_user` depends on it

### [NEW] ansible/plays/02_system.yml

`become: true`, re-runnable. Includes, in order: `repos`, `aur_helper`, `base_packages`, `gpu`,
`audio`, `network`, `firewall`, `ssh`, `snapshots`, `external_drives`, `dotfiles`, `shell`.

### [NEW] ansible/roles/{repos,aur_helper,base_packages,external_drives,shell}/tasks/main.yml

`repos` enables multilib and any extra repos the distro file declares. `aur_helper` builds `paru`
as `target_user`, guarded by `creates: /usr/bin/paru`. `base_packages` is the converge-path
counterpart of `base_install`. `external_drives` writes fstab entries from an inventory `mounts`
dict and does nothing when the key is absent. `shell` sets the user shell and stows shell config.

- Contract:
  - `aur_helper` completes before any role whose `package_source` has an `aur:` key

### [NEW] ansible/plays/03_desktop.yml

`become: true`, re-runnable, a no-op when `wm_choice: ~`. Includes `desktop_{{ wm_choice }}`
first, then the null-filtered component loop, then `theming` and `display_manager`.

### [NEW] ansible/roles/component_{bar,notification,screenshot,launcher,lock,idle,clipboard,portal}/tasks/main.yml

Install + `stow` per component; `component_lock` and `component_idle` additionally enable (never
start) their user units.

### [NEW] ansible/roles/{theming,display_manager}/tasks/main.yml

`theming` installs GTK/Qt theme, cursor, icons, fonts and stows `gtk-3.0`/`qt5ct`.
`display_manager` installs greetd/tuigreet, or is disabled with `~` (open question Q2).

### [NEW] ansible/plays/04_workflows.yml

`become: true`, re-runnable. Loops `modules` with the null filter and includes `workflow_<key>`.

### [NEW] ansible/roles/workflow_development/{defaults,tasks}/main.yml

- Contract:
  - `module_cli`, `module_gui`, and
    `module_defaults: "{{ module_cli | combine(module_gui if ui_mode == 'gui' else {}) }}"`
  - `module_gui` holds `vscode`

### [NEW] ansible/roles/workflow_ai/{defaults,tasks}/main.yml

- Contract:
  - `module_cli` holds `llamacpp`, `opencode`, `model_store`; `module_gui` is empty

### [NEW] ansible/roles/app_{git,neovim,vscode,docker,lang_toolchains}/{defaults,tasks}/main.yml

`app_git` templates `.gitconfig` from `app_params`. `app_neovim` installs neovim + ripgrep + fd
and stows `nvim`. `app_vscode` is reachable only when `ui_mode == 'gui'`, stows `settings.json`
and installs an `extensions` list. `app_docker` enables the service and adds the user to the
group, with a `rootless` param. `app_lang_toolchains` installs toolchains from an inventory dict.

### [NEW] ansible/roles/app_llamacpp/{defaults,tasks}/main.yml

Source build (decisions 2.7, 2.8).

- Contract:
  - `app_defaults` keys: `repo`, `version`, `src_dir`, `cmake_flags` (list), `jobs`
  - `cmake_flags` defaults to exactly: `-DCMAKE_BUILD_TYPE=Release`, `-DGGML_CUDA=ON`,
    `-DCMAKE_CUDA_ARCHITECTURES=89`, `-DGGML_CUDA_FA_ALL_QUANTS=ON`, `-DGGML_CUDA_F16=ON`,
    `-DGGML_NATIVE=ON`, `-DGGML_AVX512=ON`, `-DGGML_AVX512_VBMI=ON`, `-DGGML_AVX512_VNNI=ON`,
    `-DGGML_AVX512_BF16=ON`
  - both cmake `command:` tasks run only when `src.changed` or `build/bin/llama-cli` is missing
  - a header comment records that the build is machine-specific and never cache-shared

### [NEW] ansible/roles/app_opencode/{defaults,tasks}/main.yml

Installs `packages.app_opencode` (AUR `opencode-bin`) and stows `opencode`.

### [NEW] ansible/roles/ai_model_store/{defaults,tasks}/main.yml

- Contract:
  - default `model_dir: "/home/{{ target_user }}/.local/share/models"`, overridable in inventory
  - creates the directory owned by `target_user` and writes `/etc/profile.d/ai-models.sh`

### [NEW] ansible/plays/05_finalise.yml

`become: true`, re-runnable. Includes `user_services`, `default_target`, `summary`.

### [NEW] ansible/roles/{user_services,default_target,summary}/tasks/main.yml

`user_services` runs `loginctl enable-linger` and enables (never starts) registered user units.
`default_target` sets `graphical.target` when `ui_mode == 'gui'`, else `multi-user.target`.
`summary` dumps resolved `wm_choice`, `ui_mode`, active modules and active components.

### [NEW] ansible/site.yml

Imports the five plays and carries the four load-bearing orderings as a header comment:
`repos → aur_helper → aur packages`; `dotfiles → stow`; `desktop_<wm> → components`;
`user_create → any become_user`.

## 5. Task DAG

Every `Verify` runs on a Linux controller; none of them can run on this Windows workstation
(section 3 of spec 001). Commands use shell globs rather than numbered play filenames where the
expected marker is a digit, so the expectation can never match the command line itself.

### Task 1: The variable layer — `ui_mode`, inventory, package keys

- Target Files: [NEW] ansible/inventory/group_vars/all.yml, [MODIFY] ansible/inventory/hosts.yml, [MODIFY] ansible/inventory/group_vars/arch.yml
- Depends On: None
- Subtasks:
  - [x] 1.1 Write `all.yml` carrying only the `ui_mode` derivation.
    - Input: decision 2.1
    - Output: ansible/inventory/group_vars/all.yml
    - Verify: `grep -c 'ui_mode' ansible/inventory/group_vars/all.yml`
    - Expect: "1"
  - [x] 1.2 Confirm `all.yml` holds no distro vocabulary (the decision 2.2 restriction).
    - Input: output of 1.1
    - Output: reviewed all.yml
    - Verify: `grep -cE '^(packages|commands):' ansible/inventory/group_vars/all.yml | cat`
    - Expect: "0"
  - [x] 1.3 Write the `thispc` inventory entry with `wm_choice: hyprland` and the `modules` tree
        (`development: {vscode: {}, docker: ~}`, `ai: {llamacpp: {}, opencode: {}}`).
    - Input: decision 2.3; spec 001 decisions 2.1, 2.2
    - Output: ansible/inventory/hosts.yml
    - Verify: `ansible-inventory -i ansible/inventory/hosts.yml --host thispc | grep -c opencode`
    - Expect: "1"
  - [x] 1.4 Add the three new package keys to `arch.yml`.
    - Input: decision 2.9; spec 001 decision 2.8
    - Output: `packages.app_llamacpp`, `packages.app_opencode`, `packages.app_vscode`
    - Verify: `grep -cE '^    app_(llamacpp|opencode|vscode):' ansible/inventory/group_vars/arch.yml`
    - Expect: "3"
- Phase Gate: `ansible-inventory -i ansible/inventory/hosts.yml --host thispc | grep ui_mode`

### Task 2: Play 01 — bootstrap_arch and its six sub-roles

- Target Files: [NEW] ansible/plays/01_bootstrap.yml, [NEW] ansible/roles/bootstrap_arch/tasks/main.yml, [NEW] ansible/roles/{disk_partition,base_install,system_identity,user_create,bootloader,initial_network}/tasks/main.yml
- Depends On: Task 1
- Subtasks:
  - [x] 2.1 Write the six sub-roles.
    - Input: decision 2.6
    - Output: six roles under ansible/roles/
    - Verify: `ls -d ansible/roles/{disk_partition,base_install,system_identity,user_create,bootloader,initial_network} | wc -l`
    - Expect: "6"
  - [x] 2.2 Write `bootstrap_arch` as an orchestrator including them in order.
    - Input: output of 2.1
    - Output: roles/bootstrap_arch/tasks/main.yml
    - Verify: `grep -c 'include_role' ansible/roles/bootstrap_arch/tasks/main.yml`
    - Expect: "6"
  - [x] 2.3 Register `target_uid` in `user_create`.
    - Input: the `become_user` ordering constraint
    - Output: roles/user_create/tasks/main.yml
    - Verify: `grep -c getent ansible/roles/user_create/tasks/main.yml`
    - Expect: "1"
  - [x] 2.4 Write the play; it dispatches `bootstrap_{{ distro }}` and carries no `become`.
    - Input: spec 001 decision 2.13
    - Output: ansible/plays/01_bootstrap.yml
    - Verify: `grep -cE 'become' ansible/plays/*bootstrap*.yml | cat`
    - Expect: "0"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/*bootstrap*.yml --syntax-check`

### Task 3: Play 02 — system roles

- Target Files: [NEW] ansible/plays/02_system.yml, [NEW] ansible/roles/{repos,aur_helper,base_packages,gpu,audio,network,firewall,ssh,snapshots,external_drives,dotfiles,shell}/tasks/main.yml
- Depends On: Task 2
- Subtasks:
  - [x] 3.1 Write the twelve system roles.
    - Input: section 4; spec 001 decisions 2.8, 2.18
    - Output: twelve roles under ansible/roles/
    - Verify: `ls -d ansible/roles/{repos,aur_helper,base_packages,gpu,audio,network,firewall,ssh,snapshots,external_drives,dotfiles,shell} | wc -l`
    - Expect: "12"
  - [x] 3.2 Guard the `paru` build so it is a no-op once installed.
    - Input: decision on ordering (`repos` → `aur_helper` → aur packages)
    - Output: roles/aur_helper/tasks/main.yml
    - Verify: `grep -c 'creates:' ansible/roles/aur_helper/tasks/main.yml`
    - Expect: "1"
  - [x] 3.3 Write the play with `repos` ahead of `aur_helper`.
    - Input: output of 3.1
    - Output: ansible/plays/02_system.yml
    - Verify: `awk '/repos/{r=NR} /aur_helper/{a=NR} END{print (r<a)}' ansible/plays/*system*.yml`
    - Expect: "1"
  - [x] 3.4 Make `external_drives` a no-op when the inventory has no `mounts` key.
    - Input: spec 001 decision 2.2
    - Output: roles/external_drives/tasks/main.yml
    - Verify: `grep -c 'mounts | default({})' ansible/roles/external_drives/tasks/main.yml`
    - Expect: "1"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/*system*.yml --syntax-check`

### Task 4: Play 03 — Hyprland desktop and components

- Target Files: [NEW] ansible/plays/03_desktop.yml, [NEW] ansible/roles/desktop_hyprland/{defaults,tasks}/main.yml, [NEW] ansible/roles/component_{bar,notification,screenshot,launcher,lock,idle,clipboard,portal}/tasks/main.yml, [NEW] ansible/roles/{theming,display_manager}/tasks/main.yml
- Depends On: Task 3
- Subtasks:
  - [x] 4.1 Write the eight component roles.
    - Input: section 4
    - Output: eight component roles
    - Verify: `ls -d ansible/roles/component_* | wc -l`
    - Expect: "8"
  - [x] 4.2 Write `desktop_hyprland` with the profile/overrides pair.
    - Input: spec 001 decision 2.7
    - Output: roles/desktop_hyprland/defaults/main.yml
    - Verify: `grep -c 'desktop_profile | combine(desktop_overrides' ansible/roles/desktop_hyprland/defaults/main.yml`
    - Expect: "1"
  - [x] 4.3 Write `theming` and `display_manager` (Q2 decides the latter's variant).
    - Input: open question Q2
    - Output: two roles
    - Verify: `ls -d ansible/roles/theming ansible/roles/display_manager | wc -l`
    - Expect: "2"
  - [x] 4.4 Write the play: desktop include first, then the null-filtered component loop.
    - Input: spec 001 decisions 2.3, 2.12
    - Output: ansible/plays/03_desktop.yml
    - Verify: `grep -c "rejectattr('value','none')" ansible/plays/*desktop*.yml`
    - Expect: "1"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/*desktop*.yml --syntax-check`

### Task 5: Play 04 part one — workflow_development

- Target Files: [NEW] ansible/plays/04_workflows.yml, [NEW] ansible/roles/workflow_development/{defaults,tasks}/main.yml, [NEW] ansible/roles/app_{git,neovim,vscode,docker,lang_toolchains}/{defaults,tasks}/main.yml
- Depends On: Task 3
- Subtasks:
  - [ ] 5.1 Write the roster split in `workflow_development/defaults`.
    - Input: decision 2.3
    - Output: `module_cli`, `module_gui`, `module_defaults`
    - Verify: `grep -c "module_gui if ui_mode == 'gui'" ansible/roles/workflow_development/defaults/main.yml`
    - Expect: "1"
  - [ ] 5.2 Place `vscode` in `module_gui` only.
    - Input: output of 5.1
    - Output: reviewed defaults/main.yml
    - Verify: `awk '/module_gui:/{f=1} /module_defaults:/{f=0} f' ansible/roles/workflow_development/defaults/main.yml | grep -c vscode`
    - Expect: "1"
  - [ ] 5.3 Write the five development app roles.
    - Input: section 4
    - Output: five app roles
    - Verify: `ls -d ansible/roles/app_{git,neovim,vscode,docker,lang_toolchains} | wc -l`
    - Expect: "5"
  - [ ] 5.4 Confirm no task anywhere gates on `ui_mode` with a conditional.
    - Input: decision 2.3
    - Output: audit result
    - Verify: `grep -rl 'when: ui_mode' ansible/roles | wc -l`
    - Expect: "0"
- Phase Gate: `ansible-lint ansible/roles/workflow_development ansible/roles/app_vscode`

### Task 6: Play 04 part two — workflow_ai

- Target Files: [NEW] ansible/roles/workflow_ai/{defaults,tasks}/main.yml, [NEW] ansible/roles/app_llamacpp/{defaults,tasks}/main.yml, [NEW] ansible/roles/app_opencode/{defaults,tasks}/main.yml, [NEW] ansible/roles/ai_model_store/{defaults,tasks}/main.yml
- Depends On: Task 5
- Subtasks:
  - [ ] 6.1 Write `app_llamacpp/defaults` with the flag list.
    - Input: decision 2.8; the user-supplied flags
    - Output: `cmake_flags` list
    - Verify: `grep -cE '^ +- -D' ansible/roles/app_llamacpp/defaults/main.yml`
    - Expect: "10"
  - [ ] 6.2 Confirm the CUDA-specific flags survived verbatim.
    - Input: output of 6.1
    - Output: reviewed defaults
    - Verify: `grep -cE 'GGML_CUDA=ON|CUDA_ARCHITECTURES=89|AVX512_BF16=ON' ansible/roles/app_llamacpp/defaults/main.yml`
    - Expect: "3"
  - [ ] 6.3 Guard both cmake calls on `src.changed` or a missing artifact.
    - Input: decision 2.7
    - Output: roles/app_llamacpp/tasks/main.yml
    - Verify: `grep -c 'src.changed' ansible/roles/app_llamacpp/tasks/main.yml`
    - Expect: "2"
  - [ ] 6.4 Write `app_opencode` installing the AUR binary package.
    - Input: decision 2.9
    - Output: roles/app_opencode/, arch.yml key
    - Verify: `grep -c 'opencode-bin' ansible/inventory/group_vars/arch.yml`
    - Expect: "1"
  - [ ] 6.5 Write `ai_model_store` owning `model_dir` and the profile.d export.
    - Input: decision 2.10; open question Q1
    - Output: roles/ai_model_store/
    - Verify: `grep -c 'profile.d/ai-models.sh' ansible/roles/ai_model_store/tasks/main.yml`
    - Expect: "1"
  - [ ] 6.6 Confirm no other role hardcodes a models path.
    - Input: decision 2.10
    - Output: audit result
    - Verify: `grep -rl 'share/models' ansible/roles | wc -l`
    - Expect: "1"
- Phase Gate: `ansible-lint ansible/roles/workflow_ai ansible/roles/app_llamacpp ansible/roles/app_opencode ansible/roles/ai_model_store`

### Task 7: Play 05 — finalise

- Target Files: [NEW] ansible/plays/05_finalise.yml, [NEW] ansible/roles/{user_services,default_target,summary}/tasks/main.yml
- Depends On: Task 6
- Subtasks:
  - [ ] 7.1 Write the three finalise roles.
    - Input: decision 2.5
    - Output: three roles
    - Verify: `ls -d ansible/roles/{user_services,default_target,summary} | wc -l`
    - Expect: "3"
  - [ ] 7.2 Confirm user units are enabled and never started.
    - Input: spec 001 decision 2.15
    - Output: roles/user_services/tasks/main.yml
    - Verify: `grep -c 'state: started' ansible/roles/user_services/tasks/main.yml | cat`
    - Expect: "0"
  - [ ] 7.3 Select the default systemd target from `ui_mode`.
    - Input: decision 2.1
    - Output: roles/default_target/tasks/main.yml
    - Verify: `grep -c 'graphical.target' ansible/roles/default_target/tasks/main.yml`
    - Expect: "1"
  - [ ] 7.4 Write the play.
    - Input: outputs of 7.1-7.3
    - Output: ansible/plays/05_finalise.yml
    - Verify: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/*finalise*.yml --syntax-check | grep -c ERROR | cat`
    - Expect: "0"
- Phase Gate: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/*finalise*.yml --syntax-check`

### Task 8: site.yml, ordering contract and docs

- Target Files: [NEW] ansible/site.yml, [NEW] ansible/README.md, [MODIFY] AGENTS.md
- Depends On: Task 7
- Subtasks:
  - [ ] 8.1 Write `site.yml` importing all five plays.
    - Input: decision 2.5
    - Output: ansible/site.yml
    - Verify: `grep -c 'import_playbook' ansible/site.yml`
    - Expect: "5"
  - [ ] 8.2 Record the four load-bearing orderings as header comments.
    - Input: section 4
    - Output: ansible/site.yml header
    - Verify: `grep -c '^# order:' ansible/site.yml`
    - Expect: "4"
  - [ ] 8.3 Document the five-play structure and the `ui_mode` contract.
    - Input: sections 1-4
    - Output: ansible/README.md, AGENTS.md
    - Verify: `grep -c '05_finalise' ansible/README.md`
    - Expect: "1"
- Phase Gate: `ansible-lint ansible/ && for p in ansible/plays/*.yml; do ansible-playbook -i ansible/inventory/hosts.yml "$p" --syntax-check; done`

### Completion rules

- State lives on subtasks: `[ ]` pending → `[/]` in progress → `[x]` done.
- A subtask is `[x]` only when Verify exits 0 AND the output matches Expect; evidence recorded in
  `docs/temp/verify-state.json`. Exit 0 alone is never enough.
- Before marking `[x]`, run the four passes: implement, expert re-read, defect hunt, polish.
- An impossible subtask is never deleted: it gets `ABANDON: <non-empty reason>`, never `[x]`.
- A task is done only when every subtask is `[x]` AND its Phase Gate is green.
- The spec is done only when a fresh re-run of every Phase Gate is green.

## 6. Verification Commands

- Build Command: `for p in ansible/plays/*.yml; do ansible-playbook -i ansible/inventory/hosts.yml "$p" --syntax-check; done`
- Test Command: `ansible-playbook -i ansible/inventory/hosts.yml ansible/plays/02_system.yml --check`
- Lint Command: `ansible-lint ansible/`

## 7. Rollback Strategy

Revert edits in reverse Task DAG order: Task 8 (site.yml/docs) → Task 7 (play 05) → Task 6
(workflow_ai) → Task 5 (workflow_development) → Task 4 (play 03) → Task 3 (play 02) → Task 2
(play 01) → Task 1 (variable layer). Everything except the two `[MODIFY]` files is additive, so
`git rm -r ansible/plays ansible/roles ansible/site.yml ansible/inventory/group_vars/all.yml && git checkout -- ansible/inventory/hosts.yml ansible/inventory/group_vars/arch.yml`
restores the pre-spec tree. If any subtask fails verification 3 consecutive times the circuit
breaker fires (`docs/temp/escalation.md`), dirty edits are reverted and the subtask reverts to
`[ ]`.
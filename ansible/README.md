# Ansible provisioning tree

Declarative, re-runnable provisioner for this machine (Arch + Hyprland, a
`development` workflow, and an `ai` workflow). The pattern and its decisions
live in `docs/specs/001-…` and `docs/specs/002-…`; this file is the operator's
map of the tree and the `ui_mode` contract.

## Layout

- `site.yml` — full converge entrypoint; imports the five plays in order and
  carries the four load-bearing orderings as a header comment.
- `plays/` — five thin hand-written plays that loop and `include_role`.
- `roles/` — the module set. Role names are prefix-encoded archetypes
  (`bootstrap_*`, `app_*`, `component_*`, `workflow_*`, …); one shared
  `install_packages` role dispatches by package-manager filename.
- `inventory/hosts.yml` — one host, distro as the group name.
- `inventory/group_vars/arch.yml` — distro vocabulary: `packages.<role>` keyed
  by manager.
- `inventory/group_vars/all.yml` — cross-distro **derivations only** (currently
  just `ui_mode`); no packages, no distro or machine facts.

## The five plays

| Play | Name | Re-runnable | Purpose |
| :--- | :--- | :--- | :--- |
| `01_bootstrap.yml` | Bootstrap | no | Live-ISO install: no `become` (already root), includes `bootstrap_{{ distro }}`. |
| `02_system.yml` | System | yes | `become: true`. `repos → aur_helper → base_packages → gpu → audio → network → firewall → ssh → snapshots → external_drives → dotfiles → shell`. |
| `03_desktop.yml` | Desktop | yes | `become: true`. No-op when `wm_choice: ~`. `desktop_{{ wm_choice }}` first, then the null-filtered component loop, then `theming` and `display_manager`. |
| `04_workflows.yml` | Workflows | yes | `become: true`. Loops `modules` (null-filtered) and includes `workflow_<key>`. |
| `05_finalise.yml` | Finalise | yes | `become: true`. `user_services → default_target → summary`. Reboot-adjacent, whole-machine work that runs after every module. |

Run the whole thing: `ansible-playbook -i inventory/hosts.yml site.yml`.
Run a single play by path, e.g. `ansible-playbook -i inventory/hosts.yml plays/02_system.yml`.

## The `ui_mode` contract

`ui_mode` is a **derived** single-select (`cli` | `gui`), not a boolean, and the
only key in `group_vars/all.yml`:

```yaml
ui_mode: "{{ 'gui' if (wm_choice | default(None)) is not none else 'cli' }}"
```

Consequences, enforced without a single `when: ui_mode` on any task:

- **Desktop-only apps are gated at the roster.** Each `workflow_*` role splits
  its roster into `module_cli` and `module_gui`, and combines them as
  `module_cli | combine(module_gui if ui_mode == 'gui' else {})`. A desktop-only
  app (e.g. `vscode` in `module_gui`) simply does not exist on a `cli` box —
  the include loop never sees it.
- **Apps with both forms are gated at the package key.**
  `packages.<role>: {cli: {…}, gui: {…}}` is consumed as
  `packages.<role>[ui_mode]`.
- **The default target follows `ui_mode`.** `default_target` boots to
  `graphical.target` when `gui`, else `multi-user.target`.
- **A headless box can never install a GUI app**, even deliberately — there is
  no override key; `ui_mode` is derived from `wm_choice` (spec 002 decision 2.1).

The `module_defaults` / `module_cli` / `module_gui` names are load-bearing
(spec 002 section 4 contract and the Task 5/6 audit greps); `module_defaults`
is an Ansible reserved name, so `workflow_development/defaults` and
`workflow_ai/defaults` are linted as plain yaml via the `kinds:` waiver in
`.ansible-lint`.

## AUR helper selection

`aur_variant` (`paru` | `yay` | `~`) is a single-select inventory key, the same
vocabulary as the other `*_variant` keys (ADR-018). The `aur_helper` role
dispatches by filename; the install side invokes the helper by its variant
name. `~` skips the role in play 02.

## Load-bearing orderings

Recorded as a header comment in `site.yml`; the plays depend on them:

1. `repos → aur_helper → aur packages`
2. `dotfiles → stow`
3. `desktop_<wm> → components`
4. `user_create → any become_user`

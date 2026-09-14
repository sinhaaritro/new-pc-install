# Decisions

Architectural Decision Records (ADRs). Naming: `adr-<NNN>-<topic>.md`
(e.g. `adr-001-database-selection.md`). Flat — ADRs never nest; nesting is
expressed by the backlink graph (`Source:` points at the spec, optional
`Governed-by:` points at a reference doc).

Protected files: ADRs in this directory must not be edited or deleted without
explicit human confirmation.

Every ADR carries `tags: [lowercase-kebab, ...]`.

<!-- TOC:START -->
## Index
- 📁 decisions/
  - 📄 [adr-001-adr-nnn-presence-over-flags.md](./adr-001-adr-nnn-presence-over-flags.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-002-adr-nnn-the-null-sentinel-is-the-only-subtraction-operator.md](./adr-002-adr-nnn-the-null-sentinel-is-the-only-subtraction-operator.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-003-adr-nnn-every-merged-dict-loop-ends-in-rejectattr-value-none.md](./adr-003-adr-nnn-every-merged-dict-loop-ends-in-rejectattr-value-none.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-004-adr-nnn-four-variable-layers-on-ansible-s-native-precedence.md](./adr-004-adr-nnn-four-variable-layers-on-ansible-s-native-precedence.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-005-adr-nnn-one-inventory-file-one-host-distro-as-the-group-name.md](./adr-005-adr-nnn-one-inventory-file-one-host-distro-as-the-group-name.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-006-adr-nnn-distro-var-files-are-self-contained-with-no-shared-all-yml.md](./adr-006-adr-nnn-distro-var-files-are-self-contained-with-no-shared-all-yml.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-007-adr-nnn-the-two-variable-trick-x-defaults-x-overrides-x.md](./adr-007-adr-nnn-the-two-variable-trick-x-defaults-x-overrides-x.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-008-adr-nnn-package-keys-are-named-after-roles-values-keyed-by-manager.md](./adr-008-adr-nnn-package-keys-are-named-after-roles-values-keyed-by-manager.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-009-adr-nnn-one-shared-installer-dispatching-by-manager-filename.md](./adr-009-adr-nnn-one-shared-installer-dispatching-by-manager-filename.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-010-adr-nnn-real-modules-over-command-with-a-named-escape-hatch.md](./adr-010-adr-nnn-real-modules-over-command-with-a-named-escape-hatch.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-011-adr-nnn-four-role-archetypes-with-prefix-encoded-names.md](./adr-011-adr-nnn-four-role-archetypes-with-prefix-encoded-names.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-012-adr-nnn-four-thin-hand-written-plays-that-loop-and-include.md](./adr-012-adr-nnn-four-thin-hand-written-plays-that-loop-and-include.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-013-adr-nnn-play-01-is-the-only-non-re-runnable-distro-branching-play.md](./adr-013-adr-nnn-play-01-is-the-only-non-re-runnable-distro-branching-play.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-014-adr-nnn-dotfiles-are-a-git-clone-plus-stow-r-per-package.md](./adr-014-adr-nnn-dotfiles-are-a-git-clone-plus-stow-r-per-package.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-015-adr-nnn-user-scope-services-are-enabled-never-started.md](./adr-015-adr-nnn-user-scope-services-are-enabled-never-started.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-016-adr-nnn-a-bootstrap-sh-carries-the-live-iso-preamble.md](./adr-016-adr-nnn-a-bootstrap-sh-carries-the-live-iso-preamble.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-017-adr-nnn-greenfield-rebuild-the-old-tree-is-ignored-entirely.md](./adr-017-adr-nnn-greenfield-rebuild-the-old-tree-is-ignored-entirely.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-018-adr-nnn-mutually-exclusive-implementations-are-inventory-selected-variants.md](./adr-018-adr-nnn-mutually-exclusive-implementations-are-inventory-selected-variants.md) — Accepted — backlinks: docs/specs/001-declarative-ansible-provisioning-tree-the-pattern.md
  - 📄 [adr-019-adr-nnn-ui-mode-is-a-derived-single-select-never-a-boolean.md](./adr-019-adr-nnn-ui-mode-is-a-derived-single-select-never-a-boolean.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-020-adr-nnn-group-vars-all-yml-exists-for-cross-distro-derivations-only.md](./adr-020-adr-nnn-group-vars-all-yml-exists-for-cross-distro-derivations-only.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-021-adr-nnn-desktop-only-apps-are-gated-at-the-roster-never-with-when.md](./adr-021-adr-nnn-desktop-only-apps-are-gated-at-the-roster-never-with-when.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-022-adr-nnn-dual-form-apps-select-their-package-list-by-ui-mode.md](./adr-022-adr-nnn-dual-form-apps-select-their-package-list-by-ui-mode.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-023-adr-nnn-five-plays-05-finalise-is-split-out-of-the-workflow-play.md](./adr-023-adr-nnn-five-plays-05-finalise-is-split-out-of-the-workflow-play.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-024-adr-nnn-bootstrap-arch-is-an-orchestrator-over-six-ordered-sub-roles.md](./adr-024-adr-nnn-bootstrap-arch-is-an-orchestrator-over-six-ordered-sub-roles.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-025-adr-nnn-source-built-apps-are-a-guarded-command-escape-hatch.md](./adr-025-adr-nnn-source-built-apps-are-a-guarded-command-escape-hatch.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-026-adr-nnn-cmake-flags-are-a-yaml-list-in-role-defaults.md](./adr-026-adr-nnn-cmake-flags-are-a-yaml-list-in-role-defaults.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-027-adr-nnn-prefer-the-prebuilt-aur-package-where-upstream-ships-one.md](./adr-027-adr-nnn-prefer-the-prebuilt-aur-package-where-upstream-ships-one.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
  - 📄 [adr-028-adr-nnn-model-storage-is-one-key-owned-by-ai-model-store.md](./adr-028-adr-nnn-model-storage-is-one-key-owned-by-ai-model-store.md) — Accepted — backlinks: docs/specs/002-plays-and-roles-current-target-arch-hyprland-dev-ai.md
<!-- TOC:END -->

<!-- TAG-INDEX:START -->
<!-- TAG-INDEX:END -->

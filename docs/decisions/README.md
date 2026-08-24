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
  - 📄 [adr-001-ansible-domain-layout-manifest-as-single-source-of-truth.md](./adr-001-ansible-domain-layout-manifest-as-single-source-of-truth.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-002-distro-abstraction-as-data-option-a.md](./adr-002-distro-abstraction-as-data-option-a.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-003-drive-selection-model-store-all-target-selected.md](./adr-003-drive-selection-model-store-all-target-selected.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-004-two-stage-install-pattern-live-usb-host-chroot-target.md](./adr-004-two-stage-install-pattern-live-usb-host-chroot-target.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-005-phase-0-as-a-verification-gate-not-an-action.md](./adr-005-phase-0-as-a-verification-gate-not-an-action.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-006-verification-harness-lint-syntax-check-parity-manual-bring-up-no-ci.md](./adr-006-verification-harness-lint-syntax-check-parity-manual-bring-up-no-ci.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-007-var-layering-inventory-for-per-machine-values-group-vars-for-static-shared-vars-distros-for-distro-data.md](./adr-007-var-layering-inventory-for-per-machine-values-group-vars-for-static-shared-vars-distros-for-distro-data.md) — Accepted — backlinks: docs/specs/002-var-dedup-layering-single-source-of-truth-for-play-1-variables.md
  - 📄 [adr-008-play-2-uses-a-single-play-with-become-based-context-split.md](./adr-008-play-2-uses-a-single-play-with-become-based-context-split.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-009-per-module-selectability-via-inventory-flag-plus-ansible-tag.md](./adr-009-per-module-selectability-via-inventory-flag-plus-ansible-tag.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-010-gpu-module-is-vendor-agnostic-and-expandable.md](./adr-010-gpu-module-is-vendor-agnostic-and-expandable.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-011-interactive-steps-become-explicit-gates-and-printed-artifacts.md](./adr-011-interactive-steps-become-explicit-gates-and-printed-artifacts.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-012-parity-checker-extends-to-phase-2.md](./adr-012-parity-checker-extends-to-phase-2.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-013-reuse-play-1-s-verification-harness-for-play-2.md](./adr-013-reuse-play-1-s-verification-harness-for-play-2.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-014-play-3-writes-no-user-dotfiles-stow-owns-config.md](./adr-014-play-3-writes-no-user-dotfiles-stow-owns-config.md) — Accepted — backlinks: docs/specs/005-ansible-play-3-phase-3-desktop-boot-system-selectable-modules-config-free.md
  - 📄 [adr-015-play-4-profile-vars-fold-into-per-module-enable-flags-in-pre-tasks.md](./adr-015-play-4-profile-vars-fold-into-per-module-enable-flags-in-pre-tasks.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-016-play-4-writes-system-level-non-dotfile-artifacts-but-never-user-dotfiles-adr-014-extension.md](./adr-016-play-4-writes-system-level-non-dotfile-artifacts-but-never-user-dotfiles-adr-014-extension.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-017-placeholder-phase-4-modules-get-thin-manifest-driven-roles.md](./adr-017-placeholder-phase-4-modules-get-thin-manifest-driven-roles.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-018-play-4-aur-installs-reuse-the-phase-2-yay-binary-with-a-presence-gate.md](./adr-018-play-4-aur-installs-reuse-the-phase-2-yay-binary-with-a-presence-gate.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-019-ai-model-downloads-are-flag-gated-and-resume-safe.md](./adr-019-ai-model-downloads-are-flag-gated-and-resume-safe.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-020-parity-checker-gains-profile-aware-phase-4-support-with-flat-module-ids.md](./adr-020-parity-checker-gains-profile-aware-phase-4-support-with-flat-module-ids.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-021-play-4-reuses-the-play-3-pre-tasks-gate-and-the-sudo-u-user-context-wrapper.md](./adr-021-play-4-reuses-the-play-3-pre-tasks-gate-and-the-sudo-u-user-context-wrapper.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-022-play-4-reuses-the-play-1-3-verification-harness-with-no-new-infra.md](./adr-022-play-4-reuses-the-play-1-3-verification-harness-with-no-new-infra.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-023-the-shared-dotfiles-backup-role-bootstraps-stow-and-the-dotfiles-git-repo-idempotently-without-adopting-configs.md](./adr-023-the-shared-dotfiles-backup-role-bootstraps-stow-and-the-dotfiles-git-repo-idempotently-without-adopting-configs.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
<!-- TOC:END -->

<!-- TAG-INDEX:START -->
<!-- TAG-INDEX:END -->

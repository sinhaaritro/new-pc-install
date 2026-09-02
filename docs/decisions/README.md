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
  - 📄 [adr-002-distro-data-single-source-of-truth-var-layering-variant-module-pattern-inventory-group-selection.md](./adr-002-distro-data-single-source-of-truth-var-layering-variant-module-pattern-inventory-group-selection.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-003-drive-selection-model-store-all-target-selected.md](./adr-003-drive-selection-model-store-all-target-selected.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-004-gpu-module-is-vendor-agnostic-and-expandable.md](./adr-004-gpu-module-is-vendor-agnostic-and-expandable.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-004-play-execution-model-live-usb-two-stage-install-single-play-with-become-split-on-the-booted-system.md](./adr-004-play-execution-model-live-usb-two-stage-install-single-play-with-become-split-on-the-booted-system.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-005-interactive-steps-become-explicit-gates-and-printed-artifacts.md](./adr-005-interactive-steps-become-explicit-gates-and-printed-artifacts.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-005-phase-0-as-a-verification-gate-not-an-action.md](./adr-005-phase-0-as-a-verification-gate-not-an-action.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-006-verification-harness-lint-syntax-check-parity-manual-bring-up-no-ci.md](./adr-006-verification-harness-lint-syntax-check-parity-manual-bring-up-no-ci.md) — Accepted — backlinks: docs/specs/001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md
  - 📄 [adr-007-placeholder-phase-4-modules-get-thin-manifest-driven-roles.md](./adr-007-placeholder-phase-4-modules-get-thin-manifest-driven-roles.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-008-play-4-aur-installs-reuse-the-phase-2-yay-binary-with-a-presence-gate.md](./adr-008-play-4-aur-installs-reuse-the-phase-2-yay-binary-with-a-presence-gate.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-009-ai-model-downloads-are-flag-gated-and-resume-safe.md](./adr-009-ai-model-downloads-are-flag-gated-and-resume-safe.md) — Accepted — backlinks: docs/specs/006-ansible-play-4-phase-4-workflow-booted-system-profile-selectable-modules-system-level-only.md
  - 📄 [adr-010-per-module-selectability-inventory-flag-plus-ansible-tag-profile-vars-fold-into-flags.md](./adr-010-per-module-selectability-inventory-flag-plus-ansible-tag-profile-vars-fold-into-flags.md) — Accepted — backlinks: docs/specs/004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md
  - 📄 [adr-011-config-ownership-no-user-dotfiles-from-automation-named-system-artifact-exception-dotfiles-backup-bootstrap.md](./adr-011-config-ownership-no-user-dotfiles-from-automation-named-system-artifact-exception-dotfiles-backup-bootstrap.md) — Accepted — backlinks: docs/specs/005-ansible-play-3-phase-3-desktop-boot-system-selectable-modules-config-free.md
<!-- TOC:END -->

<!-- TAG-INDEX:START -->
<!-- TAG-INDEX:END -->

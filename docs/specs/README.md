# Specs

Permanent functional & technical specs. Promotion pipeline:

- Draft: `docs/temp/draft-plan.md` (gitignored)
- Acceptance: promoted to `docs/specs/<NNN>-<feature-slug>.md` and committed

Naming: `NNN-<feature-slug>.md` (e.g. `001-feature-spec.md`). Sub-documents use
sub-IDs that share the parent `NNN` prefix: `NNN-<letter><NN>` (e.g. `001-A01`),
deeper `NNN-<letter><NN>-<letter><NN>` (e.g. `001-A01-B01`). Parent and child
share the `NNN` so a worktree can claim the subtree.

Every spec carries `tags: [lowercase-kebab, ...]`; the promotion gate runs
`tag-lint` on them.

<!-- TOC:START -->
## Index
- 📁 specs/
  - 📄 [001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md](./001-ansible-play-1-live-usb-install-through-first-reboot-phase-0-1.md) — APPROVED
  - 📄 [002-var-dedup-layering-single-source-of-truth-for-play-1-variables.md](./002-var-dedup-layering-single-source-of-truth-for-play-1-variables.md) — APPROVED
  - 📄 [003-role-consolidation-selectable-layout-verify-boot-merge-fstype-conditional-checks-bootloader-pattern-password-flow.md](./003-role-consolidation-selectable-layout-verify-boot-merge-fstype-conditional-checks-bootloader-pattern-password-flow.md) — APPROVED
  - 📄 [004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md](./004-ansible-play-2-phase-2-system-hardening-boot-system-selectable-modules.md) — APPROVED
<!-- TOC:END -->

<!-- TAG-INDEX:START -->
<!-- TAG-INDEX:END -->

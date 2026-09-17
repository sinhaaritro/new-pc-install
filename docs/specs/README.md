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
  - 📄 [001-declarative-ansible-provisioning-tree-the-pattern.md](./001-declarative-ansible-provisioning-tree-the-pattern.md) — APPROVED
  - 📄 [002-plays-and-roles-current-target-arch-hyprland-dev-ai.md](./002-plays-and-roles-current-target-arch-hyprland-dev-ai.md) — APPROVED
  - 📄 [003-ansible-lint-remediation.md](./003-ansible-lint-remediation.md) — APPROVED
  - 📄 [004-ansible-lint-zero-finding-without-config-waivers.md](./004-ansible-lint-zero-finding-without-config-waivers.md) — APPROVED
  - 📄 [005-aur-helper-selection-as-an-inventory-selected-variant.md](./005-aur-helper-selection-as-an-inventory-selected-variant.md) — APPROVED
<!-- TOC:END -->

<!-- TAG-INDEX:START -->
<!-- TAG-INDEX:END -->

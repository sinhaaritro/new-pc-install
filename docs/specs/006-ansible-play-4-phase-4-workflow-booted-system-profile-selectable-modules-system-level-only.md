---
tags: [ansible, archlinux, phase-4, workflow, profiles, stow]
---

# [006]: Ansible Play 4 — Phase 4 Workflow (Booted System, Profile-Selectable Modules, System-Level Only)

Status: APPROVED
Handoff: 2026-08-24
Phase: 2-Build

## 1. Goal & Context

Build **Play 4** of the Ansible automation to run **on the booted Arch system**
(post Phase 3) and drive the **Phase 4: Workflow** modules
(`os/archlinux/phase-4-workflow/`). Play 4 installs the **packages,
user services, and system-level artifacts** for the 4 workflow profiles
(dev / ai / creative / gaming) plus the shared dotfiles-backup module.

**Scope = all 18 Phase 4 manifest modules + 1 shared**, across 4 profiles
(18 total roles). Of the 24 Phase 4 docs, **8 are implemented**
(`containers`, `devpod`, `remote-ssh` [dev]; `inference`, `harness`,
`ide-integration`, `agents` [ai]; `dotfiles-backup` [shared]) and **12 are
placeholders** (`neovim`, `languages`, `api-testing`, `training`, `steam`,
`proton`, `heroic`, `mangohud`, `controllers`, `obs`, `davinci`,
`media-players`). Per the resolved scope gate, implemented modules get full
automation; placeholder modules get **thin roles** that install only the
packages their manifest entry lists and print a "doc is a placeholder —
manual steps pending" note. The manifest is the single source of truth for
which placeholder modules carry packages.

**Config boundary (extension of ADR-014, resolved gate):** Play 4, like
Play 3, **writes no user dotfiles** — everything under `~/.config/`,
`~/.ssh/`, `~/.zshrc`, `~/.continue/`, `~/.config/claude/` etc. is owned by
the user's stow package (the Phase 4 `dotfiles-backup` module sets up that
repo). Where a module's docs describe a dotfile, the role prints a "your stow
package should provide X" note. Play 4 **does** write a small set of
**system-level, non-dotfile** artifacts (same exception class as Play 3's
`/etc/greetd/config.toml`):

1. `/usr/local/bin/devpod` — downloaded binary (root).
2. The end user's subuid/subgid range (`usermod --add-subuids/--add-subgids`,
   root) for rootless podman.
3. The `ufw allow 8080/tcp` rule (root) for LAN access to llama-server.
4. `~/.config/systemd/user/llama-server.service` — a **service unit
   definition**, not a config/dotfile (explicitly allowed by the resolved
   gate; created idempotently, and the role prints that the user may prefer
   stow to own it and delete it).

**Profile selectability (resolved gate):** every module role is gated by an
`enable_<id>` inventory boolean **and** carries its own Ansible tag (same
mechanics as spec 004 D2 / spec 005 D2). Four convenience profile vars
(`profile_dev`, `profile_ai`, `profile_creative`, `profile_gaming`) are
folded into the 18 flags in pre_tasks, so `profile_dev: true` selects the
whole dev profile while any single `enable_<id>` can still be flipped or a
single module run via `--tags`.

**Dependency reality (flagged, handled by gates not hard ordering):**
`harness` (npm globals) depends on Node.js, which lives in the placeholder
`languages.md`; the `harness` role therefore checks `node --version` and,
when absent, prints a "Node.js required — see profile-dev/languages.md
(placeholder)" note instead of failing. `ide-integration` depends on the
placeholder `neovim.md`; its role installs nothing but prints the stow note
for the plugin spec + a manual note for VSCodium extensions. `proton`
depends on `steam` (both placeholder-thin): no gate needed beyond docs.
`agents` depends on `inference` (llama-server + models): gated on
`enable_inference`.

**Why this differs from Plays 1–3:** Play 4 is the first play where the
module set is **profile-structured** (the manifest phase-4 entry has a
`profiles:` list instead of a flat `modules:` list), the first play that
installs **AUR packages** as a module concern (`llama-cpp-cuda`,
`lazydocker`, `claude-desktop` — the `yay` helper itself comes from Phase 2
module 03), the first play with **external data downloads** (devpod binary,
optional model GGUFs), and the first play that deliberately **defers** most
of its config to the stow repo being created by its own shared module.

## 2. Architectural Decisions & Trade-offs

- **D1 — Profile vars fold into per-module flags in pre_tasks (resolved
  gate; extension of spec 004 D2 / spec 005 D2).** Inventory carries 18
  `enable_<id>` flags **plus** 4 `profile_<name>` convenience booleans.
  Play 4 pre_tasks compute the effective flags:
  `enable_<id> = (enable_<id> | default(false)) or (profile_<profile> |
  default(false))`. Precedence: an explicit per-module flag in inventory
  wins over the profile var only in the sense that both are OR-ed (profile
  on = all modules on; a module off while its profile is on is *not*
  expressible — accepted trade-off, documented in the README; narrowing is
  done via `--tags` at run time). Alternative rejected: profile flags only
  (coarser; breaks the per-module `--tags` workflow) or module flags only
  (no ergonomics for "give me the whole dev profile"). The fold happens in
  pre_tasks with `set_fact`-style `vars` on the play via
  `ansible.builtin.set_fact` in a pre_task that registers the computed map,
  keeping the role `when:` clauses identical in shape to Play 3's.

- **D2 — System-level artifacts written, dotfiles never (extension of
  ADR-014, resolved gate).** The ADR-014 boundary ("no user dotfiles; stow
  owns config") is extended to Play 4 with one named exception class:
  **service unit definitions and root-owned system artifacts**. Play 4
  writes exactly four: the devpod binary (`/usr/local/bin`), the podman
  subuid/subgid range (a `/etc/subuid` entry via `usermod`), the ufw 8080
  rule, and the `llama-server.service` user unit file. All four are either
  root-owned, kernel/package state, or a service definition — none carry
  user preference content (the unit's model list comes from the user's
  stow-owned `~/models/config.ini`, referenced by path). Everything else in
  the Phase 4 docs — `~/.ssh/config`, `vscodium-tunnel-proxy.sh`,
  `~/.config/systemd/user/` *beyond* the unit, aliases,
  `opencode.json`, `~/.continue/config.yaml`,
  `~/.config/claude/claude_desktop_config.json`, neovim lazy.nvim specs,
  VSCodium settings — is a printed stow note. Alternative rejected: strict
  config-free (leaves llama-server impossible to enable as a service, which
  the inference doc's Path B explicitly wants) or writing configs (collides
  with stow, violates ADR-014).

- **D3 — Placeholder modules are thin manifest-driven roles (resolved
  scope gate).** A placeholder module's role contains: (a) install the
  packages listed in its **manifest entry** (the source of truth; e.g.
  `steam`, `mangohud`, `obs-studio`, `mpv`, `neovim`, `podman` — note
  `containers` is implemented so it owns `podman` fully), (b) no AUR/npm/
  binary steps (none are documented yet), (c) a debug note: "module X doc
  is a placeholder — package set is manifest-only; remaining manual steps
  are pending in os/archlinux/phase-4-workflow/...". This keeps the parity
  checker green (every manifest package is referenced) and the playbook
  useful today, while the docs get filled in later without a playbook
  redesign. Alternative rejected: skip placeholders entirely (parity
  checker would need a whitelist; `make run-phase4` would not give a
  working gaming/creative baseline) or guess package sets from README
  hints (drift risk; the manifest is the contract).

- **D4 — AUR installs reuse the Phase 2 `aur` role's `yay` and follow its
  build pattern.** Phase 4 roles that need AUR packages (`inference` →
  `llama-cpp-cuda`; `containers` → `lazydocker`; `agents` →
  `claude-desktop`) gate on the `yay` binary existing (`which yay`,
  registered in a pre_task; absent = clear "run Play 2 with
  enable_aur: true first" failure, no silent skip). The `claude-desktop`
  AUR build is flaky upstream (the doc itself says it may fall back to a
  manual AppImage), so the `agents` role tries `yay -S --noconfirm
  claude-desktop` and, on failure, **prints** the manual AppImage
  instructions and continues (module still "applied" with a warning, not a
  hard fail). Alternative rejected: a dedicated AUR helper role (yay is a
  plain binary; the `aur` role's pattern is already the house style).

- **D5 — Model downloads are flag-gated and resumable (resolved gate).**
  GGUF downloads (Hermes 8B for `agents`; the Gemma 4 / Ornith set for
  `inference`, per `~/models/config.ini` in the docs) are **not** run by
  default: they live in tasks gated on `enable_ai_models` (inventory
  boolean, default `false`) **and** the module's own flag. Downloads use
  `wget -c` (resume-safe) into `~/models/` as the end user (no root), with
  `creates:` guards per file so re-runs are no-ops. `inference` always
  creates `~/models/`; the `config.ini` master preset is **stow-owned**
  (printed note, not written) because it is user preference data.
  Alternative rejected: always-download (tens of GB on a flag nobody
  thought about) or skip models (leaves inference inoperable without
  hand-rolled curl commands).

- **D6 — Parity checker gains profile-aware Phase 4 support (extension of
  spec 005 D6).** `manifest_to_playbook.py` gets `phase-4` in `PHASE_IDS`
  and a profile-aware `load_modules` branch: when a phase entry has
  `profiles:`, the checker's `load_modules` iterates the nested
  `profiles[].modules[]` (phase-4 ids stay flat — they are unique across
  profiles in the manifest; the only id that would collide with the
  phase-3 namespace is `davinci`, so its role is named
  `creative_davinci_resolve` and the ROLE_MAP entry maps `davinci` →
  `creative_davinci_resolve`, mirroring how `gpu` already covers the
  phase-2 `nvidia` id). `ROLE_MAP` gains 19 Phase 4 entries (18 modules +
  `dotfiles-backup` → `dotfiles_backup` shared role). Package-reference
  checking is unchanged (it scans the whole ansible tree). Alternative
  rejected: namespaced ids (would force tag/flag renames and break the
  flat `enable_<id>` convention).

- **D7 — One play, `become`-based context split, Play 3 gates reused
  (same as spec 004 D1 / spec 005 D1).** Play 4 is a single play on
  `localhost` with play-level `become: true`. The pre_tasks gate (no live
  USB, invoking user in wheel, `end_user` exists) is copied from Play 3
  (it is identical in shape; kept as local tasks rather than extracted to a
  shared role — three plays is not yet enough to justify a shared gate
  role, and the failure messages differ per play). User-context commands
  (user systemd enables, `podman system migrate`, devpod provider config,
  npm installs, `~/models` downloads, `~/dotfiles` repo init) run via the
  `sudo -u {{ end_user }} env XDG_RUNTIME_DIR=/run/user/<uid> …` wrapper
  (sound role pattern, spec 004 D1) so the play works whether invoked by
  root or by the user.

- **D8 — No new verification infra; reuse the Play 1/2/3 harness (same as
  spec 005 D7).** Always-on checks stay `ansible-playbook --syntax-check`,
  `yamllint`, `ansible-lint`, and the parity check (now Phase 0–4,
  profile-aware). Acceptance is a documented manual bring-up: run Play 4
  with a chosen profile, then run each applied module's docs' verification
  command. No CI added.

- **D9 — Shared `dotfiles-backup` role: stow + git repo bootstrap,
  idempotent, config-free.** Installs `stow` (pacman, root); creates
  `~/dotfiles` as a git repo **only if it does not already exist** (never
  `git init` over an existing repo — the user may already have one); prints
  the naming convention (`[type]_[name]_[variant]`), the suggested stow
  package list from the doc, and the `stow --adopt` + `git checkout -- .`
  workflow. It writes **no** stow packages and moves **no** files (moving
  the user's existing configs into the repo is an interactive,
  user-judgment step — printed instructions only). Alternative rejected:
  auto-adopt existing configs (destructive to user state; exactly the kind
  of judgment ADR-014 assigns to the user).

## 3. Affected Files & Scope

- **Created:**
  - `ansible/playbooks/40-workflow.yml` — **Play 4**: pre_tasks gate (Play
    3 gates + profile-fold (D1) + `yay` presence check (D4)); 19 roles wired
    (18 modules + shared `dotfiles_backup`), each tagged + flag-gated;
    `agents` additionally gated on `enable_inference` (doc prerequisite).
  - `ansible/roles/dotfiles_backup/tasks/main.yml` — shared module
    `dotfiles-backup` (D9): stow install, `~/dotfiles` git bootstrap
    (idempotent), printed workflow.
  - `ansible/roles/dev_containers/tasks/main.yml` — module `containers`:
    `podman` (pacman), `lazydocker` (AUR, D4), subuid/subgid range (D2),
    `podman system migrate` (user ctx), `podman.socket` user service
    enable, lazypodman-alias stow note, verification prints.
  - `ansible/roles/dev_devpod/tasks/main.yml` — module `devpod`: binary
    download to `/usr/local/bin` (D2, `creates:`-guarded), `devpod provider
    add docker` + `set-options DOCKER_PATH=/usr/bin/podman` (user ctx,
    idempotent: check `devpod provider list` first), verification prints.
  - `ansible/roles/dev_remote_ssh/tasks/main.yml` — module `remote-ssh`:
    `openssh openbsd-netcat procps-ng` (pacman); stow notes for
    `~/.ssh/config` host blocks + `vscodium-tunnel-proxy.sh` (incl. the
    chmod 600/+x requirements); verification prints.
  - `ansible/roles/dev_neovim/tasks/main.yml` — **thin** (D3): install
    manifest package `neovim`; placeholder note + stow notes for
    lazy.nvim/LSP/treesitter.
  - `ansible/roles/dev_languages/tasks/main.yml` — **thin** (D3): no
    manifest packages; placeholder note listing intended runtimes
    (Python/uv, Go, Node, Java, Rust) and that `harness` needs Node.js.
  - `ansible/roles/dev_api_testing/tasks/main.yml` — **thin** (D3): no
    manifest packages; placeholder note (posting/curl/httpie per README
    index) — `curl` note only (already base-installed).
  - `ansible/roles/ai_inference/tasks/main.yml` — module `inference`:
    `cuda` (pacman), `llama-cpp-cuda` (AUR, D4); `~/models/` dir (user
    ctx, `creates:`); **flag-gated** model downloads (D5, `wget -c`,
    per-file `creates:`); llama-server user unit file (D2, template,
    idempotent, stow-may-own note); `systemctl --user daemon-reload` +
    `enable-linger` + `enable --now llama-server.service` (user ctx via
    wrapper); `ufw allow 8080/tcp` (root, idempotent check first); stow
    notes for `~/models/config.ini` + `llama-start`/`llm()` alias;
    verification prints.
  - `ansible/roles/ai_harness/tasks/main.yml` — module `harness`: Node.js
    presence check (gate, D1-context: missing → printed note, no fail);
    npm globals `kilocode`, `@anthropic-ai/claude-code`,
    `@google-gemini/gemini-cli` (doc's `@anthropic-ai/gemini-cli` scope
    corrected), `opencode` (pacman) — all user ctx via wrapper; stow notes
    for `opencode.json` + `aliases.zsh`; env-var manual notes (ANTHROPIC
    key, gemini auth, KILOCODE vars); verification prints.
  - `ansible/roles/ai_ide_integration/tasks/main.yml` — module
    `ide-integration`: **package-free**; stow notes for neovim lazy.nvim
    plugin spec (avante/codecompanion/copilot) +
    `~/.continue/config.yaml` + VSCodium `settings.json`; manual note for
    `codium --install-extension` (Open VSX); verification prints.
  - `ansible/roles/ai_agents/tasks/main.yml` — module `agents`:
    `claude-desktop` (AUR, D4 flaky-fallback print); Hermes 8B GGUF
    download (D5, flag-gated, user ctx, `creates:`); stow note for
    `~/.config/claude/claude_desktop_config.json`; npx-MCP manual note;
    verification prints. Gated on `enable_inference` (play level).
  - `ansible/roles/ai_training/tasks/main.yml` — **thin** (D3): no manifest
    packages; placeholder note (Unsloth/Axolotl/LLaMA-Factory/torchtune +
    pip deps per doc plan).
  - `ansible/roles/gaming_steam/tasks/main.yml` — **thin** (D3): manifest
    package `steam`; placeholder note (multilib client notes pending).
  - `ansible/roles/gaming_proton/tasks/main.yml` — **thin** (D3): no
    manifest packages; placeholder note (deps: steam).
  - `ansible/roles/gaming_heroic/tasks/main.yml` — **thin** (D3): no
    manifest packages; placeholder note (AUR `heroicgameslauncher` pending
    doc).
  - `ansible/roles/gaming_mangohud/tasks/main.yml` — **thin** (D3):
    manifest package `mangohud`; placeholder note.
  - `ansible/roles/gaming_controllers/tasks/main.yml` — **thin** (D3): no
    manifest packages; placeholder note.
  - `ansible/roles/creative_obs/tasks/main.yml` — **thin** (D3): manifest
    package `obs-studio`; placeholder note (portal/sound deps).
  - `ansible/roles/creative_davinci_resolve/tasks/main.yml` — module
    `davinci`, **thin** (D3; role name extended per D6 to avoid the
    phase-3 namespace collision): no manifest packages; placeholder note
    (manual .deb per doc).
  - `ansible/roles/creative_media_players/tasks/main.yml` — **thin** (D3):
    manifest package `mpv`; placeholder note (ncmpcpp/mpd pending doc).
  - `ansible/templates/llama-server.service.j2` — the user unit file (D2):
    `Type=simple`, `ExecStart=/usr/bin/llama-server --models-preset
    %h/models/config.ini --fit off --models-max 1`, `Restart=on-failure`,
    `RestartSec=10s`, `Environment=CUDA_VISIBLE_DEVICES={{
    inference_cuda_device | default(0) }}`, `WantedBy=default.target`.
    The **only** template Play 4 writes.

- **Modified:**
  - `ansible/inventory/hosts.yml` — Play 4 section: 4 `profile_*` vars
    (default: `profile_dev: true`, `profile_ai: true`, `profile_creative:
    false`, `profile_gaming: false` — README "pick one or more" with dev+ai
    as the sensible default for this repo), 18 `enable_<id>` flags (all
    default `false` — the profile vars drive selection; a user who wants
    per-module control sets `profile_*: false` and flips individual
    flags), `enable_ai_models: false` (D5), `inference_cuda_device: 0`
    (optional).
  - `ansible/vars/distros/archlinux.yml` — Phase 4 data: `phase4:` map with
    per-module pacman package lists (thin roles read their manifest-listed
    packages from here), AUR package lists (`inference: [llama-cpp-cuda]`,
    `containers: [lazydocker]`, `agents: [claude-desktop]`), npm global
    lists (`harness: [kilocode, @anthropic-ai/claude-code,
    @google-gemini/gemini-cli]` + `opencode_pacman: true`), and the model
    download URL map (Hermes 8B; Gemma 4 E2B/12B set; Ornith 35B set).
  - `ansible/generators/manifest_to_playbook.py` — `PHASE_IDS +=
    ("phase-4",)`; profile-aware `load_modules` (D6); `ROLE_MAP` +19
    entries (18 modules + `dotfiles-backup`).
  - `ansible/Makefile` — `run-phase4` target; `syntax` gains
    `40-workflow.yml`.
  - `ansible/README.md` — Play 4 user flow (post Phase 3, `make run-phase4`,
    profile vars vs per-module flags vs `--tags`, `enable_ai_models`
    opt-in, stow boundary + the four system-level exceptions, manual
    bring-up checklist).
  - `os/archlinux/phase-4-workflow/README.md` — pointer to the `ansible/`
    Play 4 automation companion (mirrors the Phase 0–3 pointers).

- **Deleted:** none

- **Out of scope (stow-owned, explicitly NOT written by Play 4):** every
  user dotfile — `~/.ssh/config`, `~/.ssh/vscodium-tunnel-proxy.sh`,
  `~/.config/systemd/user/llama-server.service` *if the user prefers stow
  ownership* (the role prints this), `~/models/config.ini`,
  `~/.config/claude/claude_desktop_config.json`, `opencode.json`,
  `~/.continue/config.yaml`, `~/.config/VSCodium/User/settings.json`,
  `~/.config/nvim/` (lazy.nvim specs), `~/.config/zsh/aliases.zsh`,
  `~/.zshrc`/`~/.bashrc` alias additions, and any stow package contents
  under `~/dotfiles/`.

## 4. Actionable TODO Checklist

- [x] Step 1: Extend `ansible/vars/distros/archlinux.yml` with the
      `phase4:` data map (per-module pacman/AUR/npm lists + model URL map,
      D4/D5 data).
- [x] Step 2: Add the Play 4 section to `ansible/inventory/hosts.yml`
      (4 profile vars + 18 `enable_<id>` flags + `enable_ai_models` +
      `inference_cuda_device`, with the commented selection semantics, D1).
- [x] Step 3: Create `ansible/templates/llama-server.service.j2` (D2 unit
      file).
- [x] Step 4: Implement `roles/dotfiles_backup` (shared, D9): stow install,
      idempotent `~/dotfiles` git bootstrap, printed workflow + naming
      convention.
- [x] Step 5: Implement `roles/dev_containers` (`containers`): podman +
      lazydocker(AUR) + subuid/subgid + migrate + podman.socket + stow
      alias note.
- [x] Step 6: Implement `roles/dev_devpod` (`devpod`): binary download
      (creates-guarded) + provider config (idempotent) + prints.
- [x] Step 7: Implement `roles/dev_remote_ssh` (`remote-ssh`): 3 pacman
      packages + stow notes for ssh config + proxy script.
- [x] Step 8: Implement the 3 thin dev roles (`dev_neovim`,
      `dev_languages`, `dev_api_testing`) per D3.
- [x] Step 9: Implement `roles/ai_inference`: cuda + llama-cpp-cuda(AUR) +
      models dir + flag-gated downloads + unit file (template) + daemon-
      reload/linger/enable + ufw 8080 + stow notes + prints.
- [x] Step 10: Implement `roles/ai_harness`: node gate + npm globals +
      opencode(pacman) + stow/env notes + prints.
- [x] Step 11: Implement `roles/ai_ide_integration` (package-free stow/
      manual notes) and `roles/ai_agents` (claude-desktop AUR fallback +
      flag-gated Hermes download + stow/MCP notes).
- [x] Step 12: Implement `roles/ai_training` thin role (D3).
- [x] Step 13: Implement the 5 thin gaming roles (`gaming_steam`,
      `gaming_proton`, `gaming_heroic`, `gaming_mangohud`,
      `gaming_controllers`) per D3.
- [x] Step 14: Implement the 3 thin creative roles (`creative_obs`,
      `creative_davinci_resolve`, `creative_media_players`) per D3.
- [x] Step 15: Create `ansible/playbooks/40-workflow.yml`: Play 3 gate
      pre_tasks + profile fold (D1) + yay presence check (D4); wire the 19
      roles with tags + flag gates (`agents` also gated on
      `enable_inference`).
- [x] Step 16: Extend `generators/manifest_to_playbook.py` (D6: phase-4 +
      profile-aware load + 19 ROLE_MAP entries); update `Makefile`
      (`run-phase4`, syntax check for 40-workflow.yml).
- [ ] Step 17: Update `ansible/README.md` (Play 4 flow, selection
      semantics, stow boundary + 4 exceptions, model opt-in, manual
      bring-up) + Phase 4 README pointer.
- [ ] Step 18: Run `make lint syntax check` (Phase 0–4 parity green,
      profile-aware) + `--list-tasks` selectability smoke (profile on/off,
      `--tags`, agents-gated-on-inference); document the manual bring-up.

## 5. Verification Commands

- Lint: `make lint` (yamllint + ansible-lint over playbooks/ + roles/)
- Syntax: `ansible-playbook --syntax-check playbooks/40-workflow.yml`
- Parity: `python3 generators/manifest_to_playbook.py --check --manifest
  ../os/archlinux/manifest.yaml` (now covers Phase 0–4 profile-aware: every
  Phase 4 module id has a role; every Phase 4 manifest package is
  referenced)
- Selectability smoke: `ansible-playbook playbooks/40-workflow.yml
  --list-tasks --tags ai-inference` shows only that role; a run with
  `profile_dev: false, enable_dev_podman: true` (hypothetical flag naming
  per final ids) selects a single module; `profile_gaming: true` lists all
  5 gaming roles.
- Prerequisite smoke: a run with `enable_inference: false` and
  `enable_agents: true` skips agents (play-level gate); a run without
  `yay` fails the pre_task with the "run Play 2 enable_aur" message.
- Model-gate smoke: default inventory (`enable_ai_models: false`) lists no
  download tasks; `enable_ai_models: true` lists them.
- Manual bring-up (real machine, post Phase 3): `make run-phase4` with a
  chosen profile, then per applied module run its docs' verification
  (e.g. `podman run --rm hello-world`, `devpod list`, `llama-server
  --version` + `curl :8080/v1/models`, `npm ls -g`, `stow --version`,
  `ls -la ~/dotfiles/.git`).

## 6. Rollback Strategy

Play 4 is additive; rollback is per-module package removal + (where
applied) service disable + artifact delete. Stow state is never touched
(no dotfiles written), so the user's dotfiles repo is unaffected.

- **dotfiles-backup:** `sudo pacman -Rns stow`; `rm -rf ~/dotfiles` only
  if Play 4 created it (the role refuses to touch an existing repo).
- **containers:** `sudo pacman -Rns podman`; `yay -Rns lazydocker`;
  `sudo usermod --del-subuids 100000-165535 --del-subgids 100000-165535
  <user>`; `sudo -u <user> systemctl --user disable --now podman.socket`.
- **devpod:** `sudo rm /usr/local/bin/devpod`.
- **remote-ssh:** `sudo pacman -Rns openbsd-netcat procps-ng` (leave
  openssh — Phase 2 owns it).
- **inference:** `sudo systemctl --user (wrapper) disable --now
  llama-server.service`; `rm ~/.config/systemd/user/llama-server.service`
  (if Play 4 wrote it); `sudo ufw delete allow 8080/tcp`;
  `sudo pacman -Rns cuda`; `yay -Rns llama-cpp-cuda`; `rm -rf ~/models`
  only if the user agrees (models are data).
- **harness:** `npm uninstall -g kilocode @anthropic-ai/claude-code
  @google-gemini/gemini-cli`; `sudo pacman -Rns opencode`.
- **agents:** `yay -Rns claude-desktop` (or remove the manual AppImage);
  delete the Hermes GGUF if Play 4 downloaded it.
- **thin roles:** `sudo pacman -Rns <that module's manifest package>`
  (neovim / steam / mangohud / obs-studio / mpv); the no-package thin
  roles have nothing to roll back.
- **play/infra files:** git revert (the playbook, roles, templates,
  inventory/vars/generator/Makefile edits are all committed artifacts).

If the parity checker or lint fails 3× on the same change, revert that
file to its pre-change state (git) and re-derive from the manifest — the
manifest is the source of truth, so a green `make check` is the recovery
target.

---
tags: [ansible, provisioning, arch-linux, comparison, implementation-audit]
---

# `ansible_bck/` vs specs 001/002 — where the implementation is better

Comparison of the approved specs (`docs/specs/001-*.md`, `docs/specs/002-*.md`, which describe the
new greenfield `ansible/` tree) against the existing implementation in `ansible_bck/`. This lists
the places where the **implementation does something the specs do not** (or more robustly), with
`file:line` evidence. Not a verdict on overall quality — the specs win on cleanliness/
extensibility/`--check`; section 9 is the honest inverse. Per request, this file is the
"implementation wins" side.

Legend: **[W]** = clear win · **[N]** = nuanced/trade-off · **[!]** = carries a caveat/defect.

---

## 1. Runtime safety gates (specs have none)

Every `ansible_bck` play asserts the *environment* before touching anything. The specs' plays have
no equivalent guards (spec 001's only guard is a "disk confirmation pause", `001` §4 line 282).

- **[W] Live-USB-only gate on the wipe play.** `playbooks/10-install.yml:9-23` — `stat /run/archiso`
  + `assert ...exists`; fail: "Do NOT run this play on your installed system — it will wipe the
  target drive."
- **[W] Installed-system-only gates on plays 2-4.** `20-hardening.yml:18-33`, `30-desktop.yml:17-32`,
  `40-workflow.yml:22-37` — assert `/run/archiso` is **absent** (refuse to run from the ISO).
- **[W] Privilege gate.** `20-hardening.yml:35-52`, `30-desktop.yml:34-52`, `40-workflow.yml:39-55` —
  `id -u && id -nG`, assert invoker is root **or** `wheel`.
- **[W] End-user-exists gate.** `20-hardening.yml:54-71` (+30/40) — `id {{ end_user }}`, assert `rc==0`.
- **[W] AUR-helper precondition gate.** `40-workflow.yml:75-93` — `which yay`, assert installed before
  any AUR-dependent Phase-4 module, with an actionable fail message.
- **[W] Pre-flight verification phase (no spec analogue at all).** `roles/verify_boot_network/tasks/
  main.yml:9-86` — UEFI-mode assert (`stat {{ efi_dir }}`), firmware-size read, connectivity ping,
  non-interactive `iwctl` Wi-Fi (`40-48`), and an NTP-active gate (`67-86`), all `changed_when: false`.

**Net:** materially smaller blast radius for a mis-run (wipe against the installed disk, Phase 2 from
the ISO, non-root invocation, missing AUR helper).

## 2. Destructive-op hardening (beyond a pause)

- **[W] Triple-locked partition wipe.** `roles/partitioning/tasks/main.yml:37-77` — (1) target present
  in `lsblk`-detected drives, (2) `target_drive_model` regex-match, (3) `target_drive_size` regex-match,
  (4) explicit `confirm_destructive | bool` gate with "This play will DESTROY all data on …". Drives
  enumerated to a structured fact (`6-21`). Spec 001 uses a single `target_disk` (`001` §4 line 159) +
  a pause — no model/size cross-check.
- **[W] Default-deny confirm flag.** `inventory/group_vars/all.yml:11` `confirm_destructive: false`;
  `Makefile:22-23` `run:` passes `--confirm-destructive`.
- **[W] Drive identity in inventory.** `inventory/hosts.yml:16-18` — `target_drive` +
  `target_drive_model` + `target_drive_size` (three fields, not one path).
- **[W] Keyring + supply-chain steps before pacstrap.** `roles/install_base/tasks/main.yml:23-46` —
  `pacman -Sy archlinux-keyring` first, `reflector --country {{ country }}` mirror selection,
  `pacstrap -K` (keeps keyring).
- **[W] Pre-reboot verification + EBUSY tolerance.** `roles/first_reboot/tasks/main.yml:5-48` — four
  asserts (fstab non-empty, grub.cfg non-empty, user in passwd, root fstype==btrfs) and `umount -R`
  with `failed_when: rc not in [0, 17]` (tolerates the classic busy-tmpfs rc 17).

## 3. Operational selection flexibility (spec concedes it lost this)

- **[W] Three independent selection mechanisms at once** (`40-workflow.yml`):
  1. Per-module boolean — `hosts.yml:82-86 / 111-134 / 155-175` `enable_<id>`.
  2. Whole-profile toggle — `hosts.yml:149-152` `profile_dev/ai/gaming/creative`, folded into flags
     by `40-workflow.yml:98-118` (with the documented Jinja `'false'`-string `| bool` trap, `95-97`).
  3. Run-time narrowing — every role is `tags:`-tagged (`10-install.yml:26-51`,
     `40-workflow.yml:121-197`), so `--tags neovim` edits no file.
- Spec 001 **explicitly concedes** this in its risk section (`001` §3, lines 90-91):
  > "Every enable/disable becomes an inventory edit; there is no boolean to flip and no `--extra-vars`
  > toggle for skipping a component."
  Day-2 changes ("disable screenshots today") are strictly cheaper in the implementation.
- **[W] Inter-module dependency gating (specs model apps as independent).**
  `40-workflow.yml:129-134` — `devpod` requires `containers`; `40-workflow.yml:156-161` — `agents`
  requires `inference` (llama-server). Spec 002 installs each `app_*` independently; `devpod` without
  `podman` / `agents` without inference would be installed and left broken. The implementation refuses.

## 4. Real-world hardware/config content the spec re-derives from scratch

Spec 001 §3 (lines 96-98) admits the old tree's "package lists, distro quirks and hardware
workarounds … are re-derived from scratch." The highest-value artifacts:

- **[W]![N] NVIDIA pacman hook + full chroot driver setup.** `roles/gpu/tasks/nvidia.yml:42-86` +
  `roles/gpu/templates/nvidia.hook.j2:1-16`. Beyond "install nvidia-open": multilib repo + mirrorlist
  include (`28-40`), `nvidia_drm.modeset=1 nvidia_drm.fbdev=1` grub cmdline with grep-guard (`45-53`),
  `MODULES=( nvidia nvidia_modeset nvidia_uvm nvidia_drm )` + **removal of the `kms` hook** (`55-73`),
  in-chroot `mkinitcpio -P` (`81-86`), and a `PostTransaction` hook that rebuilds the initramfs on
  every future driver/kernel transaction (guarded to skip driver-only transactions). *A minimal
  "install the package" role breaks at the first `linux` update.* Caveat: hard to generalise to AMD/
  Intel (those are honest stubs, `amd.yml:7-11`, `intel.yml:7-11`).
- **[W] btrfs subvolume layout + options.** `roles/filesystems_btrfs/tasks/main.yml:51-85` +
  `group_vars/archlinux.yml:21-35` — subvols `@/@home/@snapshots/@var_log/@pkg`,
  `noatime,compress=zstd:3,ssd,space_cache=v2`, `mkfs_args: -L ARCH`, swap-branch device naming
  (`p3` vs `p2`, `main.yml:16-20`), idempotent `changed_when: "'already exists' not in …"`.
- **[W] Grub dual-boot / os-prober flow.** `roles/bootloader_grub/tasks/main.yml:7-27,40-52,106-126` —
  detects the Windows EFI partition, mounts it host-side so os-prober sees it, `saved`-mode
  `GRUB_DEFAULT`/`grub-set-default` handling, post-gen `menuentry` count assert + Windows-detection
  warning.
- **[W] CPU microcode selection.** `cpu_vendor` → `amd-ucode`/`intel-ucode` baked into the pacstrap
  list (`archlinux.yml:63-65`; `install_base/main.yml:8-21` assert + success_msg).
- **[W] Snapper ↔ `@snapshots` integration with idempotency gate + concrete retention.**
  `roles/snapshots/tasks/main.yml:23-96` (whole role gated on `stat /etc/snapper/configs/root`;
  re-run prints "already exists — keeping the existing layout"), and a hard-won 11-value retention
  policy (`roles/snapshots/vars/snapshots_retention.yml:7-18`), both timers enabled, plus
  `grub-btrfs-overlayfs` mkinitcpio hook + `mkinitcpio -P` (`119-136`).
- **[W] `/boot` backup pacman hook.** `roles/snapshots/templates/50-bootbackup.hook.j2:1-12` —
  `Type=Path, Target=boot/*, When=PreTransaction, Exec=… rsync -a --delete /boot /.bootbackup`.
  Protects the boot partition before every pacman transaction. No "install + enable" equivalent.
- **[W] Chroot-stage plumbing everywhere.** Every Phase-1 role re-keys the install verb to
  `arch-chroot <mount> pacman -S --noconfirm` (`roles/_common/tasks/install_by_backend.yml:18-19`).

## 5. User-context mechanisms (specs state the requirement, never the recipe)

- **[W] `sudo -u <user> env XDG_RUNTIME_DIR=/run/user/<uid>` wrapper (~9 sites).** Canonical example
  `roles/sound/tasks/main.yml:16-33` — resolves `id -u {{ end_user }}` (`check_mode: false`), then
  `sudo -u {{ end_user }} env XDG_RUNTIME_DIR=/run/user/<uid> systemctl --user enable --now …`.
  This is the *only* working recipe for `systemctl --user` / `npm -g` / `devpod` from a root play;
  specs 001 D15 / 002 name the requirement but never the mechanism.
- **[W] Rootless podman setup (spec 002's docker role has none of this).** `roles/dev_containers/tasks/
  main.yml:24-59` — `usermod --add-subuids 100000-165535 --add-subgids … {{ end_user }}`,
  `podman system migrate`, then user `podman.socket` via the wrapper.
- **[W] AUR helper built as the end user (cache in `@home`-excluded space).** `roles/aur/tasks/
  main.yml:4-43` — clone-or-pull idempotent guard, makedepends pre-installed
  (`archlinux.yml:121-124`), built `become: false`, final `pacman -U` as root.
- **[W] Check-mode-aware reads.** `check_mode: false` on probes that must return stdout — `id -u`
  (`sound/main.yml:21-23`), `findmnt` (`snapshots/main.yml:145-162`), `timedatectl` poll
  (`clock_sync/main.yml:15-28`).

## 6. Concrete service/config artifacts the specs lack entirely

- **[W]! llama-server systemd *user* unit + full lifecycle.** `roles/ai_inference/tasks/main.yml:25-108`
  + `ansible_bck/templates/llama-server.service.j2:1-17` — `~/models` dir, `ExecStart=… --models-preset
  %h/models/config.ini`, `Restart=on-failure`, `Environment=CUDA_VISIBLE_DEVICES={{ inference_cuda_device
  | default(0) }}`; `daemon-reload → enable-linger → enable --now` chain; `ufw allow 8080/tcp` rule
  (`:91`); acceptance curl to `/v1/models` (`:106-108`). Spec 002's `app_llamacpp` only *builds* — no
  service, no models dir, no port rule. **Caveat:** the unit file sits at repo-level
  `ansible_bck/templates/`, which is **not** on the role's template search path
  (`roles/ai_inference/templates/` + `playbooks/templates/`) — as shipped, this `template` task fails
  at runtime (reproduced with ansible-core 2.21.3). Move it into the role when porting.
- **[W]! Flag-gated GGUF model downloads with exact URLs.** `ai_inference/main.yml:34-43` gated on
  `enable_ai_models`, 7 exact model URLs+filenames (`archlinux.yml:341-356`). Caveat: uses `get_url`,
  which is **not resumable**, despite the comment promising `wget -c` (`archlinux.yml:338`) — an
  interrupted 35B download restarts from zero.
- **[W] devpod release download + provider no-op guard.** `roles/dev_devpod/tasks/main.yml:8-44` —
  `get_url` to `/usr/local/bin/devpod` (idempotent), then `devpod provider list | grep -c '^docker'`
  check-then-add with `DOCKER_PATH=/usr/bin/podman`. No spec counterpart at all.
- **[W] greetd config (answers spec 002's parked Q2).** `roles/display_manager/templates/
  greetd-config.toml.j2:3-8` — `vt=1`, `command="tuigreet --time --remember --cmd Hyprland"`,
  `user="greeter"`; role writes `/etc/greetd/config.toml` mode 0644 + enables `greetd`. Caveat: the
  `greeter` user is never created by any role (latent gap).
- **[W] System fontconfig fallback chain.** `roles/fonts/templates/local.conf.j2` — monospace→
  `Maple Mono NF`, 8-font fallback incl. Noto CJK/Emoji/MDI, `hintslight`/`rgba rgb` for HiDPI
  Wayland; `fc-cache -fv` (`fonts/main.yml:18-31`). Spec 002 `theming` says only "installs … fonts."
- **[W] Sudoers drop-in with validation.** `roles/users_sudo/tasks/main.yml:71-89` —
  `validate: "visudo -cf %s"` + mode 0440, then a full chroot `visudo -c`; plus a `no_log`
  pre-fill-or-prompt password flow (`15-69`). A broken sudoers would otherwise brick the box.

## 7. Graceful degradation / failure tolerance

- **[W] Best-effort dotfiles with remediation.** `roles/desktop_config/tasks/main.yml:24-101` —
  `stat ~/dotfiles/.git` → clone only if absent else `git pull --ff-only`; every stow step
  `failed_when: false` so a bad SSH key can't fail the play; on failure prints exact remediation
  (register the key, re-run `--tags desktop-config`). Spec 001's `dotfiles` role is "clone … runs
  once in play 02" — no pull path, no failure tolerance, no message.
- **[W] AUR-build failure tolerance.** `roles/ai_agents/tasks/main.yml:10-17,39-49` — `failed_when: false`
  on the AUR install + documented manual fallback (claude-desktop AppImage → `/opt` → symlink). Same
  pattern guards the `node` check in `ai_harness/main.yml:10-17`.
- **[W] Cold-start NTP race handled.** `roles/clock_sync/tasks/main.yml:15-28` — polls `timedatectl`
  with `until/retries: 10/delay: 3` (`check_mode: false`) instead of one immediate read; also prints
  the exact Windows `RealTimeIsUniversal` registry fix for dual-boot (`39-46`).
- **[W] Pre-existing-repo protection.** `roles/dotfiles_backup/tasks/main.yml:18-41` — `stat` both the
  dir and `.git`; `git init` only when the dir is absent ("never `git init` over an existing repo").
  Spec 001's clone role has no such guard — a naive rewrite risks clobbering `~/dotfiles`.
- **[W] Per-module verify/acceptance oracles.** The `debug` notes carry exact verify commands and
  keybind expectations across desktop/AI roles (`sound/main.yml:36-38`, `ai_inference/main.yml:106-108`,
  clipboard round-trip, screenshots keybinds) — de-facto test oracles the specs don't provide.

## 8. Already-populated data corpus (cheapest to lift verbatim)

- **[W] The entire `distro_packages` corpus is filled** with working, machine-specific values —
  `group_vars/archlinux.yml:38-246`. Spec 002 fills only 3 package keys (`app_llamacpp/opencode/
  vscode`, `002` §4); the rest of the roster is empty templates. Also:
  - AI model GGUF URLs+filenames (`341-362`), npm globals (`333-337`), AUR pkgs (`326-332`, `183-191`,
    `234`), devpod binary URL (`360-362`).
  - `distro_commands` + `distro_paths` split (`378-407`) — a bigger distro-abstraction than spec 001's
    bootstrap-mechanics set (`bootstrap_cmd`/`commands`/`chroot_prefix`/`target_root`, `001` §4:169);
    for a second distro every command/path difference has an obvious slot.

## 9. Honest balance — where the specs are actually better

To keep this from over-selling the old tree, these are places the **specs win** (do not port the old
way):

- **[N] `--check`-first installer.** Spec 001 D10 uses real modules (`community.general.pacman`, etc.)
  that report `changed` honestly and support `--check`. The old `roles/_common/tasks/
  install_by_backend.yml:21-35` is `shell`-based with `changed_when: rc == 0` — `--check` does not
  work and "changed" just means "the verb succeeded."
- **[N] Check-mode posture.** The old tree has only 4 `check_mode: false` sites and **no `creates:`
  anywhere**; the destructive `gdisk`/`mkfs` steps are not idempotent (a re-run re-wipes). Spec 001
  D13's "`02-04 are idempotent / re-runnable via `--check`" is a real improvement.
- **[N] Generated-playbook liability.** Spec 001 D12 drops the generator; the old
  `Makefile:19-20` `check:` runs `generators/manifest_to_playbook.py --check` against
  `../os/archlinux/manifest.yaml` — a genuine parity-enforcement capability the new tree lacks, but
  the new tree's "no second source of truth" stance is defensible. Nuanced, not a clear win either way.
- **[N] Gaming/creative + several dev roles are placeholders** (`gaming_*`, `creative_*`,
  `dev_neovim/languages/api_testing/training` are mostly `debug`-only). A from-scratch rewrite loses
  nothing there but the scope notes.

## 10. Porting caveats (defects found in the old tree)

- **`llama-server.service.j2` is mislocated** — see §6. Must move into `roles/ai_inference/templates/`
  or the `template` task fails at runtime.
- **Model downloads use `get_url` (non-resumable)** despite the `wget -c` intent — see §6.
- **`greeter` user is never created** — see §6.
- **`sound` uses `enable --now`** (starts sockets), in tension with spec 002's "enable, never start"
  contract (`002` Task 7.2 expects 0 `state: started`). Sockets are benign, but it is a real deviation.

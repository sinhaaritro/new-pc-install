# Ansible — Play 1: Live-USB Install Through First Reboot (Phase 0–1)

Automates the Arch Linux install from the live USB (`root@archiso`): Phase 0
verification gate, then Phase 1 modules 01–08, ending in a reboot into a
bootable dual-boot CLI system (GRUB menu with Linux + Windows).

The module/package source of truth is
[`os/archlinux/manifest.yaml`](../os/archlinux/manifest.yaml); the generator
parity check keeps the two from drifting.

## User Flow

1. **Phase 0 (manual, pre-Linux)** — follow
   [`os/archlinux/phase-0-pre-install/`](../os/archlinux/phase-0-pre-install/README.md):
   BIOS Secure Boot off, Windows Fast Startup off, flash the USB, boot in UEFI mode.
2. **On the live USB**, install the tooling:

   ```bash
   pacman -S git ansible
   git clone <this-repo-url> ~/new-pc-install
   cd ~/new-pc-install/ansible
   ```

3. **Set your drive** in `inventory/hosts.yml` — the single "place to put the
   drive". Identify it first:

   ```bash
   lsblk -o NAME,SIZE,MODEL
   ```

   Set `target_drive` (e.g. `nvme1n1`), `target_drive_model` (e.g. `SAMSUNG`),
   and `target_drive_size` (e.g. `1T`). These are validated before anything is
   written.
4. **Run Play 1** with the destructive gate flag:

   ```bash
   make run
   # or: ansible-playbook playbooks/10-install.yml --confirm-destructive
   ```

    The play will halt before writing any GPT table unless `--confirm-destructive`
    is present. You will be prompted for the root and end-user passwords
    (see **Passwords** below).
5. **Reboot** — the play ends in `reboot`. Remove the USB when the system
   powers off. Confirm the GRUB menu shows **Arch Linux** and
   **Windows Boot Manager**, boot Linux, log in as your user, and check
   `ping archlinux.org`, `findmnt -t btrfs`, `ls /sys/firmware/efi`.

## Safety Gates

- **Destructive gate** — no GPT table is written without `--confirm-destructive`.
- **Drive validation** — `target_drive` must be present and match
  `target_drive_model` / `target_drive_size` before the gate is reached.
- **Phase 0 gate** — the `preflight` role asserts UEFI mode, internet, NTP,
  and target drive presence up front; any failure halts with a clear message.
- **Selectable layout** — `fstype` (only `btrfs` implemented) gates the
  btrfs-specific checks in `filesystems_btrfs`, `system_config`, and
  `first_reboot`; `bootloader` (only `grub` implemented) is the same pattern
  for the bootloader role.
- Re-runs are safe from the live USB: the play re-partitions and re-pacstraps
  from scratch (idempotent recovery path).

## Distro Selection (Option A: distros as data)

`ansible_distro: archlinux` in the inventory selects
`vars/distros/<distro>.yml`, which carries the per-distro package names,
commands, paths, and layout constants (btrfs layout, gdisk hex codes, sudo
group/shell). Adding a distro later means adding a data file — no role
   rewrites. Only `archlinux.yml` exists in this spec (Phase 0–1 scope).

## Passwords (spec 003)

`root_password` and `end_user_password` are per-machine inventory vars with
pre-fill semantics:

- **Non-empty value** → used as-is; the keyboard prompt is skipped.
- **Empty (`""`) or absent** → the play prompts interactively.
- **Enter at the prompt** → that password is left unset for now.

Both are applied via `chroot chpasswd` with `no_log: true`. Prefer the
prompt for a fresh install; the inventory pre-fill exists for re-runs and
automation.

## Var Layering (spec 002: single source of truth)

One rule for where values live:

- **Per-machine values** → `inventory/hosts.yml` (`target_drive*`,
  `hostname`, `timezone`, `locale`, `end_user`, `country`, `efi_size`,
   `swap`, `swap_size`, `fstype`, `bootloader`, `root_password`,
   `end_user_password`).
- **Static shared layout constants** → `group_vars/all.yml`
  (`ansible_distro`, `mount_point`, `efi_dir` — the UEFI efivars path — and
  the `confirm_destructive` gate).
- **Distro-specific data** (packages/commands/paths/btrfs/gdisk/sudo) →
  `vars/distros/<distro>.yml`.

Roles reference these keys directly; no `roles/*/defaults/<distro>.yml`
files remain.

## Verification (always-on, no CI)

```bash
make lint     # yamllint + ansible-lint
make syntax   # ansible-playbook --syntax-check
make check    # manifest <-> playbook parity (exit 0 iff in sync)
```

Acceptance = the manual bring-up above: Play 1 reboots into a GRUB menu showing
both Linux and Windows.

## Layout

```
ansible/
├── ansible.cfg
├── inventory/hosts.yml        # per-machine values: drive, identity, layout, swap, fstype, bootloader, passwords, country
├── group_vars/all.yml         # static shared constants: mount_point, efi_dir, gate
├── vars/distros/archlinux.yml # Option A distro layer (packages/commands/paths/layout)
├── playbooks/10-install.yml   # Play 1: preflight -> modules 01-08 -> reboot
├── roles/
│   ├── preflight/             # Phase 0 gate (overview, pre-flight, verify-boot)
│   ├── partitioning/          # 02 (detect-all fact, validation, gate, gdisk template)
│   ├── filesystems_btrfs/     # 03 (mkfs, subvolumes, mounts)
│   ├── install_base/          # 04 (reflector, keyring, pacstrap -K /mnt)
│   ├── system_config/         # 05 (genfstab; chroot: timezone, locale, hostname, NM)
│   ├── users_sudo/            # 06 (user + sudoers.d drop-in, chroot-stage)
│   ├── bootloader_grub/       # 07 (grub, mkconfig, os-prober, efibootmgr)
│   └── first_reboot/          # 08 (final checks, unmount, reboot)
└── generators/manifest_to_playbook.py  # parity checker
```

# 02 Core Config

> **Module id**: `desktop-config`
> **Phase**: 3 — Desktop
> **Prerequisites**: [Window Manager](./01-install.md), [Dotfiles (GNU Stow)](../dotfiles-backup.md)
> **Packages**: none (config is applied via Stow; the compositor is installed by #1)

---

## Overview

Apply the compositor's core configuration — keybinds, monitors, window rules,
input — using **GNU Stow**. This module is the **last step of the desktop play**:
it runs after the compositor is installed and after the dotfiles repo is ready.

The config content lives in your **private** dotfiles repo
(`git@github.com:sinhaaritro/dotfiles.git`). This module does not author any
config — it fetches the repo over SSH and stows it into your home directory.
(ADR-011: user dotfiles are owned by your stow package, not by automation.)

## How the automation does it

The `desktop_config` role (runs as your user, `become: false`):

1. **Fetch the private repo over SSH** with your key
   (`git@github.com:sinhaaritro/dotfiles.git` → `~/dotfiles`):
   - clones it if `~/dotfiles` is not yet a git repo,
   - otherwise `git pull --ff-only` to update it.
2. **Stow every top-level package** in the repo (`stow <pkg>` for each
   directory, skipping `.git`).
3. **Report** the result.

> [!NOTE]
> Because this runs **last**, a failure here does not fail the whole play. Every
> step is best-effort: if the repo can't be fetched (SSH key not registered, or
> no network), the role prints a "register your key / re-run" message and skips
> stowing.

## Manual steps (reference)

```bash
# 1. Fetch the private repo (your key must be registered on it first)
git clone git@github.com:sinhaaritro/dotfiles.git ~/dotfiles
cd ~/dotfiles && git pull --ff-only

# 2. Stow every package
for pkg in */; do stow "${pkg%/}"; done
```

## If it was skipped (SSH / auth)

If the role skipped, your SSH key isn't registered on the repo yet. Register
`~/.ssh/id_ed25519.pub` (GitHub → repo Settings → Deploy keys, or your account),
then re-run just this module:

```bash
ansible-playbook 30-desktop.yml --tags desktop-config
```

## Verification

```bash
# a stowed config is a symlink back into the repo
ls -la ~/.config/hypr/

# the compositor picked up the config (reload and check keybinds/monitors apply)
```

#!/usr/bin/env python3
"""Manifest/playbook parity checker (spec 001, D1).

os/archlinux/manifest.yaml is the single source of truth for modules and
packages. This script verifies that the Ansible tree cannot silently drift
from it:

  1. Every Phase 0-2 module id has a role whose tasks/main.yml references it
     (preflight covers phase-0: overview + pre-flight; gpu covers the
     phase-2 nvidia module).
  2. Every package listed in a Phase 0-2 module is referenced somewhere in
     the Ansible tree (roles/ + vars/ + group_vars/).

Usage:
  manifest_to_playbook.py --check [--manifest PATH]

Exit 0 = green, exit 1 = drift detected.
"""

import argparse
import re
import sys
from pathlib import Path

ANSLIB = Path(__file__).resolve().parent.parent
ROLE_MAP = {
    "overview": "preflight",
    "pre-flight": "preflight",
    "verify-boot": "preflight",
    "partitioning": "partitioning",
    "filesystems": "filesystems_btrfs",
    "install-base": "install_base",
    "system-config": "system_config",
    "users-sudo": "users_sudo",
    "bootloader": "bootloader_grub",
    "first-reboot": "first_reboot",
    "nvidia": "gpu",
    "snapshots": "snapshots",
    "aur": "aur",
    "sound": "sound",
    "networking": "networking",
    "clock-sync": "clock_sync",
    "firewall": "firewall",
    "external-drives": "external_drives",
    "ssh": "ssh_git",
    "hyprland-install": "hyprland_install",
    "hyprland-config": "hyprland_config",
    "hyprland-lock": "hyprland_lock",
    "hyprland-wallpaper": "hyprland_wallpaper",
    "hyprland-screenshare": "hyprland_screenshare",
    "shell-terminal": "shell_terminal",
    "app-launcher": "app_launcher",
    "status-bar": "status_bar",
    "notifications": "notifications",
    "display-manager": "display_manager",
    "clipboard": "clipboard",
    "screenshots": "screenshots",
    "file-manager": "file_manager",
    "fonts": "fonts",
    # Phase 4 (profile-structured; spec 006 D6). Module ids stay flat - they
    # are unique across profiles in the manifest. 'davinci' maps to an
    # extended role name to avoid the Phase 3 namespace collision (ADR-020).
    # 'dotfiles' is the manifest id of the SHARED Phase 4 module (its docs
    # file is dotfiles-backup.md; the role directory is dotfiles_backup).
    "dotfiles": "dotfiles_backup",
    "dotfiles-backup": "dotfiles_backup",
    "neovim": "dev_neovim",
    "containers": "dev_containers",
    "devpod": "dev_devpod",
    "languages": "dev_languages",
    "api-testing": "dev_api_testing",
    "inference": "ai_inference",
    "harness": "ai_harness",
    "ide-integration": "ai_ide_integration",
    "agents": "ai_agents",
    "training": "ai_training",
    "steam": "gaming_steam",
    "proton": "gaming_proton",
    "heroic": "gaming_heroic",
    "mangohud": "gaming_mangohud",
    "controllers": "gaming_controllers",
    "obs": "creative_obs",
    "davinci": "creative_davinci_resolve",
    "media-players": "creative_media_players",
}

PHASE_IDS = ("phase-0", "phase-1", "phase-2", "phase-3", "phase-4")


def load_modules(manifest_path):
    """Return {module_id: module_dict} for the covered phases.

    Phases carry a flat 'modules:' list; phase-4 carries a 'profiles:' list
    whose entries each hold a 'modules:' list (spec 006 D6) - both shapes are
    walked, ids stay flat.
    """
    import yaml

    if not manifest_path.is_file():
        print(f"manifest not found: {manifest_path}")
        raise SystemExit(1)
    with open(manifest_path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    modules = {}
    for phase in data.get("phases", []):
        if phase.get("id") not in PHASE_IDS:
            continue
        for module in phase.get("modules", []):
            modules[module["id"]] = module
        for profile in phase.get("profiles", []):
            for module in profile.get("modules", []):
                modules[module["id"]] = module
    return modules


def read_tree(paths):
    chunks = []
    for path in paths:
        if path.is_dir():
            chunks.extend(p.read_text(encoding="utf-8") for p in path.rglob("*.yml"))
            chunks.extend(p.read_text(encoding="utf-8") for p in path.rglob("*.j2"))
        elif path.is_file():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def check():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--manifest", default=str(ANSLIB.parent / "os" / "archlinux" / "manifest.yaml"))
    args = parser.parse_args()

    modules = load_modules(Path(args.manifest))
    errors = []

    role_tasks = [
        (module_id, ROLE_MAP[module_id] + "/tasks/main.yml")
        for module_id in ROLE_MAP
        if module_id in modules
    ]

    missing_modules = [m for m in modules if m not in ROLE_MAP]
    for module_id in missing_modules:
        errors.append(f"module {module_id!r} has no role mapping (add it to ROLE_MAP)")

    for module_id, rel in role_tasks:
        path = ANSLIB / "roles" / rel
        if not path.is_file():
            errors.append(f"module {module_id!r}: missing role file roles/{rel}")
            continue
        if module_id not in path.read_text(encoding="utf-8"):
            errors.append(f"module {module_id!r}: role file roles/{rel} does not reference it")

    package_ids = set()
    for module in modules.values():
        package_ids.update(module.get("packages", []))

    tree = read_tree([ANSLIB / "roles", ANSLIB / "vars", ANSLIB / "group_vars"])
    for package in sorted(package_ids):
        if not re.search(r"\b" + re.escape(package) + r"\b", tree):
            errors.append(f"package {package!r} (from manifest) not referenced in ansible/ roles, vars, or group_vars")

    if errors:
        print("PARITY FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"PARITY OK: {len(modules)} Phase 0-4 modules, {len(package_ids)} packages all covered")
    return 0


if __name__ == "__main__":
    sys.exit(check())

# AUR Helper (yay)

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/08-first-reboot.md)
> **Packages**: None (yay is built from AUR)

---

## Overview

The **Arch User Repository (AUR)** contains community-built packages not in the official repositories. You can build them manually or use an AUR helper like `yay` to automate the process.

> [!TIP]
> It is better to understand manual AUR builds before relying on a helper. See [AUR Best Practices (YouTube)](https://www.youtube.com/watch?v=goOrF8zAkqU).

## Reference

- [AUR Web Interface](https://aur.archlinux.org/)

## Manual AUR Build (Without Helper)

### Building a Package

1. Search for the package at https://aur.archlinux.org/
2. Copy its **Git Clone URL**
3. Clone and build:
   ```bash
   git clone https://aur.archlinux.org/PACKAGE_NAME.git
   cd PACKAGE_NAME
   makepkg -si
   ```
   - `-s` installs missing dependencies
   - `-i` installs the built package

### Upgrading a Package

```bash
cd PACKAGE_NAME
git pull
makepkg -si
```

---

## Install yay (AUR Helper)

### Step 1: Clone yay

```bash
mkdir -p ~/aur
cd ~/aur
git clone https://aur.archlinux.org/yay.git
cd yay
```

### Step 2: Build and Install

```bash
makepkg -si
```

## yay Usage

| Command | Purpose |
|---------|---------|
| `yay PACKAGE_NAME` | Search and install a package |
| `yay -S PACKAGE_NAME` | Install a specific package |
| `yay -Syu` | Update all packages (pacman + AUR) |
| `yay -Rns PACKAGE_NAME` | Remove package + unused dependencies |

> [!NOTE]
> When yay prompts:
> - **Clean build?** Select `N` (unless the previous build failed, then `A`)
> - **Diff?** Select `N` for trusted packages, `Y` to review PKGBUILD changes

## Verification

```bash
yay --version
```

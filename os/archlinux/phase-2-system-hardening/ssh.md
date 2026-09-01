# SSH & Git

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/09-first-reboot.md)
> **Packages**: `openssh`

---

## Overview

Set up SSH keys for GitHub authentication and configure Git. Includes multi-key setup for managing multiple accounts.

## Prerequisites

```bash
sudo pacman -S openssh
```

## Steps

### Step 1: Check for Existing SSH Keys

```bash
ls ~/.ssh
```

Look for `id_ed25519` and `id_ed25519.pub`. If they exist, you already have a key pair.

### Step 2: Generate a New SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- Press `Enter` to accept the default location (`~/.ssh/id_ed25519`)
- Add a passphrase for extra security, or press `Enter` for none

> [!NOTE]
> If your system doesn't support Ed25519: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`

### Step 3: Add the Key to the SSH Agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Step 4: Add the Key to GitHub

Copy the public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

1. Go to [GitHub → Settings → SSH and GPG keys](https://github.com/settings/keys)
2. Click **New SSH Key**
3. Paste the public key, give it a title, click **Add SSH Key**

### Step 5: Test the Connection

```bash
ssh -T git@github.com
```

Expected output:
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## Multi-Key Setup

For multiple accounts or services, use separate keys with an SSH config file.

### Naming Convention

Use descriptive names: `id_ed25519_service_account`

```
~/.ssh/
├── id_ed25519_github_personal
├── id_ed25519_github_personal.pub
├── id_ed25519_github_work
├── id_ed25519_github_work.pub
└── config
```

### Generate Separate Keys

```bash
ssh-keygen -t ed25519 -C "personal@email.com" -f ~/.ssh/id_ed25519_github_personal
ssh-keygen -t ed25519 -C "work@email.com" -f ~/.ssh/id_ed25519_github_work
```

### Configure SSH Config

```bash
touch ~/.ssh/config
chmod 600 ~/.ssh/config
nvim ~/.ssh/config
```

```text
# Personal GitHub Account
Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github_personal

# Work GitHub Account
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github_work
```

### Use Host Aliases

```bash
# Personal
git clone git@github-personal:username/repo.git

# Work
git clone git@github-work:username/repo.git
```

---

## Git Configuration

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519
git config --global commit.gpgsign true
```

> [!NOTE]
> Also add the `.pub` key to GitHub as a **Signing Key** (separate from Authentication Key) under SSH and GPG keys settings.

## Verification

```bash
ssh -T git@github.com
git config --list | grep user
```

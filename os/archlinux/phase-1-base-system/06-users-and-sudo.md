# Users & Sudo

> **Phase**: 1 — Base System
> **Prerequisites**: [System Configuration](./05-system-config.md)
> **Packages**: None (already installed with `base`)

---

## Overview

Set the root password, create your user account, and configure `sudo` access via the `wheel` group.

## Steps

### Step 1: Set Root Password

```bash
passwd
```

Enter and confirm a strong root password.

### Step 2: Create Your User Account

```bash
useradd -m -G wheel -s /bin/bash username
passwd username
```

*(Replace `username` with your desired username, e.g., `aritro`)*

| Flag | Purpose |
|------|---------|
| `-m` | Create a home directory (`/home/username`) |
| `-G wheel` | Add to the `wheel` group (for sudo access) |
| `-s /bin/bash` | Set default shell to bash (can switch to zsh later) |

### Step 3: Enable Sudo for the Wheel Group

```bash
EDITOR=nano visudo
```

Find the line:
```text
# %wheel ALL=(ALL:ALL) ALL
```

Remove the leading `#` to uncomment it:
```text
%wheel ALL=(ALL:ALL) ALL
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

### Step 4: (Optional) Allow Passwordless Commands

To let wheel members run certain commands without a password, add this below the `%wheel` line:

```text
## Allow wheel members to run some commands without a password
%wheel ALL=(ALL) NOPASSWD: /usr/bin/shutdown,/usr/bin/reboot,/usr/bin/pacman -Syu,/usr/bin/pacman -Syyu,/usr/bin/pacman -Rns
```

> [!NOTE]
> This is a convenience trade-off. Only add commands you're comfortable running without password confirmation.

## Verification

You can test sudo access after first reboot by logging in as your user and running:
```bash
sudo whoami
```
It should prompt for your password and output `root`.

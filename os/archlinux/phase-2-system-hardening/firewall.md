# Firewall (ufw)

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/08-first-reboot.md)
> **Packages**: `ufw`

---

## Overview

`ufw` (Uncomplicated Firewall) provides a simple interface for managing `iptables` firewall rules.

## Steps

### Step 1: Install

```bash
sudo pacman -S ufw
```

### Step 2: Configure Default Rules

```bash
# Deny all incoming connections by default
sudo ufw default deny incoming

# Allow all outgoing connections
sudo ufw default allow outgoing
```

### Step 3: Enable

```bash
sudo ufw enable
sudo systemctl enable ufw
```

### Step 4: Common Rules (Optional)

```bash
# Allow SSH (if you need remote access)
sudo ufw allow ssh

# Allow specific port
sudo ufw allow 8080

# Check status
sudo ufw status verbose
```

## Verification

```bash
sudo ufw status
```

Should show `Status: active` with your configured rules.

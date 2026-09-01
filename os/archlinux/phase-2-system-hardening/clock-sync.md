# Clock Sync (Dual-Boot)

> **Phase**: 2 — System Hardening
> **Prerequisites**: [First Reboot](../phase-1-base-system/09-first-reboot.md)
> **Packages**: None

---

## Overview

When dual-booting Linux and Windows, the system clock can be off by several hours because Linux uses **UTC** for the hardware clock while Windows uses **local time** by default. The fix is to make Windows use UTC.

## Steps

### Step 1: Enable NTP in Arch Linux

```bash
sudo timedatectl set-ntp true
```

### Step 2: Fix Windows to Use UTC

In Windows, open a **Command Prompt as Administrator** and run:

```cmd
reg add "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\TimeZoneInformation" /v RealTimeIsUniversal /d 1 /t REG_DWORD /f
```

Reboot Windows for the change to take effect.

## Reference

- [Arch Wiki: System time — UTC in Windows](https://wiki.archlinux.org/title/System_time#UTC_in_Microsoft_Windows)

## Verification

After rebooting into each OS, the time should be correct in both.

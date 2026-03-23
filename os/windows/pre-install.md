# 📝 Windows 11 Pre-Installation Checklist 📝

---

## I. System Documentation & Backup 📸

1.  **Update Screenshots:** Capture your current configurations, start menu layouts, and custom settings.
2.  **Export Application Lists:**
    *   Take screenshots of installed applications in the **Control Panel**.
    *   Export a list of installed apps via **winget** (e.g., `winget export -o apps.json`).
3.  **Save Browser State:** Bookmark or export active tabs in Google Chrome (and any other browsers).

---

## II. Data Migration & Cleanup 🧹

1.  **Backup Personal Files:**
    *   Carefully review and copy important data from primary user folders: `Downloads`, `Desktop`, `Documents`, `Pictures`, `Videos`, and `Music`.
2.  **Prepare Secondary Partitions:**
    *   Clean up or backup any other partitions on your drives, especially if you plan to wipe them entirely during reinstallation.

---

## III. Hardware & Boot Preparation ⚠️

1.  **Prepare Installation Media:**
    *   Create a bootable USB Flash Drive (Pendrive) equipped with the latest **Windows 11 Setup**.
2.  **Disconnect Alternative OS Drives (Crucial Step):**
    *   > **❗️ Very Important:** If you have another Operating System (like Linux) installed on a separate drive, **physically disconnect** that drive from the motherboard before booting the installer.
    *   *> Reason: The Windows setup is notorious for mistakenly installing the Windows Boot Manager onto the EFI partition of secondary drives instead of the target C: drive. Physically removing the other drives prevents this.*

---
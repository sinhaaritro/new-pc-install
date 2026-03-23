# ✨ Windows 11 Installation Guide ✨

---

## I. Initial Boot & Windows Setup

1.  Boot from the **Windows 11 Installation Media** (USB/DVD).
2.  During setup, select **`I do not have a product key`** when prompted.
3.  Choose **`Windows 11 Home N`** as the edition.
    *   *> Note: Media features (like Windows Media Player) are not pre-installed in 'N' editions and must be added manually later.*

---

## II. ⚠️ Disk Preparation (Critical Step!) ⚠️

1.  Proceed to the disk partitioning stage within the installer.
2.  **Delete ALL existing partitions** on the target installation drive.
3.  > **❗️ Very Important:** If other drives are connected (e.g., with Linux), **you MUST delete their partitions too**, especially any **EFI partition**. Failure to do so can cause the Windows Boot Manager to install on the wrong drive.

---

## III. Windows Installation Process ⏳

1.  Allow Windows to install.
2.  The system will **restart multiple times** automatically.
    *   *> Let this process complete without interruption.*

---

## IV. Out-of-Box Experience (OOBE) & Initial Connection 🌐

1.  Follow the on-screen prompts for the post-installation setup (OOBE):
    *   Select your **Language**, **Region**, and **Keyboard Layout**.
    *   **Connect to the internet** when prompted. *(This allows important updates to download during setup).*
    *   Complete the account login steps (typically using your **Microsoft Account**).

---

## V. First Login & System Setup 🖥️

1.  After reaching the Windows desktop for the first time:
    *   Immediately run **Windows Update** (`Settings` > `Windows Update`) and install **ALL** available updates. Reboot if necessary and check again until no more critical updates are found.
    *   Review and adjust **Privacy Settings** (`Settings` > `Privacy & security`) to your preference.
    *   Sign in to essential **Microsoft Services**:
        *   OneDrive
        *   Outlook (Mail app or Office)
        *   Microsoft Edge
    *   Download, install, and sign in to **Google Chrome** (or your preferred browser).

---

## VI. Core Driver Installation ⚙️

1.  **Reboot** the computer.
2.  Install **Motherboard-Specific Drivers**:
    *   Follow your manufacturer's method. See [BIOS setup](../../hardware/bios/setup.md) for related settings.
    *   *> Example: For ASRock boards, you might enable the 'Auto Driver Installer' in the BIOS/UEFI to automatically get Wi-Fi, Bluetooth, LAN, Audio, etc.*

---

## VII. Adjusting Login Settings 🔑

*   [**(Optional) Enable Automatic Login Setup**](./optional-login.md)

---

## VIII. System Configuration Tweaks 🛠️

1.  **Turn OFF Fast Startup:**
    *   Open **Control Panel** > `Hardware and Sound` > `Power Options`.
    *   Click **'Choose what the power buttons do'** > **'Change settings that are currently unavailable'**.
    *   **UNCHECK** the box for **'Turn on fast startup (recommended)'** and save.
    *   *> Reason: Fast Startup keeps the disk partially mounted, preventing other OSes (like Linux) from accessing it safely.*

---

## IX. Essential Software & Features 📦

1.  **Install Media Features (Required for Windows N):**
    *   Go to `Settings` > `Apps` > `Optional features`.
    *   Search for **`Media Feature Pack`**, select it, and install.
2.  **Install Graphics Drivers**:
    *   Download and install the **Nvidia App / GeForce Experience** (or AMD Adrenalin Software).

---

## X. 💾 Drive Partitioning (Post-Setup)

*   [**(Optional) Shrink Windows Partition for Dual Boot**](./optional-partitioning.md)

---

## XI. 🔊 Audio & Peripheral Setup

Since everyone's hardware varies, specific configurations are modularized.
Choose what matches your current setup:

*   **Audio Routing:** [Install & Configure Voicemeeter Potato](../../software/audio/voicemeeter-potato/README.md) (optional)
*   **Mouse Software:** [Setup Logitech G502 Macros](../../peripherals/mouse/logitech-g502/README.md)
*   **Keyboard Layouts:** [Flash RK-R65 / Shorty Zero 1 Layouts](../../peripherals/keyboards/README.md) (via QMK/VIA)
*   **RGB Lighting:**
    *   [ASRock Polychrome](../../hardware/lighting/asrock/windows-setup.md)
    *   [G.Skill RAM](../../hardware/lighting/gskill/windows-setup.md)
    *   [Zotac GPU Lighting (FireStorm)](../../hardware/lighting/zotac/windows-setup.md)

---

## XII. 💻 Applications & Workloads

### 1. Developer Tools 💻
*   Install **Git** for Windows (Download from [git-scm.com](https://git-scm.com/))
*   [**VSCodium Setup & Extensions**](../../software/development/vscodium/windows-setup.md)

### 2. Optional Workloads 🎮 🎨 
Depending on your use-case, follow these extended guides:
*   [**Microsoft Office Setup** (Download & MAS Activation)](../../software/office/windows-setup.md)
*   [**Gaming Setup** (Steam, Epic, Discord fixes)](../../software/gaming/windows-setup.md)
*   [**Creative Workflow** (DaVinci Resolve)](../../software/creative/davinci-resolve/windows-setup.md)

---

## XIII. Final Personalization ✨

1.  **Organize Files:** If you prefer a different path than the default libraries, create **'Pseudo' Folders** for `Downloads`, `Pictures`, `Videos`, and `Documents` in a data drive. Update Windows settings to point to them instead of Drive C:.

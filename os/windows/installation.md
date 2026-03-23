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
    *   > **❗️ Very Important:** If other drives are connected (e.g., with Linux), **you MUST delete their partitions too**, especially any **EFI partition**. Failure to do so can cause the Windows Boot Manager to install on the wrong drive.

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
    *   Follow your manufacturer's method (e.g., download from their website, use included media).
    *   *> Example: For ASRock boards, you might enable the 'Auto Driver Installer' in the BIOS/UEFI to automatically get Wi-Fi, Bluetooth, LAN, Audio, etc.*

---

## VII. Adjusting Login Settings 🔑

1.  **Configure Windows Hello Sign-in Options:**
    *   Navigate to: `Settings` > `Accounts` > `Sign-in options`.
    *   Scroll down to **'Additional Settings'**.
    *   Ensure the switch for **'For improved security, only allow Windows Hello Sign-in for Microsoft accounts on this device (Recommended)'** is toggled **OFF**.
2.  **Set Up Automatic Login (via `netplwiz`):**
    *   Press `Win + R`, type `netplwiz`, and press `Enter`.
    *   Select your user account in the list.
    *   **Manage the Checkbox:**
        *   If **'Users must enter a user name and password to use this computer'** is *unchecked*, **CHECK IT** and click **Apply**.
        *   Now, **UNCHECK** the box **'Users must enter a user name and password to use this computer'** and click **Apply**.
    *   **Enter Credentials Carefully:**
        *   A pop-up window titled 'Automatically sign in' appears.
        *   > **❗️ CRITICAL:** ERASE any pre-filled username.
        *   **Username:** Enter your **FULL Microsoft account email address**.
        *   **Password:** Enter your **Microsoft account password**.
        *   **Confirm Password:** Re-enter your password. *Accuracy is vital here!*
        *   Click **OK**.
    *   Click **OK** again on the main `netplwiz` window.
3.  **Restart** the computer to apply the auto-login setting.

---

## VIII. System Configuration Tweaks 🛠️

1.  **Turn OFF Fast Startup:**
    *   Open **Control Panel**.
    *   Go to `Hardware and Sound` > `Power Options`.
    *   Click **'Choose what the power buttons do'** (left sidebar).
    *   Click **'Change settings that are currently unavailable'** (requires admin rights).
    *   **UNCHECK** the box for **'Turn on fast startup (recommended)'**.
    *   Click **'Save changes'**.
    *   *> Reason: Fast Startup keeps the disk partially mounted, which can prevent other OSes (like Linux) from accessing it safely, potentially leading to data corruption warnings or mount failures.*

---

## IX. Essential Software & Features 📦

1.  **Install Media Features (Required for Windows N):**
    *   Go to `Settings` > `Apps` > `Optional features`.
    *   Click **'View features'** (next to 'Add an optional feature').
    *   Search for **`Media Feature Pack`**, select it, and click **'Next'** then **'Install'**.
    *   *(Audio software installation is in a separate step below).*
2.  Install **Graphics Drivers**:
    *   Download and install the **Nvidia App** / **GeForce Experience** (or AMD Adrenalin Software).
    *   Ensure you get the latest drivers for your GPU.

---

## X. 💾 Drive Partitioning (Post-Setup)

1.  **Shrink Windows Partition & Create New Volume:**
    *   Right-click the **Start Button** and select **'Disk Management'**.
    *   Locate your main Windows partition (usually **C:**).
    *   Right-click the **C:** partition and select **'Shrink Volume...'**.
    *   In the field **'Enter the amount of space to shrink in MB'**, enter a value that leaves your desired amount for C:.
        *   *> Example: To leave Windows with exactly **250 GB** (which is roughly **256,000 MB**), calculate `Total Size (MB) - 256000 = Amount to Shrink (MB)`. Enter the result.*
    *   Click **'Shrink'**.
    *   You'll see **'Unallocated'** space appear.
    *   Right-click the **'Unallocated'** space and select **'New Simple Volume...'**.
    *   Follow the wizard to create a new partition (assign a drive letter, format it - usually NTFS). This new partition can be used for data, other installs, etc.

---

## XI. 🎧 Audio Software Setup

1.  Install preferred audio software (e.g., **VoiceMeeter**).
2.  Configure the audio software.
    *   *> Note: Remember to use the specific **VoiceMeeter settings files and reference images** available in the repository for consistent setup.*

---

## XII. Peripheral & Aesthetic Software 💡

1.  Install **RGB Control Software** for your components (Motherboard, RAM, GPU, Mouse, etc.) if desired.

---

## XIII. Application & Game Installation 🎮

1.  Install your standard **Desktop Applications** (Productivity, Utilities, etc.).
2.  Install apps from the **Microsoft Store**.
3.  Install your **Games** (via Steam, Epic Games Launcher, GOG Galaxy, etc.).

---

## XIV. Final Personalization & Tweaks ✨

1.  **Organize Files:** If you prefer a different path than the default libraries, create custom folders (**'Pseudo' Folders**) for `Downloads`, `Pictures`, `Videos`, and `Documents` in a different drive/partition. Link them to the new folders.
2.  **Set Discord Default Monitor (for Multi-Monitor setups):**
    *   Open Discord.
    *   Ensure the Discord window is **NOT maximized**.
    *   Drag the **small Discord window** to your desired secondary monitor.
    *   **Close Discord** while it's still small and on that monitor.
    *   Re-open Discord. It should now default to opening on that screen. You can maximize it normally afterwards.

---

# ✨ New AM5 Motherboard: Essential BIOS/UEFI Setup Guide ✨

This guide outlines key steps to configure your BIOS/UEFI after installing a new AM5 motherboard, focusing on enabling optimal RAM performance while ensuring fast boot times. *Exact menu names vary by manufacturer (ASUS, Gigabyte, MSI, ASRock, etc.), but the concepts are the same.*

---

## ⚙️ Step 1: Access BIOS/UEFI

First, you need to enter the motherboard's setup utility.

1.  **Power On/Restart:** Start your new PC build or restart it if you've already installed an OS.
2.  **Press Key:** Immediately and repeatedly press the designated key during startup. Common keys are:
    *   **`DEL`** (Delete)
    *   **`F2`**
    *   *(Check your motherboard manual if unsure)*
3.  **Alternative (If Windows is installed):**
    *   Click Start > Power Icon.
    *   **Hold `SHIFT`** + click **Restart**.
    *   Navigate: Troubleshoot > Advanced options > UEFI Firmware Settings > Restart.

---

## 🧭 Step 2: Initial Checks & Basic Configuration

Once inside the BIOS/UEFI:

1.  **(Optional but Recommended) Update BIOS:** If possible (using BIOS Flashback feature *before* first boot, or via USB within the BIOS later), update to the latest stable BIOS version from your motherboard manufacturer's website. This often improves compatibility and stability.
2.  **Load Optimized Defaults:** Find an option like **`Load Optimized Defaults`**, **`Load Setup Defaults`**, or similar (often on the Exit page or accessible via a function key like F5). Select it and confirm. This ensures a clean baseline.
3.  **Switch to Advanced Mode:** Most BIOS have an "EZ Mode" and an "Advanced Mode". Switch to **`Advanced Mode`** for full access (often toggled with **`F7`**, **`F2`**, or an on-screen button).
4.  **Verify Component Recognition:** Briefly check the main/overview pages to ensure your:
    *   CPU model is correctly identified.
    *   Total RAM amount is correct (speed will likely show base JEDEC speed initially).
    *   Storage drives (NVMe SSDs, SATA drives) are detected.
5.  **Set Date & Time:** Correct the system date and time if necessary (usually on the main page).

---

## 🚀 Step 3: Enable RAM Performance Profile (EXPO/XMP)

To get your RAM running at its advertised speed:

1.  **Navigate:** Go to the primary Overclocking/Tweaking section. Common names include:
    *   `AI Tweaker` (ASUS)
    *   `Tweaker` (Gigabyte)
    *   `OC` (MSI)
    *   `OC Tweaker` (ASRock)
2.  **Find Profile Setting:** Look for a setting like:
    *   `Memory Frequency`
    *   `Ai Overclock Tuner`
    *   `DRAM Profile` / `A-XMP` / `EXPO`
3.  **Select Profile:** Change the setting from `Auto` or `Disabled` to your RAM's specific profile (e.g., **`EXPO I`**, **`EXPO II`**, or **`XMP 1`**). The advertised speed and timings should appear.

---

## 💡 Step 4: Optimize Boot Time (Memory Context Restore)

Enabling EXPO/XMP can cause slow initial boots due to memory retraining. Prevent this:

1.  **Navigate Deeper:** Within the main Overclocking/Tweaking section, find a sub-menu for memory timings. Look for:
    *   `DRAM Timing Control`
    *   `Advanced DRAM Configuration`
    *   `Memory Subtimings`
2.  **Locate Settings:** Scroll down within the timings/advanced memory settings menu. You're looking for these *two* specific options (they are often near each other):
    *   **`Memory Context Restore`**
    *   **`Power Down Enable`** (or `DRAM Power Down Mode`)
3.  **Enable Both:** Change *both* settings from `Auto` (or `Disabled`) to **`Enabled`**.
    *   *Note:* Enabling `Memory Context Restore` *might* automatically enable `Power Down Enable` on some BIOS versions, but explicitly setting both is best.

    > **Why?** This tells the motherboard to save the results of its initial successful memory training and reuse them on subsequent boots, drastically speeding up the process after the *first* boot post-change.

---

## 🐢 Step 5: (Optional) Disable BIOS Fast Boot

Sometimes, the standard BIOS "Fast Boot" can interfere. Disabling it *can* paradoxically help overall boot consistency when Memory Context Restore is enabled.

1.  **Navigate:** Go to the **`Boot`** section/tab in the BIOS.
2.  **Find Setting:** Look for an option named **`Fast Boot`** or `Ultra Fast Boot`.
3.  **Disable:** Change the setting to **`Disabled`**.

---

## ✅ Step 6: Save Changes and Exit

You're done configuring the essential settings!

1.  **Navigate:** Go to the **`Exit`** section/tab.
2.  **Select:** Choose **`Save Changes and Reset`** (or `Save Changes and Exit`).
3.  **Confirm:** Confirm that you want to save the configuration. Your PC will restart.

---

## ⚠️ Important Notes

*   **First Boot After Changes:** The *very first boot* after enabling `Memory Context Restore` and saving may **still be slow**. This is normal as the board performs its final training and saves the context. Subsequent boots should be fast.
*   **Stability:** If your system becomes unstable after enabling EXPO/XMP (crashes, errors), you may need to disable the profile, update your BIOS, check RAM compatibility (QVL list on motherboard website), or manually tune timings/voltages (advanced users only).
*   **Clearing CMOS:** If you encounter boot issues after making changes, you may need to clear the CMOS/reset the BIOS to defaults (refer to your motherboard manual for the specific jumper or button).

***

Enjoy your consistently configured and faster-booting AM5 system!

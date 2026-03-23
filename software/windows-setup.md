# Windows Software Setup

This document contains a backup of the currently installed software on your machine, mirroring the VSCodium extensions format!

## Exported List

The complete list of installed software has been exported to `winget-export.json` in this directory.

Here are the primary applications detected:
*   **Utilities & System:** `7zip.7zip`, `Microsoft.PowerToys`, `Microsoft.WindowsTerminal`, `Microsoft.PowerShell`, `Logitech.GHUB`, `DeepCool.DeepCool`
*   **Development & Tools:** `Git.Git`, `VSCodium.VSCodium`, `Google.Antigravity`
*   **Productivity:** `Microsoft.Office`, `Microsoft.OneDrive`, `Obsidian.Obsidian`, `Microsoft.Teams`
*   **Creative:** `Inkscape.Inkscape`, `Canva.Affinity`, `OBSProject.OBSStudio`, `VictorIX.BlenderLauncher`
*   **Browsers:** `Google.Chrome.EXE`, `Microsoft.Edge`
*   **Gaming:** `Valve.Steam`, `EpicGames.EpicGamesLauncher`
*   **Others:** `OpenVPNTechnologies.OpenVPNConnect`, `Balena.Etcher`, `CodecGuide.K-LiteCodecPack.Standard`

*(Note: Various dependencies such as Microsoft Visual C++ Redistributables and Nvidia PhysX were also exported).*

---

## 🚀 Quick Install Scripts

You can install all these applications automatically in your new Windows 11 installation using `winget` (Windows Package Manager).

### Option 1: Using the exported JSON (Recommended)
This command reads the exact versions and dependencies exported from your current setup. Run it from `e:\new-pc-install\software`.
```powershell
winget import -i winget-export.json --accept-package-agreements --accept-source-agreements
```

### Option 2: PowerShell Loop (Just like the VSCodium extensions)
```powershell
$apps = @(
    "7zip.7zip",
    "Git.Git",
    "Microsoft.Office",
    "Obsidian.Obsidian",
    "Logitech.GHUB",
    "OpenVPNTechnologies.OpenVPNConnect",
    "Inkscape.Inkscape",
    "Google.Chrome.EXE",
    "CodecGuide.K-LiteCodecPack.Standard",
    "OBSProject.OBSStudio",
    "Valve.Steam",
    "EpicGames.EpicGamesLauncher",
    "VictorIX.BlenderLauncher",
    "Balena.Etcher",
    "VSCodium.VSCodium",
    "Google.Antigravity",
    "Microsoft.PowerToys",
    "Canva.Affinity",
    "Microsoft.Teams",
    "Microsoft.PowerShell",
    "Microsoft.WindowsTerminal",
    "DeepCool.DeepCool"
)

foreach ($app in $apps) {
    winget install --id $app --accept-package-agreements --accept-source-agreements
}
```

---

## ⚠️ Manual Installation Required

The following applications were detected on your system but are **not** available in the `winget` repository. You will need to download and install these manually:

*   **Fairlight Audio Accelerator Utility**
*   **Local AI Manager**

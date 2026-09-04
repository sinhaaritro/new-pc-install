# Phase 4: Workflow

> **Milestone**: Productive daily driver — install tools for your use case.
> **Prerequisite**: [Phase 3: Desktop](../phase-3-desktop/README.md) (functional Hyprland desktop).
> **Automation companion**: [`ansible/`](../../../ansible/README.md) Play 4
> (`make run-phase4`) applies these modules — packages, services, and the four
> named system-level artifacts only; every dotfile stays owned by your stow
> package. Profile selection, per-module flags, and `--tags` mirror the
> profile structure below.

## Choose Your Profile(s)

Pick one or more profiles based on how you'll use this system. Profiles are **independent** — you can install any combination.

| Profile | Description | Modules |
|---------|-------------|---------|
| 🛠️ [**Developer**](./profile-dev/README.md) | NeoVim, containers, DevPod, language runtimes | 5 modules |
| 🤖 [**AI**](./profile-ai/README.md) | Local inference, coding harnesses, IDE integration, agents, training | 5 modules |
| 🎮 [**Gaming**](./profile-gaming/README.md) | Steam, Proton, Heroic, MangoHud, controllers | 5 modules |
| 🎨 [**Creative**](./profile-creative/README.md) | OBS, DaVinci Resolve, media players | 3 modules |

> [!NOTE]
> Dotfiles (GNU Stow) moved to [Phase 3: Desktop](../phase-3-desktop/dotfiles-backup.md) — it is a desktop dependency (the desktop-config module stows the compositor config from `~/dotfiles`).

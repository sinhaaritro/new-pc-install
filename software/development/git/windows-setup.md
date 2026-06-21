# Git for Windows Setup & SSH Configuration

1.  **Download and install Git for Windows:**
    *   Get the installer from [git-scm.com](https://git-scm.com/).
2.  **Restore SSH Keys:**
    *   Copy your backed-up `.ssh` folder from the pre-installation step to `%USERPROFILE%\.ssh`.
3.  **Manage SSH Agent:**
    *   Open **Git Bash**.
    *   Clear any existing or stale keys from the agent:
        ```bash
        ssh-add -D
        ```
    *   Load your restored private key:
        ```bash
        ssh-add ~/.ssh/id_ed25519
        ```
        *(Note: Replace `id_ed25519` with your actual private key filename).*
    *   Verify the keys are loaded:
        ```bash
        ssh-add -l
        ```

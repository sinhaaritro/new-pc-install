# VSCodium Setup & Extensions

1. Download and install **VSCodium** from [vscodium.com](https://vscodium.com/).

## Preferred Extensions

The following are the standard extensions configured for this environment:

### Themed Icons & UI
*   `alexdauenhauer.catppuccin-noctis-icons`
*   `pkief.material-product-icons`
*   `subframe7536.theme-maple`

### Remote & Containers
*   `ms-azuretools.vscode-containers`
*   `ms-kubernetes-tools.vscode-kubernetes-tools`
*   `jeanp413.open-remote-ssh`
*   `dreamcatcher45.podmanager`

### Languages & Frameworks
*   **Python:**
    *   `ms-python.python`
    *   `ms-python.vscode-python-envs`
    *   `ms-python.debugpy`
*   **React / Web:**
    *   `dsznajder.es7-react-js-snippets`
*   **Infrastructure (Ansible/OpenTofu):**
    *   `redhat.ansible`
    *   `jborean.ansibug`
    *   `opentofu.vscode-opentofu`
*   **Other Tools:**
    *   `redhat.vscode-yaml`
    *   `mikestead.dotenv`
    *   `mermaidchart.vscode-mermaid-chart`
    *   `kilocode.kilo-code`
    *   `task.vscode-task`
    *   `tomi.xasnippets`

---

## 🚀 Quick Install Script

You can run this script in PowerShell to automatically install all the above extensions:

```powershell
$extensions = @(
    "alexdauenhauer.catppuccin-noctis-icons",
    "dreamcatcher45.podmanager",
    "dsznajder.es7-react-js-snippets",
    "jborean.ansibug",
    "jeanp413.open-remote-ssh",
    "kilocode.kilo-code",
    "mermaidchart.vscode-mermaid-chart",
    "mikestead.dotenv",
    "ms-azuretools.vscode-containers",
    "ms-kubernetes-tools.vscode-kubernetes-tools",
    "ms-python.debugpy",
    "ms-python.python",
    "ms-python.vscode-python-envs",
    "opentofu.vscode-opentofu",
    "pkief.material-product-icons",
    "redhat.ansible",
    "redhat.vscode-yaml",
    "subframe7536.theme-maple",
    "task.vscode-task",
    "tomi.xasnippets"
)

foreach ($ext in $extensions) {
    codium --install-extension $ext
}
```

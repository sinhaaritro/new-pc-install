# Antigravity Setup

1. Ensure your code editor (**Antigravity**) is installed.

## 📦 Exporting Installed Extensions

If you need to export the list of extensions currently installed in your Antigravity setup, you can run the following command in PowerShell:

```powershell
antigravity --list-extensions
```

## 🚀 Quick Install Script

You can run this script in PowerShell on your new Windows install to automatically install all of your currently preferred extensions in Antigravity:

```powershell
$extensions = @(
    "devsense.composer-php-vscode",
    "devsense.intelli-php-vscode",
    "devsense.phptools-vscode",
    "devsense.profiler-php-vscode",
    "golang.go",
    "hashicorp.terraform",
    "jborean.ansibug",
    "llvm-vs-code-extensions.vscode-clangd",
    "meta.pyrefly",
    "ms-kubernetes-tools.vscode-kubernetes-tools",
    "ms-python.debugpy",
    "ms-python.python",
    "ms-python.vscode-python-envs",
    "opentofu.vscode-opentofu",
    "redhat.ansible",
    "redhat.java",
    "redhat.vscode-yaml",
    "shopify.ruby-lsp",
    "task.vscode-task",
    "vscjava.vscode-gradle",
    "vscjava.vscode-java-debug",
    "vscjava.vscode-java-dependency",
    "vscjava.vscode-java-pack",
    "vscjava.vscode-java-test",
    "vscjava.vscode-maven",
    "zhuangtongfa.material-theme"
)

foreach ($ext in $extensions) {
    antigravity --install-extension $ext
}
```

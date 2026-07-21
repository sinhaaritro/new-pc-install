# Remote SSH & Tunneling

> **Phase**: 4 — Workflow (Developer Profile)
> **Prerequisites**: [SSH & Git](../../phase-2-system-hardening/ssh.md)
> **Packages**: `openssh`, `openbsd-netcat`, `procps-ng`

---

## Overview

Configure SSH host aliases, identity agent sockets, dynamic remote port forwarding, and an automated tunnel proxy script for Remote Explorer access (e.g., VSCodium or VS Code Remote - SSH extension).

This setup dynamically reads active `RemoteForward` directives from `~/.ssh/config` for target hosts (such as local AI inference services like llama.cpp, Ollama, or LM Studio) and maintains background SSH tunnels upon establishing remote sessions.

---

## Configuration

### Step 1: Update `~/.ssh/config`

Add host definitions using the structure below.

> [!IMPORTANT]
> - Replace `[LOCAL_USER_NAME]` with your actual local username (e.g., `aritro` or `$(whoami)`).
> - Replace `[YOUR_REMOTE_HOSTNAME]` with your remote server IP address.
> - Replace `[YOUR_REMOTE_USERNAME]` with your remote server username.
> - **Port Configuration Note**: `8080` is a common default port (e.g., for llama.cpp). If `8080` is already in use or conflicting with another service, change it to an available local/remote port as needed.

```text
# Template Configuration
# Host my-remote-server
#     HostName [YOUR_REMOTE_HOSTNAME]
#     User [YOUR_REMOTE_USERNAME]
#     Port 22
#     IdentityFile ~/.ssh/id_ed25519
#     ForwardAgent yes
#     RemoteForward 8080 127.0.0.1:8080 # Setup for port forwarding llama.cpp (change port if needed)
#     RemoteForward 11434 localhost:11434 # Setup for port forwarding Ollama
#     RemoteForward 1234 localhost:1234 # Setup for port forwarding LM Studio
#     IdentityAgent /home/[LOCAL_USER_NAME]/.ssh/ssh-agent.sock
#     ProxyCommand /home/[LOCAL_USER_NAME]/.ssh/vscodium-tunnel-proxy.sh my-remote-server %h %p

# Example
Host devserver
    HostName [IP_ADDRESS]
    User dev
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
    RemoteForward 8080 127.0.0.1:8080
    IdentityAgent /home/[LOCAL_USER_NAME]/.ssh/ssh-agent.sock
    ProxyCommand /home/[LOCAL_USER_NAME]/.ssh/vscodium-tunnel-proxy.sh devserver %h %p
```

---

### Step 2: Create Proxy Command Script

Create `~/.ssh/vscodium-tunnel-proxy.sh`. This script parses active `RemoteForward` lines for the target host in `~/.ssh/config` and ensures the background SSH tunnel process is running before passing the session to `nc` (netcat).

> [!IMPORTANT]
> - Replace `[LOCAL_USER_NAME]` with your actual local username (e.g., `aritro` or `$(whoami)`).

```bash
#!/bin/bash
# /home/[LOCAL_USER_NAME]/.ssh/vscodium-tunnel-proxy.sh

HOST_ALIAS="$1"
TARGET_HOST="$2"
TARGET_PORT="$3"

# 1. Parse all active RemoteForward rules for this specific Host block in ~/.ssh/config
# (This automatically ignores commented-out '#' lines)
forwards=$(awk -v host="$HOST_ALIAS" '
    $1 == "Host" {
        if ($2 == host) { active = 1 } else { active = 0 }
    }
    active && $1 == "RemoteForward" {
        # Format output to colon-separated (e.g., 8080:127.0.0.1:8080)
        print $2 ":" $3
    }
' ~/.ssh/config)

# 2. Build the array of -R arguments dynamically
R_ARGS=()
if [ -n "$forwards" ]; then
    while read -r rule; do
        if [ -n "$rule" ]; then
            R_ARGS+=("-R" "$rule")
        fi
    done <<< "$forwards"
fi

# 3. If active rules exist, start the background tunnel if it is not already running
if [ ${#R_ARGS[@]} -gt 0 ]; then
    # We use pgrep to check if an SSH tunnel process for this host already exists
    if ! pgrep -f "ssh -o ProxyCommand=none -f -N .* $HOST_ALIAS" > /dev/null; then
        # Added keepalive and exit on forward failure to prevent zombie processes
        ssh -o ProxyCommand=none \
            -o ServerAliveInterval=15 \
            -o ServerAliveCountMax=3 \
            -o ExitOnForwardFailure=yes \
            -f -N "${R_ARGS[@]}" "$HOST_ALIAS"
    fi
fi

# 4. Hand over the primary SSH session stream to VSCodium
nc "$TARGET_HOST" "$TARGET_PORT"
```

---

### Step 3: Set File Permissions

Ensure proper executable permissions for the script and restricted permissions for the SSH config file:

```bash
chmod +x ~/.ssh/vscodium-tunnel-proxy.sh
chmod 600 ~/.ssh/config
```

---

## Verification

Test the SSH connection and check that background forwarding processes trigger properly:

```bash
# Test SSH alias connection
ssh devserver

# Verify running background tunnel process (when active RemoteForward rules exist)
pgrep -fl "ssh -o ProxyCommand=none"
```

# Doom Scroll Blocker

## Overview
In an age where the apocalypse feels just a scroll away, it's crucial to maintain focus and mental well-being. The `Doom Scroll Blocker` is a simple, cross-platform Python utility designed to help you do just that. It temporarily blocks access to specified distracting websites by modifying your system's `hosts` file, allowing you to concentrate on more productive (or less anxiety-inducing) tasks.

## How it Works
This utility operates by adding entries to your system's `hosts` file, redirecting traffic for specified websites to `127.0.0.1` (localhost). This effectively makes those sites unreachable from your browser or other applications. When you're ready to face the digital world again, a simple command removes these entries, restoring normal access.

## Installation
1.  **Python 3.x**: Ensure you have Python 3.x installed on your system.
2.  **Clone the repository**: If you haven't already, clone the ApocalypsAI repository.
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
3.  **Navigate to the utility**: 
    ```bash
    cd utils/doom-scroll-blocker
    ```

## Usage
**Important**: This utility modifies a system file (`hosts`) and requires administrative/root privileges to run.

### 1. Block Websites
To block one or more websites, use the `start` command followed by the list of domains. The utility will add entries for both `domain.com` and `www.domain.com` (if `domain.com` was provided).

```bash
# On Linux/macOS
sudo python3 src/blocker.py start example.com news.org socialmedia.net

# On Windows (run PowerShell or Command Prompt as Administrator)
python src/blocker.py start example.com news.org socialmedia.net
```

**Example Output (start)**:
```
Blocking example.com, news.org, socialmedia.net...
Successfully updated hosts file. Remember to run 'stop' to unblock.
```

### 2. Unblock Websites
To remove the blocked entries and restore access to all previously blocked sites by this utility, use the `stop` command.

```bash
# On Linux/macOS
sudo python3 src/blocker.py stop

# On Windows (run PowerShell or Command Prompt as Administrator)
python src/blocker.py stop
```

**Example Output (stop)**:
```
Unblocking websites...
Successfully restored hosts file.
```

## Caveats
*   **Administrator/Root Privileges**: Modifying the `hosts` file requires elevated permissions. The script will likely fail without them.
*   **DNS Cache**: Your browser or operating system might cache DNS entries. If sites remain blocked after running `stop`, try clearing your browser's cache or flushing your system's DNS cache (e.g., `ipconfig /flushdns` on Windows, `sudo killall -HUP mDNSResponder` on macOS).
*   **Firewalls/Proxies**: This utility only modifies the `hosts` file. It does not bypass firewalls, proxies, or other network restrictions.

## Contributing
Feel free to contribute improvements, bug fixes, or new features! Follow the ApocalypsAI guidelines for contributions.

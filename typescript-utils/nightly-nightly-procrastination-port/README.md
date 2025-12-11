# Nightly Procrastination Portal Blocker (NPPB)

## Banish the Digital Dust Bunnies of Distraction!

Are you constantly lured into the endless void of social media, news feeds, or cat videos when you should be conquering your tasks? Fear not, brave survivor! The Nightly Procrastination Portal Blocker is here to temporarily seal off those tempting digital gateways, allowing you to focus with the unwavering resolve of a post-apocalyptic scavenger.

This whimsical CLI utility, crafted with the robust type-safety of TypeScript, modifies your system's hosts file to redirect specified distracting websites to oblivion (or rather, to your local machine), making them inaccessible for a set duration. When your focus period is over, NPPB gracefully restores your digital freedom.

## Features

*   **Temporary Blocking**: Block sites for a specified duration (e.g., 30m, 1h, 2h30m).
*   **Whimsical Feedback**: Enjoy charming messages as you block and unblock.
*   **Persistent State**: Your blocking session persists even if you close your terminal.
*   **Easy Unblocking**: A simple command to restore access anytime.
*   **Status Check**: See what portals are currently blocked and for how long.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm installed.
2.  **Install Globally**: Open your terminal and run:
    ```bash
    npm install -g nightly-procrastination-portal-blocker
    ```
    *Note: This tool modifies your system's hosts file, which often requires administrator/root privileges. You might need to run the `nppb` commands with `sudo` on Linux/macOS or an elevated command prompt on Windows.*

## Usage

The main command is `nppb`.

### 1. Block Portals

To block one or more websites for a specific duration:

```bash
# Syntax: nppb block <duration> <site1> [site2] ...
# Examples:

# Block example.com and social.net for 1 hour
sudo nppb block 1h example.com social.net

# Block news.org for 30 minutes
sudo nppb block 30m news.org

# Block multiple sites for 2 hours and 15 minutes
sudo nppb block 2h15m facebook.com twitter.com reddit.com
```

**Duration Formats:**
*   `Xs`: X seconds (e.g., `30s`)
*   `Xm`: X minutes (e.g., `15m`, `90m`)
*   `Xh`: X hours (e.g., `1h`, `2h30m`)
*   Combinations are allowed (e.g., `1h30m`, `45m30s`).

### 2. Unblock Portals

To immediately unblock all currently blocked websites and restore your hosts file:

```bash
sudo nppb unblock
```

### 3. Check Status

To see which portals are currently under lockdown and when they will be automatically unblocked:

```bash
nppb status
```

## How it Works (The Magic Behind the Curtain)

NPPB modifies your system's `hosts` file. This file maps domain names to IP addresses. By adding entries like `127.0.0.1 example.com`, it tells your computer to look for `example.com` on your own machine, effectively making it unreachable. The tool saves the original `hosts` file content and your blocking session details in a hidden configuration file (`~/.nppb/state.json` on Unix-like systems, `%USERPROFILE%/.nppb/state.json` on Windows) so it can restore everything correctly.

When the blocking duration expires, a background process (or the next time you run `nppb` commands) will detect this and automatically unblock the sites.

## Contributing

Got an idea for a new whimsical feature or found a pesky digital dust bunny (bug)? Feel free to contribute! Check the repository for details.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

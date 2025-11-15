# Doom Scroll Blocker

## Overview

In these trying times, it's easy to get lost in the endless cascade of bad news and existential dread. The `doom-scroll-blocker` is your digital shield, a simple Python utility designed to help you reclaim your focus by temporarily blocking access to specified 'doom-scrolling' websites.

Whether you're trying to concentrate on building your bunker, optimizing your survival garden, or just getting through a work sprint without falling into a news rabbit hole, this tool has your back. It works by modifying your system's `hosts` file to redirect unwanted domains to `127.0.0.1` (localhost), effectively making them unreachable.

## Features

*   **Block Websites**: Temporarily block a list of specified websites.
*   **Unblock Websites**: Easily revert changes and restore access.
*   **Self-Contained**: Pure Python, no external dependencies.
*   **Whimsical**: Helps you survive the *digital* apocalypse.

## Usage

### Prerequisites

This utility requires administrative/root privileges to modify the `hosts` file. You will need to run it with `sudo` (Linux/macOS) or as an Administrator (Windows).

### Blocking Sites

To block sites, provide a comma-separated list of domains:

```bash
python src/blocker.py block --sites example.com,news.org,socialmedia.net
```

This will block the specified sites until you explicitly unblock them or restart your system (though the `hosts` file changes are persistent until reverted).

### Unblocking Sites

To unblock all sites previously blocked by this utility:

```bash
python src/blocker.py unblock
```

This will remove all entries added by the `doom-scroll-blocker` from your `hosts` file.

## How it Works

The `blocker.py` script identifies your system's `hosts` file location. When you run `block`, it appends lines like `127.0.0.1 example.com # APOCALYPSAI_DOOM_BLOCKER` to the file. The unique comment allows the `unblock` command to precisely identify and remove only its own entries, leaving other `hosts` file configurations untouched.

## Development & Testing

To run tests, navigate to the `utils/doom-scroll-blocker` directory and execute:

```bash
python -m unittest tests/test_blocker.py
```

Tests are designed to be deterministic and offline, mocking file system operations and system calls to ensure reliability.

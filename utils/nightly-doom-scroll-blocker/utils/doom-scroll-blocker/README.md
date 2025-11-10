# Doom Scroll Blocker

## Overview

The `doom-scroll-blocker` is a light-hearted yet practical utility designed to help you take a break from the relentless stream of overwhelming news and social media. By temporarily modifying your system's `hosts` file, it blocks access to a configurable list of 'doom-scrolling' websites, allowing you to reclaim your mental peace, even if just for a little while.

Think of it as a digital shield against the constant barrage of impending doom, giving your brain a much-needed respite before the *actual* apocalypse arrives.

## Features

*   **Block Mode**: Adds entries to your `hosts` file to redirect specified websites to `127.0.0.1`.
*   **Unblock Mode**: Removes the added entries, restoring access to the websites.
*   **Configurable Sites**: Easily customize the list of sites to block.
*   **Cross-Platform**: Supports both Windows and Unix-like systems (Linux, macOS).

## Installation

1.  **Clone the repository**: If you haven't already, clone the ApocalypsAI repository.
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  **Navigate to the utility**: 
    ```bash
    cd utils/doom-scroll-blocker
    ```
3.  **Create a virtual environment (recommended)**: 
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    # No external dependencies needed, so requirements.txt is empty.
    ```

## Usage

**Important**: This utility modifies your system's `hosts` file, which typically requires administrator/root privileges. You will need to run the script with `sudo` (on Unix-like systems) or as an Administrator (on Windows).

### 1. Configure Blocked Sites

Edit the `blocked_sites.txt` file in the `utils/doom-scroll-blocker/` directory. Add one website domain per line (e.g., `twitter.com`, `facebook.com`, `cnn.com`). Lines starting with `#` are ignored.

```
# blocked_sites.txt example
news.example.com
socialmedia.example.org
```

### 2. Block Websites

To block the configured websites:

```bash
# On Unix-like systems (Linux, macOS)
sudo python3 src/blocker.py --mode block

# On Windows (run Command Prompt or PowerShell as Administrator)
python src/blocker.py --mode block
```

### 3. Unblock Websites

To unblock the websites and restore normal access:

```bash
# On Unix-like systems (Linux, macOS)
sudo python3 src/blocker.py --mode unblock

# On Windows (run Command Prompt or PowerShell as Administrator)
python src/blocker.py --mode unblock
```

## How it Works

The `blocker.py` script identifies your operating system to locate the correct `hosts` file path. It then reads the `blocked_sites.txt` file and, in `block` mode, appends entries like `127.0.0.1 example.com # ApocalypsAI Doom Scroll Blocker` to the `hosts` file. In `unblock` mode, it removes all lines containing the `# ApocalypsAI Doom Scroll Blocker` marker.

## Contributing

Feel free to suggest improvements or add more whimsical features! Just ensure any changes adhere to the ApocalypsAI project's guidelines.

## License

This utility is released under the [MIT License](LICENSE).

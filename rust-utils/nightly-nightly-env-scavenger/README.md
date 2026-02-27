# Nightly Env Scavenger

A Rust CLI tool to manage and switch between sets of environment variables, treating them as 'scavenged caches' for different project 'wasteland zones'.

In the post-apocalyptic digital landscape, managing your environment variables can be a chaotic endeavor. The `nightly-env-scavenger` helps you organize these crucial 'byte-sized relics' into named 'scavenged caches', allowing you to quickly switch between configurations for different projects or 'wasteland zones'.

## Features

*   **Store**: Capture your current environment variables into a named cache.
*   **Load**: Apply a stored cache of environment variables to your current shell session.
*   **List**: See all your available scavenged caches.
*   **Remove**: Discard a no-longer-needed cache.

## Installation

Ensure you have Rust and Cargo installed. Then, you can install `nightly-env-scavenger` directly from crates.io (once published) or build from source:

```bash
cargo install nightly-env-scavenger
```

Alternatively, to build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-env-scavenger
cargo build --release
# The executable will be in target/release/nightly-env-scavenger
# You might want to add it to your PATH, e.g., `sudo cp target/release/nightly-env-scavenger /usr/local/bin/`
```

## Usage

### `nightly-env-scavenger store <cache_name>`

Captures the current environment variables (excluding a few common system ones like `PATH`, `HOME`, `PWD`, `SHELL`, `USER`, `TERM`, `SHLVL`, `_`, `OLDPWD`) and saves them under `<cache_name>`. If a cache with that name already exists, it will be overwritten.

```bash
# Example: Store current environment as 'dev-zone-alpha'
export MY_API_KEY="abc123"
export DB_HOST="localhost"
nightly-env-scavenger store dev-zone-alpha
```

### `nightly-env-scavenger load <cache_name>`

Outputs the environment variables for the specified cache in a format suitable for `eval` in your shell. This allows you to apply the variables to your current session.

```bash
# Example: Load 'dev-zone-alpha' into the current shell
eval "$(nightly-env-scavenger load dev-zone-alpha)"

# Verify a variable was loaded
echo $MY_API_KEY
```

### `nightly-env-scavenger list`

Lists all available scavenged caches.

```bash
# Example: See all your caches
nightly-env-scavenger list
```

### `nightly-env-scavenger remove <cache_name>`

Deletes the specified scavenged cache.

```bash
# Example: Remove 'old-test-zone'
nightly-env-scavenger remove old-test-zone
```

## Configuration Storage

Caches are stored in a TOML file within your system's standard configuration directory (e.g., `~/.config/nightly-env-scavenger/profiles.toml` on Linux/macOS, or `C:\Users\<User>\AppData\Roaming\nightly-env-scavenger\profiles.toml` on Windows).

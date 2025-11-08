# Cosmic Cache Cleaner

## The Digital Dust Bunny Sweeper for Your Dev Environment

Ever felt like your disk space is mysteriously vanishing? Or that a build is failing for no good reason, and the internet suggests 'clearing your cache'? The Cosmic Cache Cleaner is here to help!

This whimsical-yet-useful utility helps you reclaim precious disk space and resolve stubborn build issues by providing a single command to purge common development caches across various language ecosystems.

## Supported Caches

*   **Python (pip)**: Clears the global pip package cache.
*   **Node.js (npm)**: Clears the global npm package cache.
*   **Node.js (yarn)**: Clears the global yarn package cache.
*   **Go (go mod cache)**: Clears the Go module download cache.

## Usage

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/cosmic-cache-cleaner/src
    ```
2.  **Run the cleaner**:
    ```bash
    python cleaner.py
    ```

The script will detect which tools are installed on your system and offer to clear their respective caches. It will print messages indicating which caches are being cleared or if a tool is not found.

## Example Output

```
--- Cosmic Cache Cleaner Initiated ---

Checking for pip... Found.
Clearing pip cache...
  Running: pip cache purge
  Output:
  Files removed: 123
  Size removed: 456 MB

Successfully cleared pip cache.

Checking for npm... Found.
Clearing npm cache...
  Running: npm cache clean --force
  Output:
  npm WARN using --force I sure hope you know what you are doing.

Successfully cleared npm cache.

Checking for yarn... Not found. Skipping yarn cache.

Checking for go... Found.
Clearing go module cache...
  Running: go clean -modcache
  Output:

Successfully cleared go module cache.

--- Cosmic Cache Cleaner Complete ---
```

## Why use it?

*   **Free up disk space**: Development caches can grow surprisingly large over time.
*   **Resolve build issues**: Corrupted or outdated cache entries can lead to cryptic errors.
*   **Simplify maintenance**: One command to rule them all, no need to remember specific commands for each tool.
*   **Whimsical satisfaction**: Feel the cosmic energy of a clean dev environment!

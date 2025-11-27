# Nightly Echo-Chamber Purifier 🌌

A whimsical utility that scans specified directories for duplicate files based on their content hash, reporting findings to help reduce digital redundancy and purify your repository's echo chamber.

## Purpose

In the sprawling digital landscape of a repository, files can sometimes multiply, creating "echoes" of identical content across different locations. These duplicates consume unnecessary space, complicate maintenance, and can lead to confusion. The Nightly Echo-Chamber Purifier helps you identify these redundant files, allowing you to consolidate or remove them and keep your repository lean and clean.

## How it Works

The utility performs a recursive scan of the specified directories. For each file encountered, it calculates a SHA256 hash of its content. Files with identical hashes are considered duplicates. The purifier then reports all groups of duplicate files, showing their paths and the shared hash.

## Usage

To run the Nightly Echo-Chamber Purifier, provide one or more directory paths as arguments:

```bash
python src/purifier.py <directory1> [directory2 ...]
```

**Example:**

```bash
python src/purifier.py . /path/to/another/project
```

This command will scan the current directory (`.`) and `/path/to/another/project` for duplicate files.

## Example Output

```
🌌 Initiating Nightly Echo-Chamber Purification... 🌌
Scanning directories: ['.', '/path/to/another/project']

🚨 Echoes detected! Duplicate files found: 🚨

Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
  - /my-repo/docs/old_notes.md
  - /my-repo/archive/notes_backup.md

Hash: f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9
  - /my-repo/assets/logo.png
  - /my-repo/branding/current_logo.png
  - /path/to/another/project/shared/logo_copy.png

Consider consolidating or removing redundant files to purify your repository.
```

If no duplicates are found:

```
🌌 Initiating Nightly Echo-Chamber Purification... 🌌
Scanning directories: ['.']

✨ No echoes found! Your digital chambers are pristine. ✨
```

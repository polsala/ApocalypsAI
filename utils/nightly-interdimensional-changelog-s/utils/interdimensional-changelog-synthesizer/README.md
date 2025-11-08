# Interdimensional Changelog Synthesizer

## Overview

The `interdimensional-changelog-synthesizer` is a whimsical-yet-useful utility designed to help maintain a clean and informative project history. It delves into the Git commit history between two specified references (e.g., tags, branches, commit hashes) and synthesizes a structured changelog, categorizing commits based on conventional commit prefixes (e.g., `feat:`, `fix:`, `chore:`).

This tool aims to automate the tedious process of compiling release notes, making it easier to understand what changes have occurred between versions.

## Usage

Run the script from your repository's root directory, providing the start and end Git references.

```bash
python src/changelog_synthesizer.py <start_ref> <end_ref>
```

### Arguments:

*   `<start_ref>`: The Git reference (commit hash, tag, branch name) from which to start analyzing commits (exclusive).
*   `<end_ref>`: The Git reference (commit hash, tag, branch name) up to which commits will be analyzed (inclusive).

### Example:

To generate a changelog between tag `v1.0.0` and the current `HEAD`:

```bash
python src/changelog_synthesizer.py v1.0.0 HEAD
```

## Output Structure

The changelog will be printed to standard output, grouped by commit type:

```
# Changelog from <start_ref> to <end_ref>

## Features

*   feat: Add new cosmic ray deflector
*   feat(api): Implement interdimensional portal API

## Bug Fixes

*   fix: Correct temporal anomaly in flux capacitor
*   fix(ui): Resolve flickering UI issue on quantum entanglement screen

## Chores

*   chore: Update dependency manifest
*   chore(docs): Refactor README for clarity

## Other Changes

*   docs: Add more details about warp drive calibration
*   refactor: Optimize subspace communication protocols
*   build: Update CI configuration for new galaxy cluster
*   perf: Improve hyperspace jump calculations
*   test: Add unit tests for new API endpoints
*   ci: Configure nightly integration tests
*   revert: Revert accidental black hole creation
*   Initial commit
```

Commits that do not match a recognized conventional prefix will be grouped under "Other Changes".

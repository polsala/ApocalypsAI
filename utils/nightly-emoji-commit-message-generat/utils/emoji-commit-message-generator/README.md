# Emoji Commit Message Generator

## Overview

A tiny Python CLI that converts a short description into a conventional git commit message prefixed with an emoji that matches the type of change (feature, bug fix, docs, refactor, test, chore, etc.).

## Installation

```bash
pip install .
```

## Usage

```bash
python -m emoji_commit_message_generator "add user login endpoint"
# Output: ✨ add user login endpoint
```

## How it works

The tool scans the description for keywords (e.g., `feat`, `fix`, `docs`) and selects a matching emoji. If no keyword matches, a generic pencil emoji is used.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```

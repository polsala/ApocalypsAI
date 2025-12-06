# Digital Doomsday Prep Kit

## Overview
In these uncertain times, ensuring your vital digital assets are safe and accounted for is paramount. The `digital-doomsday-prep-kit` is a simple, self-contained command-line utility designed to help you track important files, their backup locations, and the last time you verified their integrity. Think of it as your personal ledger for digital survival.

## Features
- **Add Assets**: Register new digital assets (e.g., 'Family Photos', 'Tax Records', 'Secret AI Schematics') and their primary backup location.
- **List Assets**: View all tracked assets, their locations, and the date of their last verification.
- **Verify Assets**: Update the 'last verified' timestamp for an asset, confirming its safety.

## Installation
This utility is self-contained. Simply navigate to the `utils/digital-doomsday-prep-kit/` directory.

## Usage
All commands are run via `python3 prep_kit.py <command> [arguments]`.

### 1. Add a new digital asset
```bash
python3 prep_kit.py add "My Secret Plans" "Encrypted USB Drive Alpha"
```

### 2. List all tracked assets
```bash
python3 prep_kit.py list
```

### 3. Verify an existing asset
```bash
python3 prep_kit.py verify "My Secret Plans"
```

## Data Storage
The utility stores its data in a JSON file named `prep_kit_data.json` within the utility's root directory. This file is automatically created and managed by the utility.

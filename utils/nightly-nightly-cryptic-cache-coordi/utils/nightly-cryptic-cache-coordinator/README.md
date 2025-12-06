# Nightly Cryptic Cache Coordinator

## Overview

In the chaotic aftermath, remembering where you stashed that last can of beans or the emergency glow sticks can be a matter of life or death. The **Nightly Cryptic Cache Coordinator** is your trusty digital ledger for all your hidden treasures. It helps you log, retrieve, and manage your secret caches with simple commands, ensuring your valuable resources are never truly lost to the sands of time (or the marauding hordes).

It stores your cache information in a local JSON file, keeping your secrets safe and sound, right where you need them.

## Features

*   **Add Cache**: Log a new hidden cache with a name, location, and a cryptic hint.
*   **List Caches**: See an overview of all your registered caches.
*   **View Cache**: Get detailed information (including the hint!) for a specific cache.
*   **Delete Cache**: Remove a cache entry once it's been plundered (or relocated).

## Usage

The utility is a Python script that can be run from the command line.

### Prerequisites

*   Python 3.6+

### Running the Coordinator

Navigate to the `src` directory and run `cache_coordinator.py` with the desired command.

```bash
python src/cache_coordinator.py --help
```

#### Add a new cache

```bash
python src/cache_coordinator.py add --name "Emergency Medkit" --location "Old Sewer Junction, Sector 7G" --hint "Under the third broken pipe, near the glowing fungi."
```

#### List all caches

```bash
python src/cache_coordinator.py list
```

#### View a specific cache

```bash
python src/cache_coordinator.py view --name "Emergency Medkit"
```

#### Delete a cache

```bash
python src/cache_coordinator.py delete --name "Emergency Medkit"
```

## Data Storage

Cache data is stored in a JSON file named `caches.json` within the `src` directory. This keeps your data local and self-contained.

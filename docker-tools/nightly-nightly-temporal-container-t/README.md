# Nightly Temporal Container Tidy

A containerized utility to chronologically defragment and tidy up your Docker images and containers, making your host feel temporally lighter.

## ✨ Whimsical Purpose

In the chaotic aftermath, even our digital infrastructure can suffer from temporal entropy. This utility acts as a digital chronomancer, sifting through the echoes of past container runs and forgotten image layers. It doesn't just "delete" them; it "chronologically re-aligns" their temporal signatures, ensuring your Docker environment is free from unnecessary temporal distortions and resource bloat. Think of it as a cosmic janitor for your container timelines!

## 🛊 Practical Utility

This tool helps you reclaim disk space and maintain a clean Docker environment by:
- Identifying and offering to remove stopped Docker containers older than a specified threshold.
- Identifying and offering to remove "dangling" Docker images (those not associated with any tagged image or container).

It provides a crucial `--dry-run` mode to preview changes before committing to any temporal re-alignments.

## 🚀 How to Use

### Prerequisites

- Docker installed and running on your system.

### 1. Build the Utility Container

First, you need to build the `nightly-temporal-container-tidy` Docker image. Navigate to the utility's directory and run:

```bash
docker build -t temporal-container-tidy .
```

### 2. Run the Utility

The utility needs access to your Docker daemon to inspect and manage containers/images. This is achieved by mounting the Docker socket (`/var/run/docker.sock`) into the container.

#### Dry Run (Recommended First!)

Always start with a dry run to see what temporal anomalies would be re-aligned:

```bash
./run.sh --dry-run
```

Or directly with `docker run`:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock temporal-container-tidy --dry-run
```

#### Force Clean (Use with Caution!)

Once you're confident with the dry run output, you can proceed with the actual temporal defragmentation:

```bash
./run.sh --force-clean
```

Or directly with `docker run`:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock temporal-container-tidy --force-clean
```

#### Customizing Container Age Threshold

By default, stopped containers older than 24 hours are considered stale. You can adjust this threshold:

```bash
./run.sh --dry-run --container-age-threshold 72 # Check for containers older than 72 hours
```

## 🧪 Automated Tests

The utility includes unit tests for its core logic, ensuring that its temporal re-alignment algorithms function as expected without requiring a live Docker daemon.

To run the tests:

1.  Ensure you have `pytest` and `docker` installed in your Python environment:
    ```bash
    pip install pytest docker
    ```
2.  Navigate to the utility's directory.
3.  Run `pytest` from the root of the utility:
    ```bash
    python -m unittest tests/test_temporal_tidy.py
    ```

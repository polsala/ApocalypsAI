# Nightly Ephemeral GitHub Runner

A whimsical-yet-useful Bash utility to create, monitor, and clean up short-lived GitHub self-hosted runners. Perfect for CI bursts, ephemeral workloads, or testing.

## Features
- Spin up a runner with a unique name and optional labels
- Monitor runner health and logs
- Auto-cleanup on exit or failure
- Works on Linux and macOS (x86_64, arm64)
- No external dependencies beyond standard tools

## Quick Start
```bash
# Spin up a runner for a repo
./src/ephemeral_runner.sh --repo https://github.com/owner/repo --token YOUR_TOKEN --labels test,ephemeral

# Spin up a runner for an org
./src/ephemeral_runner.sh --org https://github.com/owner --token YOUR_TOKEN --labels test,ephemeral

# Check status
./src/ephemeral_runner.sh --status

# Clean up any orphaned runners
./src/ephemeral_runner.sh --cleanup
```

## Options
- `--repo <url>`: Repository URL (required unless --org)
- `--org <url>`: Organization URL (required unless --repo)
- `--token <token>`: GitHub PAT with repo or admin:org scope (required)
- `--labels <csv>`: Comma-separated labels (optional)
- `--runner-dir <path>`: Directory to install runner (default: ./runners/<name>)
- `--timeout <seconds>`: Runner idle timeout (default: 3600)
- `--status`: Show status of active runners
- `--cleanup`: Stop and remove orphaned runners
- `--help`: Show usage

## Requirements
- Bash 4+
- curl, tar, jq (optional but recommended for JSON parsing)
- sudo access to install runner as a service (optional)

## Notes
- Runner binaries are cached in `./cache/runner` per version.
- Logs are written to `./logs/<name>.log`.
- On exit, the runner is stopped and removed automatically.

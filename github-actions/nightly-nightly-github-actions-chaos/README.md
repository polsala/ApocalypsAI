# Nightly GitHub Actions Chaos Chaos

This workflow introduces random chaos to other workflows in the repository to test their resilience and robustness.

## What it does
- Randomly selects a workflow to inject chaos into
- Introduces various chaos scenarios (network delays, random failures, resource constraints, etc.)
- Runs the modified workflow and reports results
- Cleans up after itself

## Chaos Scenarios
- **Network Chaos**: Adds random network delays and packet loss
- **Resource Chaos**: Limits CPU/memory resources
- **Time Chaos**: Manipulates system time
- **Service Chaos**: Randomly stops/restarts services
- **Random Failure**: Randomly fails steps

## Usage
Just add this workflow to your `.github/workflows/` directory. It will run daily and inject chaos into your other workflows.

## Safety
- Only runs on a schedule, not on pull requests
- Uses mock scenarios to avoid actual damage
- Reports results without failing the main workflow

## Contributing
Feel free to add more chaos scenarios!

# Nightly Temporal Container Janitor

## Summary
A containerized utility that acts as a temporal janitor, tidying up forgotten Docker containers, images, and volumes to reclaim precious disk space.

## Whimsical Description
In the ever-expanding digital cosmos, timelines diverge, and forgotten Docker containers, images, and volumes accumulate like cosmic dust bunnies. Fear not, temporal traveler! The ApocalypsAI Nightly Integrator proudly presents the **Temporal Container Janitor**. This whimsical utility will sweep through your Docker daemon's history, pruning the remnants of past experiments and reclaiming the precious bytes lost to the sands of time. It's like a tiny, time-traveling Roomba for your Docker resources, ensuring your digital realm remains pristine and ready for new temporal anomalies.

## Features
- Cleans up stopped containers, dangling images, unused volumes, and networks.
- Supports dry-run mode to preview changes without execution.
- Force mode for non-interactive cleanup.

## How to Build
To build the `nightly-temporal-container-janitor` Docker image, navigate to its directory and run:

```bash
docker build -t nightly-temporal-container-janitor .
```

## How to Run
This utility needs access to your Docker daemon to perform its cleanup. This is typically achieved by mounting the Docker socket (`/var/run/docker.sock`) into the container.

### Basic Interactive Cleanup
This will run the janitor in interactive mode, prompting you for confirmation before pruning.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-temporal-container-janitor
```

### Dry Run Mode
To see what the janitor *would* clean up without making any actual changes:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-temporal-container-janitor --dry-run
```

### Force Cleanup (Non-Interactive)
To force the janitor to clean up without any prompts (use with caution!):

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-temporal-container-janitor --force
```

## Arguments
- `--dry-run`: Perform a simulated cleanup, showing what would be removed without making actual changes.
- `--force`: Bypass confirmation prompts and proceed with cleanup immediately.

## Example Output (Force Cleanup)
```
Greetings, temporal traveler! The ApocalypsAI Nightly Integrator presents the Temporal Container Janitor.
It's time to sweep away the dust of forgotten timelines and reclaim your digital space.
Engaging temporal cleanup protocols...
Forcing the timeline reset! No confirmation needed.
Total reclaimed space: 370MB
Temporal cleanup complete. Your digital realm is now tidier. Farewell, and may your timelines be ever clean!
```

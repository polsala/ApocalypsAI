# Nightly Docker Dust Bunny Sweep

## Summary

The `nightly-docker-dust-bunny-sweep` is a whimsical yet useful containerized utility designed to help you keep your Docker environment tidy. It scans for common forms of digital clutter – dangling images, unused volumes, and exited containers – and presents them as 'digital dust bunnies' that need sweeping. It then provides clear, actionable `docker` commands to help you clean up your system.

## Why use this?

Over time, Docker environments can accumulate a lot of unused resources. This utility makes identifying and cleaning them up a fun and straightforward process, preventing your system from getting bogged down by forgotten artifacts.

## How it works

The utility runs a Python script inside a Docker container. This script executes various `docker` commands (e.g., `docker images`, `docker volume ls`, `docker ps`) to identify resources that are no longer in use. It then formats this information into a friendly report, complete with suggested `docker prune` or specific `docker rm` commands.

## Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t nightly-docker-dust-bunny-sweep .
    ```

2.  **Run the sweeper:**
    You need to mount the Docker socket so the container can interact with the Docker daemon on your host.
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-dust-bunny-sweep
    ```

    The output will list the detected 'dust bunnies' and provide cleanup suggestions.

### Example Output

```
✨ Initiating the Nightly Docker Dust Bunny Sweep! ✨

Oh dear, it seems some digital dust bunnies have accumulated in your Docker realm!
Let's see what we've found...

--- 🧹 Dangling Images (Forgotten Phantoms) 🧹 ---
These images are like old blueprints for projects long finished, taking up space.

  <none>              <none>              a1b2c3d4e5f6        2 weeks ago         123MB
  <none>              <none>              f6e5d4c3b2a1        3 months ago        456MB

To banish these forgotten phantoms, consider running:
  docker rmi a1b2c3d4e5f6 f6e5d4c3b2a1
  # Or, for a general sweep of all dangling images:
  docker image prune

--- 🗑️ Unused Volumes (Lost Luggage) 🗑️ ---
Volumes that aren't attached to any container, like lost luggage at a forgotten terminal.

  my_old_data_volume
  temp_logs_volume

To reclaim this lost luggage, consider running:
  docker volume rm my_old_data_volume temp_logs_volume
  # Or, for a general sweep of all unused volumes:
  docker volume prune

--- 👻 Exited Containers (Lingering Spirits) 👻 ---
Containers that have finished their work but are still hanging around, taking up minimal space but adding to the clutter.

  container_alpha (exited 0)
  container_beta (exited 137)

To bid farewell to these lingering spirits, consider running:
  docker rm container_alpha container_beta
  # Or, for a general sweep of all exited containers:
  docker container prune

--- ✨ Grand Cleanup Suggestion ✨ ---
For a comprehensive sweep of all dangling images, unused volumes, and exited containers, you can use the mighty:

  docker system prune

Remember to review the items before pruning! Happy sweeping!
```

## Development & Testing

To run the tests for the Python script logic:

1.  **Build the test image:**
    ```bash
    docker build -f tests/Dockerfile.test -t nightly-docker-dust-bunny-sweep-test .
    ```

2.  **Run the tests:**
    ```bash
    docker run --rm nightly-docker-dust-bunny-sweep-test
    ```

This will execute the `test_sweeper.py` script inside a controlled environment.

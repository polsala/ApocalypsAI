# Nightly Container Critter Catcher

## Summary
The digital wilds of your Docker daemon can sometimes get a bit... cluttered. Introducing the **Nightly Container Critter Catcher**, a whimsical utility designed to help you identify and "rehome" (clean up) those idle, stopped, or abandoned Docker containers, images, and volumes that might be lurking in the shadows. Think of it as a friendly neighborhood digital pest control, but for your containers!

## How it Works
This tool scans your Docker environment for:
1.  **Stopped Containers**: "Sleepy Critters" that are no longer running but still occupy space.
2.  **Dangling Images**: "Lost Pups" – images that aren't tagged and aren't used by any container.
3.  **Unused Volumes**: "Forgotten Nests" – volumes not attached to any active container.

It then presents you with a list of these "critters" and asks if you'd like to "rehome" them (i.e., remove them).

## Usage

### Prerequisites
-   Docker installed and running on your system.
-   The Docker daemon must be accessible by the user running the container (e.g., user is in `docker` group, or `sudo` is used).

### Running the Critter Catcher

1.  **Build the Docker Image:**
    ```bash
    docker build -t nightly-critter-catcher .
    ```

2.  **Run the Catcher:**
    To simply scan and get a report without making changes:
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock nightly-critter-catcher scan
    ```

    To scan and interactively clean up critters:
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock nightly-critter-catcher cleanup
    ```

    *Explanation of `docker run` flags:*
    -   `--rm`: Automatically remove the container when it exits.
    -   `-it`: Run in interactive mode, allowing you to see output and provide input.
    -   `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker daemon socket into the container, allowing the script inside to interact with your host's Docker daemon. **Caution: This grants the container full access to your Docker daemon. Only run trusted images.**

### Example Output (Interactive Cleanup)

```
Welcome to the Nightly Container Critter Catcher!
Scanning for digital critters...

Found 2 Sleepy Critters (stopped containers):
  - a1b2c3d4e5f6 (my-old-app)
  - f6e5d4c3b2a1 (dev-db-test)

Found 1 Lost Pup (dangling image):
  - <none>:<none> (Image ID: 789abcdef012)

Found 0 Forgotten Nests (unused volumes).

Would you like to rehome these critters? (y/N): y
Rehoming Sleepy Critter a1b2c3d4e5f6... Done!
Rehoming Sleepy Critter f6e5d4c3b2a1... Done!
Rehoming Lost Pup 789abcdef012... Done!

All identified critters have been rehomed. Your Docker environment is now a bit tidier!
```

## Development & Testing

To run tests, you need `bash` and `coreutils` (for `grep`, `sed`, `awk`, `cat`, `echo`).
The tests use a mocked `docker` command to ensure determinism and offline execution.

```bash
# From the root of the utility directory
bash tests/test_critter_catcher.sh
```

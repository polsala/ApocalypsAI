# Nightly Chrono-Container

## Summary
Executes commands within a time-locked Docker container to ensure consistent temporal environments.

## Description
In the chaotic temporal flux of the post-apocalypse, even a simple `date` command can yield wildly inconsistent results. The Nightly Chrono-Container provides a hermetically sealed, time-anchored execution environment. It uses advanced temporal stabilization techniques (read: `faketime`) within a Docker container to ensure your commands perceive a consistent, user-defined point in time, regardless of the host system's temporal shenanigans. Perfect for reproducible builds, time-sensitive data processing, or just ensuring your logs don't lie about when they were written.

## Usage
To use the Chrono-Container, simply run the host-side script `src/run-chrono-container.sh` with your desired command and an optional temporal anchor (date/time string).

```bash
./src/run-chrono-container.sh "your_command_here" ["YYYY-MM-DD HH:MM:SS"]
```

**Examples:**

1.  Run `date` command, anchoring time to a specific point:
    ```bash
    ./src/run-chrono-container.sh "date -u +%Y-%m-%d %H:%M:%S" "2077-10-23 13:37:00"
    # Expected output (or similar, depending on locale/timezone settings):
    # Chrono-Container: Anchoring time to 2077-10-23 13:37:00 for command: date -u +%Y-%m-%d %H:%M:%S
    # 2077-10-23 13:37:00
    ```

2.  Run a `git log` command, ensuring a consistent perceived commit date:
    ```bash
    ./src/run-chrono-container.sh "git log --pretty=format:'%ad' --date=iso-strict -1" "2023-01-01 00:00:00"
    # Note: For git commands operating on an actual repository, you would need to mount the repository
    # into the container using Docker's `-v` option. This utility focuses on time-locking the command's perception.
    ```

3.  Run a command without a temporal anchor (uses the container's current system time):
    ```bash
    ./src/run-chrono-container.sh "echo 'Current time inside container:' && date"
    # Expected output:
    # Chrono-Container: Running command without temporal anchor (using container's current time): echo 'Current time inside container:' && date
    # Current time inside container:
    # <Current date/time inside the container>
    ```

## How It Works
1.  The `src/run-chrono-container.sh` script first builds a Docker image based on the `Dockerfile` in the utility's root directory. This image includes `faketime` and our custom entrypoint script.
2.  It then runs a Docker container from this image, passing your command and the optional temporal anchor as arguments.
3.  Inside the container, the `src/chrono-run.sh` entrypoint script checks if a temporal anchor was provided.
4.  If an anchor is present, it sets the `FAKETIME` environment variable and uses `LD_PRELOAD` to inject the `faketime` library before executing your command. This makes your command perceive the system time as the specified temporal anchor.
5.  If no anchor is provided, the command is executed normally, using the container's actual system time.

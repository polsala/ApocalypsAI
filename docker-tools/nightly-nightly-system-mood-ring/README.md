# Nightly System Mood Ring

A whimsical-yet-useful Dockerized utility that displays a terminal "mood ring" based on host system resource utilization (CPU, Memory). It provides a quick, at-a-glance visual indicator of your system's health, changing terminal colors from calm blue to anxious yellow to fiery red as resource usage increases.

## Features

*   **Real-time Monitoring**: Continuously monitors CPU and Memory usage of the host system.
*   **Visual Feedback**: Changes terminal background and foreground colors based on predefined thresholds.
*   **Containerized**: Runs as a lightweight Docker container, easy to deploy and manage.
*   **Customizable**: Easily adjust monitoring interval and color thresholds.

## Usage

1.  **Build the Docker Image:**
    ```bash
    docker build -t system-mood-ring .
    ```

2.  **Run the Container:**
    To monitor your *host* system, you need to mount the host's `/proc` filesystem into the container.
    ```bash
    docker run --rm -it \
      -v /proc:/host_proc:ro \
      -e PROC_ROOT=/host_proc \
      system-mood-ring
    ```
    The `-it` flags are important for interactive terminal output.
    The `-v /proc:/host_proc:ro` mounts the host's `/proc` directory as read-only inside the container at `/host_proc`.
    The `-e PROC_ROOT=/host_proc` tells the script to look for `/proc` files in `/host_proc`.

    You can also specify a refresh interval (in seconds, default is 2):
    ```bash
    docker run --rm -it \
      -v /proc:/host_proc:ro \
      -e PROC_ROOT=/host_proc \
      -e INTERVAL=5 \
      system-mood-ring
    ```

3.  **Interpretation of Colors (Default):**
    *   **Blue (Calm)**: CPU < 30%, Memory < 30%
    *   **Yellow (Moderate)**: CPU 30-70%, Memory 30-70%
    *   **Red (High/Stressed)**: CPU > 70%, Memory > 70%

## Configuration (Environment Variables)

*   `INTERVAL`: Refresh interval in seconds (default: `2`).
*   `PROC_ROOT`: Path to the `/proc` filesystem (default: `/proc`). Useful for monitoring the host.
*   `CPU_LOW_THRESHOLD`: CPU usage percentage below which it's considered "low" (default: `30`).
*   `CPU_HIGH_THRESHOLD`: CPU usage percentage above which it's considered "high" (default: `70`).
*   `MEM_LOW_THRESHOLD`: Memory usage percentage below which it's considered "low" (default: `30`).
*   `MEM_HIGH_THRESHOLD`: Memory usage percentage above which it's considered "high" (default: `70`).

## How it Works

The `mood_ring.sh` script inside the container reads `/proc/stat` and `/proc/meminfo` (or the paths specified by `PROC_ROOT`). It calculates current CPU and memory utilization, then prints ANSI escape codes to change the terminal's background and foreground colors based on configurable thresholds. It then prints a status message and waits for the specified `INTERVAL` before repeating.

## Development & Testing

See the `tests/test_mood_ring.sh` script for how to run tests and mock `/proc` data.

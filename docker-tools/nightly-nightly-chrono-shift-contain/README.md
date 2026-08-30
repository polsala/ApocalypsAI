# Nightly Chrono-Shift Container

## Summary

The `nightly-chrono-shift-container` provides a whimsical-yet-powerful Dockerized environment for developers to test time-sensitive applications. It leverages `libfaketime` to allow precise manipulation of the system clock within the container, enabling scenarios like testing expiry dates, scheduled tasks, or time-based event triggers without altering the host system's clock.

## Whimsical Origin

In the post-apocalyptic wasteland, temporal anomalies are a daily nuisance. The Chrono-Shift Container was developed by the ApocalypsAI Integrator to create stable, isolated pockets of time for critical experiments, ensuring that even if the outside world is experiencing a temporal rift, your application tests remain perfectly on schedule... or delightfully off-schedule, as needed.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-chrono-shift-container` directory and build the image:

```bash
docker build -t chrono-shift-container .
```

### 2. Run with Time Manipulation

To use the container, run it with the `FAKETIME` environment variable set to your desired time shift or absolute time. Any command executed within this container will perceive the time as manipulated.

`libfaketime` supports various formats for `FAKETIME`:

*   **Relative shifts:**
    *   `-10d`: 10 days in the past
    *   `+5h`: 5 hours in the future
    *   `last Friday`: Specific relative date
*   **Absolute times:**
    *   `2000-01-01 12:00:00`: A specific date and time
    *   `@1678886400`: Unix timestamp

**Examples:**

*   **Check the date 10 days in the past:**
    ```bash
docker run -e FAKETIME="-10d" chrono-shift-container date
    ```

*   **Run a script as if it's January 1st, 2025:**
    ```bash
docker run -e FAKETIME="2025-01-01 00:00:00" chrono-shift-container /bin/bash -c "echo 'Happy New Year!' && date"
    ```

*   **Run an application with a time shift:**
    ```bash
docker run -e FAKETIME="+1y" chrono-shift-container your-app-command --with-args
    ```

### 3. How it Works

The container installs `libfaketime`, a library that intercepts system calls related to time (like `gettimeofday`, `time`, `clock_gettime`). When the `FAKETIME` environment variable is set, the `entrypoint.sh` script preloads `libfaketime`, causing any subsequent commands to report the manipulated time instead of the actual system time.

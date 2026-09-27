# Nightly System Serenity Sensor

The `nightly-serenity-sensor` is a whimsical-yet-useful Bash utility designed to provide a quick, at-a-glance report on your system's core health metrics. Instead of just raw numbers, it translates disk usage, memory consumption, CPU load, and critical service statuses into "serenity levels" with a touch of charm and helpful emojis.

Think of it as your system's personal zen master, gently nudging you when things get a bit too chaotic.

## Features

*   **Disk Serenity Check**: Monitors disk space and reports if your storage is peaceful, stressed, or critically cluttered.
*   **Memory Serenity Check**: Assesses RAM usage, letting you know if your system's thoughts are clear or if it's gasping for air.
*   **CPU Load Serenity Check**: Keeps an eye on your CPU's workload, indicating if it's gently humming along or running a marathon.
*   **Critical Service Check**: Verifies the status of essential services (e.g., `sshd`, `cron`), ensuring all vital functions are active.
*   **Whimsical Reporting**: Uses emojis and friendly messages to make system monitoring a less daunting task.
*   **Configurable Thresholds**: Easily adjust stress and critical thresholds via environment variables.

## Usage

1.  **Make the script executable**:
    ```bash
    chmod +x src/serenity_sensor.sh
    ```

2.  **Run the report**:
    ```bash
    ./src/serenity_sensor.sh
    ```

    Example output for a serene system:
    ```
    --- Nightly System Serenity Report (Tue Apr 23 10:30:00 UTC 2024) ---

      ✅ Disk Serenity: PEACEFUL. Disk space is at 10%. Plenty of room to breathe. 🧘
      ✅ Memory Serenity: PEACEFUL. Memory usage is at 20%. All thoughts are clear. ✨
      ✅ CPU Load Serenity: PEACEFUL. 1-min load average is 0.10. Gently humming along. 🎶
      Services Serenity:
        ✅ Service 'sshd': Active. All systems go! 🚀
        ✅ Service 'cron': Active. All systems go! 🚀

    ✨ Overall System Serenity: ALL IS WELL. The digital garden is thriving. Enjoy the peace! ✨
    -------------------------------------------------
    ```

    Example output for a system with concerns:
    ```
    --- Nightly System Serenity Report (Tue Apr 23 10:30:00 UTC 2024) ---

      ⚠️ Disk Serenity: STRESSED. Disk space is at 85%. Consider archiving old logs. 📦
      🚨 Memory Serenity: CRITICAL! Memory usage is at 95%! Your system is gasping for air! 🌬️
      ✅ CPU Load Serenity: PEACEFUL. 1-min load average is 0.10. Gently humming along. 🎶
      Services Serenity:
        🚨 Service 'sshd': INACTIVE! This needs attention! 🛑
        ✅ Service 'cron': Active. All systems go! 🚀

    ⚡ Overall System Serenity: CONCERNS DETECTED. Some aspects require your gentle attention. 🚧
    -------------------------------------------------
    ```

## Configuration

You can customize the thresholds and critical services by setting environment variables before running the script:

*   `DISK_THRESHOLD_CRITICAL`: Percentage of disk usage (default: `90`)
*   `DISK_THRESHOLD_STRESSED`: Percentage of disk usage (default: `80`)
*   `MEM_THRESHOLD_CRITICAL`: Percentage of memory usage (default: `90`)
*   `MEM_THRESHOLD_STRESSED`: Percentage of memory usage (default: `80`)
*   `LOAD_AVG_THRESHOLD_CRITICAL`: 1-minute load average (default: `5.0`)
*   `LOAD_AVG_THRESHOLD_STRESSED`: 1-minute load average (default: `2.0`)
*   `CRITICAL_SERVICES`: Space-separated list of service names (default: `"sshd cron"`)

**Example with custom thresholds:**
```bash
DISK_THRESHOLD_CRITICAL=95 DISK_THRESHOLD_STRESSED=85 ./src/serenity_sensor.sh
```

## Development & Testing

The utility includes a self-contained test script.

1.  **Run tests**:
    ```bash
    ./tests/test_serenity_sensor.sh
    ```

The tests use bash function mocking to simulate different system states (e.g., high disk usage, inactive services) without actually affecting your system or requiring external dependencies. This ensures deterministic and offline testing.

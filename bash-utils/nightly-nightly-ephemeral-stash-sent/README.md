# Nightly Ephemeral Stash Sentinel

A whimsical Bash utility to create temporary, self-destructing 'ephemeral stashes' (directories) with optional timed deletion or check-in reminders.

## Summary

Ever needed a temporary place for files that you *know* you'll want to clean up later, or just need a nudge to review? The Ephemeral Stash Sentinel creates a designated directory and can optionally schedule its automatic deletion after a set period, or send you a reminder to check its contents. Perfect for fleeting thoughts, temporary downloads, or mission-critical data that shouldn't linger.

## Usage

To create an ephemeral stash, simply run the script with a desired stash name and optional parameters:

```bash
./src/ephemeral_stash_sentinel.sh <stash_name> [OPTIONS]
```

### Arguments

*   `<stash_name>`: The name of the ephemeral stash directory to create. This will be created in the current working directory.

### Options

*   `-d <duration>`: Set a self-destruction timer for the stash. The directory and its contents will be automatically deleted after this duration. Format: `Xs`, `Xm`, `Xh`, `Xd` (seconds, minutes, hours, days). For example, `-d 30m` for 30 minutes, `-d 1h` for 1 hour.
*   `-r <duration>`: Set a check-in reminder. A notification will be sent (if `notify-send` is available) or logged, reminding you to review the stash. Format: `Xs`, `Xm`, `Xh`, `Xd`. For example, `-r 1h` for a reminder in 1 hour, `-r 15s` for 15 seconds.
*   `-h`: Display the help message.

## Examples

1.  **Create a simple stash:**
    ```bash
    ./src/ephemeral_stash_sentinel.sh my_secret_plans
    # Output: Ephemeral stash 'my_secret_plans' created at /path/to/my_secret_plans
    ```

2.  **Create a stash that self-destructs in 5 minutes:**
    ```bash
    ./src/ephemeral_stash_sentinel.sh temporary_notes -d 5m
    # Output: Stash 'temporary_notes' scheduled for self-destruction in 5m.
    ```

3.  **Create a stash with a reminder in 30 minutes:**
    ```bash
    ./src/ephemeral_stash_sentinel.sh review_later -r 30m
    # Output: Check-in reminder for 'review_later' scheduled in 30m.
    ```

4.  **Create a stash that self-destructs in 2 hours and reminds you in 1 hour:**
    ```bash
    ./src/ephemeral_stash_sentinel.sh urgent_task_files -d 2h -r 1h
    # Output: Stash 'urgent_task_files' scheduled for self-destruction in 2h.
    # Output: Check-in reminder for 'urgent_task_files' scheduled in 1h.
    ```

## How it Works

When you specify a deletion or reminder duration, the script launches a background process for each. These processes `sleep` for the specified duration and then execute the `rm -rf` command (for deletion) or `notify-send` (for reminders). The `disown` command ensures these background tasks continue even if your terminal session closes.

If `notify-send` (a common desktop notification utility) is not available, reminders will be logged to `~/.ephemeral_stash_sentinel_reminders.log` instead.

## Requirements

*   Bash shell
*   `mkdir`, `rm`, `sleep` (standard Unix utilities)
*   `notify-send` (optional, for desktop notifications)

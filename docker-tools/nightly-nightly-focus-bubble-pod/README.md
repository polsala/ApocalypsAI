# Nightly Focus Bubble Pod

## Summary

The `nightly-focus-bubble-pod` is a whimsical-yet-useful utility designed to help you achieve laser-like focus on a single task. It creates an ephemeral, isolated Docker container – your personal "focus bubble" – equipped with basic command-line tools (like `nano` and `cowsay`) and a persistent data directory. When you're done, the bubble vanishes, leaving only your work behind.

Think of it as a temporary, distraction-free workspace for your thoughts, coding snippets, or quick notes, without cluttering your main system.

## Features

*   **Isolated Environment**: A clean Alpine Linux container, free from your usual desktop distractions.
*   **Ephemeral**: Containers are automatically removed when you exit, keeping your system tidy.
*   **Persistent Data**: Mounts a local `focus_data` directory into the container, so your work is saved.
*   **Whimsical Welcome**: Greeted by a friendly `cowsay` message upon entry.
*   **Simple Interface**: Easy-to-use bash script for building, starting, stopping, and cleaning.

## Prerequisites

*   Docker must be installed and running on your system.
*   Bash shell.

## Usage

Navigate to the `nightly-focus-bubble-pod` directory and use the `focus-bubble.sh` script with the following commands:

### 1. Build the Focus Bubble Pod Image

This command builds the Docker image for your focus bubble. You only need to do this once, or when the `Dockerfile` changes.

```bash
./src/focus-bubble.sh build
```

### 2. Start Your Focus Bubble Pod

This command starts a new, interactive focus bubble container. It will automatically create a `./focus_data` directory in your current location if it doesn't exist, and mount it inside the container at `/app/data`. Any files you create or modify in `/app/data` within the container will persist on your host machine.

```bash
./src/focus-bubble.sh start
```

Once inside the bubble, you'll be dropped into a bash shell. You can use tools like `nano` to edit files in `/app/data`. To exit the bubble, simply type `exit`.

### 3. Stop a Running Focus Bubble Pod

If you need to stop a running bubble without exiting its shell (e.g., from another terminal), use this command. Note that the `start` command uses `--rm`, so usually, exiting the shell is enough.

```bash
./src/focus-bubble.sh stop
```

### 4. Clean Up Images and Stopped Containers

This command removes the Docker image and any lingering stopped containers associated with the Focus Bubble Pod. Your `focus_data` directory will remain untouched.

```bash
./src/focus-bubble.sh clean
```

## Example Workflow

1.  **Build the image (first time):**
    ```bash
    ./src/focus-bubble.sh build
    ```
2.  **Start a session:**
    ```bash
    ./src/focus-bubble.sh start
    # Inside the container:
    # cowsay 'Welcome to your Focus Bubble! Your thoughts are safe here. Your data is in /app/data.'
    # nano /app/data/my_focused_notes.md
    # (Ctrl+X to save and exit nano)
    # ls /app/data
    # exit
    ```
3.  **Verify data (on host):**
    ```bash
    ls focus_data/
    cat focus_data/my_focused_notes.md
    ```
4.  **Clean up the image (when no longer needed):**
    ```bash
    ./src/focus-bubble.sh clean
    ```

Enjoy your focused moments!

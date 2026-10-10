# nightly-pocket-dimension-manager

## Summary

The `nightly-pocket-dimension-manager` is a whimsical-yet-powerful containerized utility designed to help developers create, manage, and snapshot isolated, ephemeral Docker development environments. Think of them as "pocket dimensions" – self-contained universes for your projects, easily spun up, entered, snapshotted, and destroyed without cluttering your host system.

## Features

*   **`create <dimension_name> <image>`**: Conjure a new pocket dimension, initializing a dedicated Docker container and named volume.
*   **`enter <dimension_name>`**: Step into your dimension, gaining an interactive shell within its isolated environment.
*   **`run <dimension_name> <command>`**: Cast a spell (execute a command) inside a dimension without fully entering it.
*   **`snapshot <dimension_name> <snapshot_tag>`**: Freeze your dimension in time, creating a new Docker image from its current state.
*   **`list`**: Gaze upon all active pocket dimensions.
*   **`destroy <dimension_name>`**: Vanish a dimension, removing its container and associated volume.

## Usage

First, build the manager image:

```bash
docker build -t apocalypsai/pocket-dimension-manager .
```

Then, run commands by mounting your Docker socket (this allows the manager to control other Docker containers on your host):

### Create a new dimension

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/pocket-dimension-manager create my-project-dev ubuntu:latest
```

### List active dimensions

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/pocket-dimension-manager list
```

### Run a command inside a dimension

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/pocket-dimension-manager run my-project-dev "echo 'Hello from the dimension!'"
```

### Enter a dimension (interactive)

```bash
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/pocket-dimension-manager enter my-project-dev
```
*Note: The `-it` flags are crucial for interactive sessions.*

### Snapshot a dimension

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/pocket-dimension-manager snapshot my-project-dev my-project-dev:v1.0-snapshot
```

### Destroy a dimension

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/pocket-dimension-manager destroy my-project-dev
```

## Development & Testing

To run the tests, you'll need `shunit2`.

```bash
# Install shunit2 (example for Ubuntu/Debian)
# sudo apt-get update && sudo apt-get install shunit2

# Or download it manually:
# curl -s https://raw.githubusercontent.com/dspinellis/shunit2/master/shunit2 > /usr/local/bin/shunit2
# chmod +x /usr/local/bin/shunit2

./tests/test_pocket_dimension.sh
```

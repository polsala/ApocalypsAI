# Nightly Temporal Docker Echo

A containerized utility to capture and replay Docker container environment variables and volume mounts, creating 'temporal echoes' of past configurations for testing or debugging.

## 🌌 Whimsical Concept
In the ever-shifting sands of the ApocalypsAI repository, sometimes a container's past holds the key to its present woes. The `nightly-temporal-docker-echo` allows you to capture the 'echo' of a running container's environment and volume configuration, then replay it to recreate a precise moment in its temporal existence. Debugging a bug that only appears in a specific, long-gone setup? Just replay its echo!

## 🛠️ How It Works
This utility leverages `docker inspect` to extract crucial configuration details (environment variables and volume binds) from a running container. These details are then saved as a JSON 'echo' file. Later, you can use this echo to launch a new container with the exact same configuration, effectively time-warping your environment.

### Commands:
- `capture <container_name_or_id> <echo_name>`: Captures the environment and volume configuration of a live container and saves it as a named 'echo'.
- `replay <echo_name> <image_name> [command...]`: Launches a new container using the specified Docker image, applying the environment variables and volume mounts from the saved 'echo'. You can optionally override the container's default command.
- `list`: Displays all currently saved 'echoes'.
- `delete <echo_name>`: Removes a saved 'echo' configuration.

## 🚀 Usage

### 1. Build the Docker Image
First, build the `nightly-temporal-docker-echo` image. This image contains the `echo-cli.sh` script and `jq` for JSON processing.

```bash
docker build -t temporal-docker-echo .
```

### 2. Run the Utility
You'll typically run this utility as a temporary container, mounting the Docker socket to allow it to interact with your Docker daemon and a volume to persist your 'echoes'.

```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/echoes:/app/echoes \
  temporal-docker-echo <command> [arguments]
```

- `-v /var/run/docker.sock:/var/run/docker.sock`: Grants the utility access to your Docker daemon.
- `-v $(pwd)/echoes:/app/echoes`: Persists your captured echoes in a local `echoes` directory.

### Examples:

#### a) Capture an Echo
Let's say you have a running container named `my-app-container`.

```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/echoes:/app/echoes \
  temporal-docker-echo capture my-app-container my-app-prod-snapshot
```

This will create a file `echoes/my-app-prod-snapshot.json`.

#### b) List Echoes

```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/echoes:/app/echoes \
  temporal-docker-echo list
```

#### c) Replay an Echo
Now, launch a new container using the `my-app-prod-snapshot` echo with a `my-app-image:dev` image.

```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/echoes:/app/echoes \
  temporal-docker-echo replay my-app-prod-snapshot my-app-image:dev /bin/bash
```

This will start a new `my-app-image:dev` container with the environment variables and volume mounts defined in `my-app-prod-snapshot.json`, and drop you into a bash shell.

#### d) Delete an Echo

```bash
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/echoes:/app/echoes \
  temporal-docker-echo delete my-app-prod-snapshot
```

## 🧪 Testing

To run the tests, execute the `test_echo-cli.sh` script. It uses a mocked `docker` command to ensure deterministic and offline testing.

```bash
bash tests/test_echo-cli.sh
```

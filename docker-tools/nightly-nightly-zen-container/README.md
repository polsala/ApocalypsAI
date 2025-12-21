# Nightly Zen Container

A containerized, minimalist development environment designed to help you achieve focus and tranquility in your coding sessions. It provides a clean Alpine Linux base with essential tools and an optional 'Zen Mode' that displays calming affirmations.

## Features

*   **Minimalist Environment**: Based on Alpine Linux, providing a lightweight and fast development experience.
*   **Essential Tools**: Pre-installed with `bash`, `git`, `vim`, and `nano`.
*   **Zen Mode**: An optional feature that prints calming affirmations to your terminal, encouraging focus and a peaceful mindset.
*   **Isolated**: Provides a consistent development environment, free from local system clutter.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-zen-container` directory and build the Docker image:

```bash
docker build -t nightly-zen-container .
```

### 2. Run the Container

To start your zen development environment, run the container. You can either attach directly or run in detached mode and then attach.

#### Interactive Mode (Recommended)

This will start the container and immediately drop you into a bash shell. The Zen Mode will run in the background if enabled.

```bash
docker run -it --name my-zen-dev nightly-zen-container
```

#### With Zen Mode Activated

To enable the Zen Mode, set the `ZEN_MODE` environment variable to `true` when running the container:

```bash
docker run -it -e ZEN_MODE=true --name my-zen-dev-zen nightly-zen-container
```

When Zen Mode is active, you'll see a calming affirmation printed to your terminal periodically. For true auditory bliss, consider playing ambient sounds externally.

#### Detached Mode (and then attach)

```bash
docker run -d --name my-zen-dev-detached nightly-zen-container
docker attach my-zen-dev-detached
```

### 3. Stop and Remove the Container

When you're done, you can stop and remove your container:

```bash
docker stop my-zen-dev
docker rm my-zen-dev
# Or for the zen mode one:
docker stop my-zen-dev-zen
docker rm my-zen-dev-zen
```

## Configuration

*   `ZEN_MODE`: Set to `true` to activate the Zen Mode. Default is `false`.

## Development

To customize the environment or Zen Mode affirmations, modify the `Dockerfile`, `src/entrypoint.sh`, or `src/zen_mode.sh` files and rebuild the image.

## Testing

To run the automated tests for this utility, execute the `tests/test_container.sh` script:

```bash
bash tests/test_container.sh
```

This will build a test image, run a container, and verify the presence of essential tools and the functionality of the Zen Mode.

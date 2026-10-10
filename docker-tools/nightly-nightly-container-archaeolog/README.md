# Nightly Container Archaeologist

## Unearthing Forgotten Digital Artifacts

In the post-apocalyptic digital wasteland, containers can accumulate forgotten secrets, like ancient relics buried under layers of dust. The Nightly Container Archaeologist is a whimsical-yet-useful tool designed to help you excavate your running Docker containers for potential sensitive information lurking in environment variables.

It runs as a Docker container itself, connecting to your Docker daemon to inspect other running containers.

## Features

*   Scans all running Docker containers.
*   Identifies environment variables that match common secret patterns (e.g., `API_KEY`, `SECRET`, `PASSWORD`, `TOKEN`).
*   Reports findings with container details and the "artifact" (the suspicious variable name).

## Usage

To run the Container Archaeologist, you need to mount your Docker daemon socket into the container. This allows the Archaeologist to communicate with your Docker host and inspect other containers.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock polsala/nightly-container-archaeologist
```

Replace `polsala/nightly-container-archaeologist` with the actual image name once built or pushed to a registry.

### Example Output

```
Excavation Initiated: Searching for digital artifacts in running containers...

--- Artifact Found! ---
Container ID:   abcdef123456
Container Name: my-legacy-app
Image:          legacy-app:1.0
Artifact:       DB_PASSWORD (Potential secret)

--- Artifact Found! ---
Container ID:   fedcba654321
Container Name: old-api-service
Image:          api-service:2.1
Artifact:       STRIPE_API_KEY (Potential secret)

Excavation Complete: 2 digital artifacts unearthed.
```

## Development & Building

To build the Docker image locally:

```bash
docker build -t nightly-container-archaeologist .
```

Then run it as shown in the Usage section.

## How it Works

The tool uses the Docker SDK for Python to list and inspect running containers. It then iterates through their environment variables, applying a set of regex patterns to identify common secret indicators.

# Nightly Container Composter

## Whimsical Purpose
In the post-apocalyptic landscape, every byte of storage and every CPU cycle is a precious resource. The Nightly Container Composter is your automated sanitation bot, diligently sifting through the digital detritus of your Docker environment. It composts unused containers, images, volumes, and networks, turning them into valuable reclaimed space, ensuring your 'survival pods' (active containers) run lean, mean, and efficient.

Think of it as a digital gardener, pruning the overgrown vines of forgotten Docker resources to let your essential services flourish.

## Usage

This utility is designed to be run as a Docker container, ideally on a schedule (e.g., via a cron job on your host, or as part of a CI/CD pipeline).

### Prerequisites
- Docker installed and running on the host where this container will execute.
- The Docker daemon's socket (`/var/run/docker.sock`) must be mounted into the container so it can interact with the host's Docker.

### Running the Composter

To run the composter with default settings (prunes stopped containers and dangling images):

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock polsala/apocalypsai/nightly-container-composter
```

### Configuration

The composter's behavior can be customized using environment variables:

- `PRUNE_ALL_VOLUMES`: Set to `true` to prune all unused volumes. Default: `false`.
- `PRUNE_ALL_IMAGES`: Set to `true` to prune all unused images (not just dangling ones). Default: `false`.
- `PRUNE_NETWORKS`: Set to `true` to prune unused networks. Default: `false`.
- `PRUNE_BUILD_CACHE`: Set to `true` to prune the Docker build cache. Default: `false`.

**Example: Pruning everything**

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e PRUNE_ALL_VOLUMES="true" \
  -e PRUNE_ALL_IMAGES="true" \
  -e PRUNE_NETWORKS="true" \
  -e PRUNE_BUILD_CACHE="true" \
  polsala/apocalypsai/nightly-container-composter
```

### Building the Image (for development/testing)

```bash
docker build -t nightly-container-composter .
```

Then run it:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-composter
```

## How it Works

The `entrypoint.sh` script executes various `docker prune` commands based on the provided environment variables. It's designed to be idempotent and safe, using the `-f` (force) flag to avoid interactive prompts and `|| true` to ensure the script continues even if a specific prune command finds nothing to remove.

## Contributing
Feel free to suggest improvements or new pruning options! Just ensure any changes include corresponding tests.

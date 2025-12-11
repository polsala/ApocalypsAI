# Nightly Digital Dust Bunny Sweeper

## Summary
The `nightly-digital-dust-bunny-sweeper` is a whimsical, containerized utility designed to help you maintain a pristine Docker environment by identifying and optionally sweeping away "digital dust bunnies" – those forgotten, unused Docker resources that accumulate over time. Think of it as a friendly, automated custodian for your container ecosystem!

## What are Digital Dust Bunnies?
In the realm of Docker, digital dust bunnies are:
- **Dangling Images:** Image layers that are no longer tagged or referenced by any container. They're like forgotten socks behind the digital sofa.
- **Stopped Containers:** Containers that have exited and are no longer running, but still occupy disk space. They're the sleepy critters taking up space in your digital bed.
- **Unused Volumes:** Volumes that are no longer attached to any container. These are the lost treasures under the digital rug.

This utility helps you find and eliminate them, reclaiming valuable disk space and keeping your Docker setup tidy.

## Classifier
`docker-tools`

## How to Use

### 1. Build the Docker Image
First, you need to build the `nightly-digital-dust-bunny-sweeper` Docker image. Navigate to the utility's directory and run:

```bash
docker build -t nightly-digital-dust-bunny-sweeper .
```

### 2. Run in Report Mode (Default)
To simply see what digital dust bunnies are lurking without making any changes, run the container in "report" mode. This is the default behavior if no arguments are provided.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-digital-dust-bunny-sweeper
```
This command mounts your host's Docker socket into the container, allowing the script inside to interact with your Docker daemon to list resources. The `--rm` flag ensures the container is removed after it exits.

### 3. Run in Clean Mode
Once you're ready to sweep away the dust bunnies, run the container with the `clean` argument. **Use with caution, as this will remove resources!**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-digital-dust-bunny-sweeper clean
```
This will execute `docker image prune -f`, `docker container prune -f`, `docker volume prune -f`, and `docker system prune -f` (which includes network pruning) to clean up unused resources.

## Example Output (Report Mode)

```
  _   _
 ( \_/ )
  \_ _/
   (.)

Greetings, fellow digital custodian!
The Nightly Digital Dust Bunny Sweeper is commencing its rounds.
Time to banish the forgotten fluff and reclaim your digital corners!

Scanning for rogue fluffballs (dangling images)...
  Found these dusty image bunnies:
    - dangling_image_id_1
    - dangling_image_id_2

Checking for slumbering containers (stopped containers)...
  Discovered these snoozing container critters:
    - stopped_container_id_1

Peeking under the digital rug for lost treasures (unused volumes)...
  Uncovered these forgotten volume trinkets:
    - dangling_volume_id_1

To perform a full sweep and reclaim space, run this utility with the 'clean' argument:
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-digital-dust-bunny-sweeper clean
Currently in 'report' mode. No changes were made.
```

## Automated Tests

The utility includes a `tests/test_sweeper.sh` script that uses a mocked Docker environment to ensure the script's logic and output are correct without requiring a live Docker daemon.

To run the tests:
```bash
bash tests/test_sweeper.sh
```

The tests verify:
-   Correct identification and reporting of mock dangling images, stopped containers, and unused volumes in "report" mode.
-   Correct messages and execution flow for cleanup operations in "clean" mode (using mocked prune commands).

#!/bin/bash

# Whimsical ASCII Art Dust Bunny
DUST_BUNNY_ART="\n  _   _\n ( \\_/ )\n  \\_ _/\n   (.)\n"

# Whimsical ASCII Art Broom
BROOM_ART="\n    /\\\n   //\\\\\n  //  \\\\\n //____\\\\\n ||    ||\n ||    ||\n ||____||\n"

echo "$DUST_BUNNY_ART"
echo "Greetings, fellow digital custodian!"
echo "The Nightly Digital Dust Bunny Sweeper is commencing its rounds."
echo "Time to banish the forgotten fluff and reclaim your digital corners!"
echo ""

MODE=${1:-"report"} # Default to report mode

# Function to simulate docker commands for testing
# Mock rationale: We cannot run actual docker commands in a CI/CD environment without a docker daemon.
# This function allows us to simulate the output of docker commands for testing purposes,
# ensuring the script's logic and output formatting are correct without requiring a live docker setup.
mock_docker_command() {
    local cmd="$1"
    case "$cmd" in
        "docker image ls -f dangling=true -q")
            echo "dangling_image_id_1"
            echo "dangling_image_id_2"
            ;;
        "docker ps -a -f status=exited -q")
            echo "stopped_container_id_1"
            ;;
        "docker volume ls -f dangling=true -q")
            echo "dangling_volume_id_1"
            ;;
        "docker system prune -f")
            echo "Total reclaimed space: 100MB"
            ;;
        "docker image prune -f")
            echo "Total reclaimed space: 50MB"
            ;;
        "docker container prune -f")
            echo "Total reclaimed space: 20MB"
            ;;
        "docker volume prune -f")
            echo "Total reclaimed space: 30MB"
            ;;
        *)
            echo ""
            ;;
    esac
}

# Use mock_docker_command if MOCK_DOCKER is set, otherwise use actual docker
DOCKER_CMD_PREFIX=""
if [ "$MOCK_DOCKER" = "true" ]; then
    DOCKER_CMD_PREFIX="mock_"
fi

echo "Scanning for rogue fluffballs (dangling images)..."
DANGLING_IMAGES=$(${DOCKER_CMD_PREFIX}docker image ls -f dangling=true -q)
if [ -z "$DANGLING_IMAGES" ]; then
    echo "  No forgotten image lint found. Your image registry is sparkling!"
else
    echo "  Found these dusty image bunnies:"
    echo "$DANGLING_IMAGES" | while read -r id; do echo "    - $id"; done
fi
echo ""

echo "Checking for slumbering containers (stopped containers)..."
STOPPED_CONTAINERS=$(${DOCKER_CMD_PREFIX}docker ps -a -f status=exited -q)
if [ -z "$STOPPED_CONTAINERS" ]; then
    echo "  All containers are either active or gracefully departed. No sleepy heads here!"
else
    echo "  Discovered these snoozing container critters:"
    echo "$STOPPED_CONTAINERS" | while read -r id; do echo "    - $id"; done
fi
echo ""

echo "Peeking under the digital rug for lost treasures (unused volumes)..."
DANGLING_VOLUMES=$(${DOCKER_CMD_PREFIX}docker volume ls -f dangling=true -q)
if [ -z "$DANGLING_VOLUMES" ]; then
    echo "  Your volume garden is neatly tended. No wild growths!"
else
    echo "  Uncovered these forgotten volume trinkets:"
    echo "$DANGLING_VOLUMES" | while read -r id; do echo "    - $id"; done
fi
echo ""

if [ "$MODE" = "clean" ]; then
    echo "$BROOM_ART"
    echo "Initiating the grand sweep! Prepare for digital tidiness!"
    echo ""

    echo "Sweeping away dangling images..."
    ${DOCKER_CMD_PREFIX}docker image prune -f
    echo ""

    echo "Evicting stopped containers..."
    ${DOCKER_CMD_PREFIX}docker container prune -f
    echo ""

    echo "Reclaiming unused volumes..."
    ${DOCKER_CMD_PREFIX}docker volume prune -f
    echo ""

    echo "A final polish with 'docker system prune' for good measure..."
    ${DOCKER_CMD_PREFIX}docker system prune -f
    echo ""
    echo "The digital realm is now pristine! Enjoy your reclaimed space!"
else
    echo "To perform a full sweep and reclaim space, run this utility with the 'clean' argument:"
    echo "  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-digital-dust-bunny-sweeper clean"
    echo "Currently in 'report' mode. No changes were made."
fi

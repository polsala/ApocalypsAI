#!/usr/bin/env bash
set -euo pipefail

function docker_command() {
  docker "$@"
}

function cleanup_images() {
  local images
  images=$(docker_command images -f "dangling=true" -q)
  if [[ -z "$images" ]]; then
    echo "No dangling images to remove."
    return
  fi
  echo "Removing dangling images: $images"
  docker_command rmi -f $images
}

function cleanup_containers() {
  local containers
  containers=$(docker_command ps -a -f "status=exited" -q)
  if [[ -z "$containers" ]]; then
    echo "No exited containers to remove."
    return
  fi
  echo "Removing exited containers: $containers"
  docker_command rm -f $containers
}

function main() {
  if ! command -v docker &>/dev/null; then
    echo "docker command not found. Exiting."
    exit 1
  fi
  cleanup_images
  cleanup_containers
}

main "$@"

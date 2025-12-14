#!/usr/bin/env bash
set -euo pipefail

docker() {
  case "$1" in
    images)
      if [[ "$2" == "-f" && "$3" == "dangling=true" && "$4" == "-q" ]]; then
        echo -e "image1\nimage2"
      else
        echo ""
      fi
      ;;
    rmi)
      echo "Deleted $2"
      ;;
    ps)
      if [[ "$2" == "-a" && "$3" == "-f" && "$4" == "status=exited" && "$5" == "-q" ]]; then
        echo -e "container1\ncontainer2"
      else
        echo ""
      fi
      ;;
    rm)
      echo "Removed $2"
      ;;
    *)
      echo ""
      ;;
  esac
}

output=$(./src/main.sh)

expected=(
  "Removing dangling images: image1 image2"
  "Deleted image1"
  "Deleted image2"
  "Removing exited containers: container1 container2"
  "Removed container1"
  "Removed container2"
)

for i in "${!expected[@]}"; do
  if [[ "${output}" != *"${expected[$i]}"* ]]; then
    echo "Test failed: expected line '${expected[$i]}' not found in output."
    exit 1
  fi
done

echo "All tests passed."

# nightly-docker-ghost-cleaner

A whimsical Bash utility that cleans up dangling Docker images and celebrates with a ghost emoji.

## Usage

./src/main.sh

The script will:

1. Find all dangling Docker images (`docker images -f dangling=true -q`).
2. Remove them (`docker rmi <id>`).
3. Print a ghost emoji to celebrate.

## Example

$ ./src/main.sh
👻 Docker ghosts cleaned! (3 images removed)

If there are no dangling images:

$ ./src/main.sh
🕸️ No ghosts found.

## Requirements

- Bash 4.0+
- Docker CLI installed

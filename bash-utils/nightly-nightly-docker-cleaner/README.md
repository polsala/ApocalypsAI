# nightly-docker-cleaner

A whimsical yet useful Bash utility that cleans up dangling Docker images and exited containers, freeing disk space with a single command.

## Usage

```bash
./src/main.sh
```

The script will:

- List dangling images (`docker images -f "dangling=true" -q`) and remove them.
- List exited containers (`docker ps -a -f "status=exited" -q`) and remove them.
- Print a summary of actions taken.

## Requirements

- Bash 4.0 or newer
- Docker CLI installed and accessible in `$PATH`

## Testing

Run the bundled test script:

```bash
bash tests/test_main.sh
```

The test mocks the `docker` command to verify that the script correctly identifies and removes resources.

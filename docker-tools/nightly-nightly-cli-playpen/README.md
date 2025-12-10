# CLI Playpen

A Docker container with essential CLI tools and ASCII art for daily development fun.

## Usage
```bash
# Build
docker build -t cli-playpen .

# Run with interactive shell
docker run -it cli-playpen

# Or run a single command
docker run cli-playpen curl https://example.com
```

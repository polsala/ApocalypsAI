# Nightly Docker Ephemeral Runner

A containerized GitHub Actions runner that self-destructs after each job completion. Perfect for security-conscious CI/CD environments where you want fresh, isolated runners for every workflow.

## Features

- **Ephemeral by design**: Runner container terminates after each job
- **Self-healing**: Automatically spawns new runners when needed
- **Secure**: No persistent state, fresh environment every time
- **Configurable**: Easy to customize job limits and cleanup behavior
- **Lightweight**: Minimal Docker image with essential tools

## Quick Start

### Prerequisites

- Docker installed
- GitHub repository with Actions enabled
- GitHub personal access token with `repo` scope

### Basic Usage

1. **Generate a GitHub token**:
   ```bash
   # Go to GitHub Settings → Developer settings → Personal access tokens
   # Create token with 'repo' scope
   export GITHUB_TOKEN="your_token_here"
   ```

2. **Start the ephemeral runner**:
   ```bash
   docker run -d \
     --name nightly-runner \
     -e GITHUB_TOKEN="your_token_here" \
     -e GITHUB_REPO="owner/repo" \
     -e RUNNER_NAME="ephemeral-runner-$(date +%s)" \
     --restart unless-stopped \
     polsala/nightly-docker-ephemeral-runner:latest
   ```

3. **Verify the runner**:
   ```bash
   docker logs nightly-runner
   ```

### Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `GITHUB_TOKEN` | Required | GitHub personal access token |
| `GITHUB_REPO` | Required | Repository in format `owner/repo` |
| `RUNNER_NAME` | Auto-generated | Custom runner name |
| `MAX_JOBS` | `1` | Maximum jobs before self-destruction |
| `HEALTH_CHECK_INTERVAL` | `30` | Seconds between health checks |
| `JOB_TIMEOUT` | `3600` | Job timeout in seconds |

### Docker Compose

```yaml
version: '3.8'
services:
  ephemeral-runner:
    image: polsala/nightly-docker-ephemeral-runner:latest
    container_name: nightly-runner
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITHUB_REPO=${GITHUB_REPO}
      - RUNNER_NAME=ephemeral-runner-${HOSTNAME}
      - MAX_JOBS=1
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

## How It Works

1. **Registration**: Container starts, registers with GitHub Actions
2. **Job Processing**: Waits for and executes jobs
3. **Self-Destruction**: After job completion (or limit reached), container exits
4. **Auto-Recovery**: Docker restart policy spawns a fresh container

## Security Features

- **No persistent storage**: All state is lost on container exit
- **Fresh environment**: Each job gets a clean container
- **Token isolation**: GitHub token is only used for registration
- **Network isolation**: Runs in Docker's default network mode

## Monitoring

The runner logs detailed information about:

- Registration status
- Job assignments and completions
- Health check results
- Self-destruction triggers

```bash
# View real-time logs
docker logs -f nightly-runner

# Check runner status
docker ps --filter "name=nightly-runner"
```

## Troubleshooting

### Runner Not Appearing in GitHub

1. Verify GitHub token has `repo` scope
2. Check repository name format (`owner/repo`)
3. Review container logs for registration errors

### Jobs Stuck in Queue

1. Check if runner is online in GitHub Actions settings
2. Verify container is running: `docker ps`
3. Review health check logs

### Container Restarting Continuously

1. Check GitHub token validity
2. Verify network connectivity to GitHub
3. Review error logs for specific issues

## Development

### Building the Image

```bash
# Clone and build
git clone <repository>
cd nightly-docker-ephemeral-runner
docker build -t polsala/nightly-docker-ephemeral-runner:latest .
```

### Testing Locally

```bash
# Run in test mode
docker run --rm \
  -e GITHUB_TOKEN="test_token" \
  -e GITHUB_REPO="test/repo" \
  -e RUNNER_NAME="test-runner" \
  -e MAX_JOBS="1" \
  polsala/nightly-docker-ephemeral-runner:latest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:

- Check the [GitHub Issues](https://github.com/polsala/nightly-docker-ephemeral-runner/issues)
- Review the troubleshooting section above
- Ensure you're using the latest image version

---

**Note**: This is a community utility. Use at your own risk in production environments.

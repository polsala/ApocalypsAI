# Nightly Docker Ephemeral Runner

A whimsical-yet-useful Docker container that spins up as a GitHub Actions runner, completes its assigned jobs, and then self-destructs. Perfect for temporary CI/CD needs, testing environments, or just watching containers go out with a bang!

## Features

- 🚀 Spin up ephemeral runners on demand
- 🎯 Automatically terminates after job completion
- 🛡️ Secure token-based authentication
- 📦 Self-contained Docker image
- 🎉 Whimsical exit messages

## Usage

### Prerequisites

- Docker installed
- GitHub repository with Actions enabled
- GitHub personal access token with `repo` and `admin:repo_hook` permissions

### Quick Start

1. **Build the image**:

```bash
./build.sh
```

2. **Run the ephemeral runner**:

```bash
./run.sh your-github-owner your-github-repo your-github-token
```

3. **Watch it work**:

The runner will register itself, wait for jobs, execute them, and then self-destruct with a whimsical message.

### Environment Variables

- `GITHUB_OWNER`: Your GitHub organization or username
- `GITHUB_REPO`: Your repository name
- `GITHUB_TOKEN`: Your personal access token
- `RUNNER_NAME`: (Optional) Custom runner name (defaults to hostname)

### Docker Compose

For easier management, use the provided `docker-compose.yml`:

```bash
GITHUB_OWNER=your-owner GITHUB_REPO=your-repo GITHUB_TOKEN=your-token docker-compose up
```

## Development

### Building Manually

```bash
docker build -t nightly-docker-ephemeral-runner:latest .
```

### Testing

Run the test suite to ensure everything works:

```bash
./test.sh
```

## Security Notes

- The GitHub token is only used for runner registration
- The container self-destructs after use, leaving no trace
- Always use a dedicated token for ephemeral runners

## Whimsical Exit Messages

When the runner completes its job, it will exit with one of these messages:

- "Mission accomplished! This runner is now going ghost."
- "Job done! Time to fade into the digital ether."
- "All tasks complete! This runner is now obsolete."
- "Success! This runner has fulfilled its destiny."

## Contributing

Feel free to add more whimsical exit messages or improve the runner's functionality. Just make sure to run the tests!

## License

MIT - because even ephemeral things deserve love.

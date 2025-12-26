# Nightly GitHub Actions Runner Simulator

A whimsical-yet-useful utility that simulates GitHub Actions runners locally, allowing you to test your workflows without triggering real CI/CD pipelines.

## Features

- **Local Simulation**: Run GitHub Actions workflows locally without hitting GitHub's servers
- **Workflow Validation**: Test your workflow syntax and logic before committing
- **Cost Savings**: Avoid consuming GitHub Actions minutes during development
- **Offline Testing**: Works completely offline once dependencies are cached
- **Debug Mode**: Detailed logging to help troubleshoot workflow issues

## Usage

```bash
# Run a specific workflow file
./simulate_runner.sh .github/workflows/deploy.yml

# Run with debug output
./simulate_runner.sh --debug .github/workflows/test.yml

# Run with custom environment variables
./simulate_runner.sh --env-file .env.local .github/workflows/build.yml
```

## Installation

1. Clone this utility to your project
2. Make the script executable: `chmod +x simulate_runner.sh`
3. Run your workflows locally!

## Supported Actions

- Checkout actions
- Setup Node.js/Python/Go
- Cache actions
- Custom composite actions
- Matrix strategies
- Conditional steps

## Limitations

- No actual GitHub API calls
- Limited to supported action types
- No artifact uploads/downloads
- No secrets from GitHub (use local env files)

## Contributing

Add support for new actions by extending the `supported_actions` array in the script.

## License

MIT - Use freely, but test responsibly!

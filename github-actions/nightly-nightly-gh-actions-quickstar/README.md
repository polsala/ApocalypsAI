# Nightly GitHub Actions Quickstart

A utility to generate GitHub Actions workflow files with configurable job templates and security best practices.

## Features

- Generate workflow files with common job templates
- Include security best practices (no secrets in logs, proper permissions)
- Support for multiple trigger events
- Configurable job dependencies and matrix strategies
- Built-in testing for generated workflows

## Usage

```bash
# Generate a basic CI workflow
python src/main.py --template ci --output .github/workflows/ci.yml

# Generate a deployment workflow with matrix strategy
python src/main.py --template deploy --matrix os:ubuntu-latest,ubuntu-22.04 --output .github/workflows/deploy.yml

# Generate a security-focused workflow
python src/main.py --template security --security --output .github/workflows/security.yml
```

## Templates

- `ci`: Basic continuous integration workflow
- `deploy`: Deployment workflow with environment-specific jobs
- `security`: Security-focused workflow with vulnerability scanning
- `release`: Release automation workflow

## Security Features

- No secrets printed to logs
- Proper permissions configuration
- Dependency scanning enabled
- CodeQL analysis included
- Container scanning for Docker workflows

## Testing

The utility includes comprehensive tests to ensure generated workflows are valid:

```bash
python -m pytest tests/test_main.py -v
```

## Requirements

- Python 3.8+
- PyYAML library

## License

MIT

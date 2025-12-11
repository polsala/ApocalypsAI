# Nightly Chaos Config Validator

A whimsical-yet-useful Bash utility that validates configuration files against chaos engineering principles. Ensures your systems remain resilient under failure conditions by checking for common anti-patterns and resilience gaps.

## Features

- **Chaos Validation**: Checks configs for single points of failure
- **Resilience Scoring**: Rates your configuration's chaos readiness
- **Whimsical Warnings**: Delivers warnings with a touch of humor
- **Multi-Format Support**: Works with JSON, YAML, and INI configurations

## Installation

```bash
# Clone or copy the script to your system
chmod +x src/main.sh
# Run directly or add to PATH
```

## Usage

```bash
# Validate a single config file
./src/main.sh /path/to/config.yaml

# Validate multiple files
./src/main.sh /path/to/config1.yaml /path/to/config2.json

# Show help
./src/main.sh --help
```

## Output

The validator provides:
- **Resilience Score**: 0-100 rating of chaos readiness
- **Critical Issues**: Must-fix problems
- **Warnings**: Areas for improvement
- **Suggestions**: Whimsical recommendations

## Example

```bash
$ ./src/main.sh examples/web-server.yaml

=== Chaos Config Validator ===
File: examples/web-server.yaml
Resilience Score: 75/100

Critical Issues:
❌ Single point of failure: Only one database instance
❌ Missing circuit breaker configuration

Warnings:
⚠️  No timeout configured for external API calls
⚠️  Missing retry logic for network requests

Suggestions:
💡 Add at least 3 database replicas for high availability
💡 Implement exponential backoff for retries
💡 Configure health checks for all services

Remember: In chaos, we find order. In failure, we find strength! 🚀
```

## Supported Formats

- **JSON**: Standard JSON configuration files
- **YAML**: YAML configuration files
- **INI**: INI-style configuration files

## Chaos Principles Checked

1. **No Single Points of Failure**: Multiple instances for critical services
2. **Circuit Breakers**: Protection against cascading failures
3. **Timeouts**: Prevent hanging operations
4. **Retries**: Graceful handling of transient failures
5. **Health Checks**: Monitoring service availability
6. **Load Balancing**: Distribution of traffic
7. **Graceful Degradation**: Fallback mechanisms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

---

*May your systems be resilient and your chaos be controlled! 🎭*

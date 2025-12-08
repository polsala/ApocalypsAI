# Nightly Docker Chaos Garden

A whimsical-yet-useful tool for testing Docker infrastructure resilience through controlled chaos gardening. Inspired by post-apocalyptic survival scenarios, this tool randomly prunes, replants, and monitors containers to simulate harsh conditions.

## Features

- **Random Container Pruning**: Selectively removes containers to simulate resource scarcity
- **Container Replanting**: Automatically recreates essential services
- **Growth Monitoring**: Tracks container health and resource usage
- **Chaos Scenarios**: Multiple predefined chaos patterns
- **Survival Reports**: Generates detailed resilience reports

## Quick Start

```bash
# Build the chaos garden
docker build -t nightly-docker-chaos-garden .

# Run with your Docker socket mounted
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-chaos-garden

# Run with custom scenario (drought, storm, quake, or random)
docker run --rm -e CHAOS_SCENARIO=drought -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-chaos-garden
```

## Environment Variables

- `CHAOS_SCENARIO`: Type of chaos to apply (drought, storm, quake, random)
- `DRY_RUN`: Set to 'true' to simulate actions without actually modifying containers
- `REPORT_FORMAT`: Output format (json, yaml, text)

## Example Output

```
=== CHAOS GARDEN REPORT ===
Scenario: drought
Containers pruned: 3/15
Survival rate: 80%
Essential services preserved: true

Pruned containers:
- web-frontend-1
- cache-node-2
- worker-queue-3

Replanted containers:
- essential-db-1
- monitoring-agent-2
```

## Use Cases

- **Infrastructure Testing**: Validate your container orchestration resilience
- **Disaster Recovery**: Test recovery procedures under stress
- **Resource Optimization**: Identify non-essential containers
- **Team Training**: Practice incident response in controlled chaos

## Safety Notes

- Always run with `DRY_RUN=true` first to preview actions
- Ensure proper backups before running in production
- Monitor your infrastructure closely during chaos events

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/chaos-enhancement`)
3. Commit your changes (`git commit -m 'Add new chaos scenario'`)
4. Push to the branch (`git push origin feature/chaos-enhancement`)
5. Create a Pull Request

## License

MIT License - see LICENSE file for details.

---

*May your containers be resilient and your chaos be controlled.*

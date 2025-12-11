# Nightly Chaos Garden Orchestrator

A whimsical chaos engineering tool that orchestrates controlled failures across garden-themed services to test resilience. Perfect for ensuring your microservices can weather any storm in the garden of your infrastructure!

## Features

- 🌱 **Garden-themed chaos scenarios**: Network delays, resource exhaustion, service failures, and time distortions
- 🌿 **Controlled chaos**: Configurable intensity and duration
- 🌸 **Whimsical reporting**: Beautiful chaos reports with garden metaphors
- 🌺 **Easy integration**: Simple bash script that works with any service
- 🌻 **Safe defaults**: Non-destructive testing with rollback capabilities

## Installation

```bash
# Clone or copy the chaos_garden_orchestrator.sh script
chmod +x chaos_garden_orchestrator.sh
```

## Usage

### Basic Chaos

```bash
# Run a gentle chaos scenario
./chaos_garden_orchestrator.sh --scenario network-delay --intensity gentle --duration 5m

# Run a wild chaos scenario
./chaos_garden_orchestrator.sh --scenario resource-exhaustion --intensity wild --duration 2m
```

### Advanced Orchestrations

```bash
# Run multiple scenarios in sequence
./chaos_garden_orchestrator.sh --orchestrate --scenarios "network-delay,service-failure,time-warp"

# Custom chaos configuration
./chaos_garden_orchestrator.sh --config custom_chaos.yml
```

### Available Scenarios

- **network-delay**: Introduces artificial network latency
- **resource-exhaustion**: Consumes CPU/memory resources
- **service-failure**: Randomly kills and restarts services
- **time-warp**: Manipulates system time
- **random-chaos**: Unpredictable chaos events

### Intensity Levels

- **gentle**: Light chaos, minimal impact
- **moderate**: Noticeable but manageable disruption
- **wild**: Aggressive chaos for stress testing

## Configuration

Create a YAML configuration file to customize chaos scenarios:

```yaml
chaos_garden:
  scenarios:
    - name: network-delay
      intensity: moderate
      duration: 3m
      targets:
        - web-service
        - api-service
    - name: resource-exhaustion
      intensity: gentle
      duration: 2m
      targets:
        - database
  report_format: garden_report
```

## Reporting

After each chaos run, a detailed report is generated:

```
🌿 Chaos Garden Report 🌿

Scenario: Network Delay
Intensity: Moderate
Duration: 3 minutes

Affected Services:
- web-service: 🌱 150ms latency introduced
- api-service: 🌱 200ms latency introduced

Recovery Status: ✅ All services bloomed back to health

Lessons Learned:
- Load balancer handled traffic gracefully
- Timeout configurations worked as expected
- Monitoring alerts fired correctly
```

## Safety Features

- **Rollback mechanisms**: Automatic service restoration
- **Time limits**: Chaos scenarios have built-in timeouts
- **Service health checks**: Continuous monitoring during chaos
- **Emergency stop**: Ctrl+C to halt chaos immediately

## Contributing

1. Fork the repository
2. Create a new chaos scenario
3. Add tests for your scenario
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

Use this tool responsibly in controlled environments. The authors are not responsible for any unintended consequences of chaos engineering gone wrong.

---

*Remember: A garden needs both sunshine and storms to grow strong. Happy chaos gardening! 🌈🌻*

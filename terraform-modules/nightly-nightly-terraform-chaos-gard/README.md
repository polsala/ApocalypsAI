# Nightly Terraform Chaos Garden

A whimsical-yet-useful Terraform module that introduces controlled chaos into your cloud infrastructure for resilience testing. Inspired by chaos engineering principles, this module randomly applies "chaos events" to your resources to ensure they can handle unexpected failures.

## Features

- **Random Chaos Events**: Introduces temporary failures, latency, and resource constraints
- **Configurable Chaos**: Set chaos level from 0 (no chaos) to 10 (maximum chaos)
- **Safe Defaults**: Chaos events are temporary and bounded
- **Whimsical Events**: Includes fun chaos events like "Cosmic Ray Strike" and "Quantum Entanglement"
- **Cloud Agnostic**: Works with AWS, GCP, Azure, and other providers

## Usage

```hcl
module "chaos_garden" {
  source = "./modules/chaos-garden"
  
  chaos_level = 5  # Scale of 0-10
  
  # Resources to protect from chaos
  protected_resources = [
    "production-db",
    "critical-api"
  ]
  
  # Chaos schedule (optional)
  chaos_schedule = "0 2 * * *"  # Daily at 2 AM
}
```

## Chaos Events

- **Network Latency**: Adds artificial delay to network requests
- **CPU Spike**: Temporarily increases CPU usage
- **Memory Pressure**: Consumes available memory
- **Disk I/O Slowdown**: Slows disk operations
- **Cosmic Ray Strike**: Random bit flips (simulated)
- **Quantum Entanglement**: Random resource state changes
- **Solar Flare**: Temporary service interruption
- **Meteor Shower**: Multiple simultaneous failures

## Safety Considerations

- Chaos events are **disabled by default** (chaos_level = 0)
- Always test in development environments first
- Use protected_resources to exclude critical infrastructure
- Monitor your systems during chaos experiments

## License

MIT - Use responsibly and have fun! 🎭

# Nightly Terraform Chaos Garden Orchestrator

A whimsical-yet-useful Terraform module that creates a chaos garden orchestrator in AWS. Perfect for testing your infrastructure's resilience with configurable chaos scenarios.

## Features

- Creates an AWS ECS cluster with Fargate tasks
- Configurable chaos scenarios (network latency, CPU stress, random failures)
- Whimsical resource naming ("ChaosGarden", "MayhemOrchestrator")
- Automated cleanup after chaos runs
- Comprehensive monitoring and logging

## Usage

```hcl
module "chaos_garden" {
  source = "./modules/chaos-garden"
  
  # Basic configuration
  environment = "staging"
  chaos_duration = "30m"
  
  # Chaos scenarios
  enable_network_chaos = true
  network_latency_ms = 200
  enable_cpu_chaos = true
  cpu_stress_duration = "10m"
  enable_random_failures = true
  failure_rate = 0.1
  
  # Whimsical settings
  whimsy_level = "high"
  chaos_garden_name = "TheWhimsicalWasteland"
}
```

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `environment` | Environment name for tagging | `"staging"` |
| `chaos_duration` | How long chaos runs | `"30m"` |
| `enable_network_chaos` | Enable network latency chaos | `true` |
| `network_latency_ms` | Network latency in milliseconds | `200` |
| `enable_cpu_chaos` | Enable CPU stress chaos | `true` |
| `cpu_stress_duration` | CPU stress duration | `"10m"` |
| `enable_random_failures` | Enable random task failures | `true` |
| `failure_rate` | Probability of random failures (0.0-1.0) | `0.1` |
| `whimsy_level` | Whimsy level: "low", "medium", "high" | `"high"` |
| `chaos_garden_name` | Name for your chaos garden | `"TheWhimsicalWasteland"` |

## Outputs

| Output | Description |
|--------|-------------|
| `chaos_cluster_id` | ECS cluster ID for chaos tasks |
| `chaos_task_definition` | ARN of the chaos task definition |
| `chaos_schedule_rule` | CloudWatch Events rule for chaos scheduling |

## Safety Notes

⚠️ **Warning**: This module intentionally introduces chaos into your infrastructure. Use only in non-production environments!

- Always test in a sandbox environment first
- Set appropriate chaos durations
- Monitor your resources during chaos runs
- Use the whimsy_level to control how chaotic things get

## License

MIT License - Use responsibly and with appropriate chaos!

---

*May your infrastructure be resilient and your chaos be controlled.*

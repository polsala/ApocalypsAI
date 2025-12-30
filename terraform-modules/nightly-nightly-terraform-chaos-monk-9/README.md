# Nightly Terraform Chaos Monkey

A Terraform module that introduces controlled chaos into your infrastructure by randomly destroying and recreating resources. Inspired by Netflix's Chaos Monkey, this module helps test your infrastructure's resilience and recovery mechanisms.

## Features

- Randomly selects resources for destruction based on configurable probability
- Supports multiple cloud providers (AWS, GCP, Azure)
- Configurable chaos windows and resource exclusion lists
- Comprehensive logging and reporting
- Safe mode for testing without actual destruction

## Usage

### Basic Configuration

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos monkey
  enabled = true
  
  # 10% chance of destroying a resource during each apply
  destruction_probability = 0.1
  
  # Only run chaos during business hours (UTC)
  chaos_window_start = "09:00"
  chaos_window_end   = "17:00"
  
  # Exclude critical resources from chaos
  excluded_resources = [
    "production-database",
    "backup-storage"
  ]
}
```

### Provider Configuration

```hcl
# AWS Configuration
provider "aws" {
  region = "us-west-2"
}

# GCP Configuration
provider "google" {
  project = "my-project"
  region  = "us-central1"
}

# Azure Configuration
provider "azurerm" {
  features {}
}
```

## Variables

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `enabled` | Enable/disable chaos monkey | `bool` | `false` |
| `destruction_probability` | Probability (0.0-1.0) of destroying a resource | `number` | `0.05` |
| `chaos_window_start` | Start time for chaos window (HH:MM format) | `string` | `"00:00"` |
| `chaos_window_end` | End time for chaos window (HH:MM format) | `string` | `"23:59"` |
| `excluded_resources` | List of resource names to exclude from chaos | `list(string)` | `[]` |
| `safe_mode` | Run in safe mode (no actual destruction) | `bool` | `true` |
| `log_level` | Logging level (DEBUG, INFO, WARN, ERROR) | `string` | `"INFO"` |

## Outputs

| Output | Description |
|--------|-------------|
| `chaos_events` | List of chaos events that occurred |
| `resources_destroyed` | Count of resources destroyed |
| `resources_recreated` | Count of resources recreated |

## Safety Considerations

⚠️ **WARNING**: This module is designed to destroy infrastructure. Use extreme caution:

1. **Always test in development environments first**
2. **Use safe mode** (`safe_mode = true`) to preview chaos without destruction
3. **Exclude critical resources** using the `excluded_resources` variable
4. **Monitor your infrastructure** during chaos windows
5. **Ensure you have proper backups and recovery procedures**

## Examples

### Development Environment

```hcl
module "dev_chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  enabled               = true
  destruction_probability = 0.2
  safe_mode             = true  # Preview only
  excluded_resources    = []
}
```

### Production Environment (Minimal Chaos)

```hcl
module "prod_chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  enabled               = true
  destruction_probability = 0.01  # Very low probability
  chaos_window_start    = "02:00"  # Off-peak hours
  chaos_window_end      = "04:00"
  safe_mode             = false
  excluded_resources    = [
    "production-db",
    "load-balancer",
    "monitoring-system"
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

This is a community project. For issues and feature requests, please use the GitHub issue tracker.

---

*Remember: With great power comes great responsibility. Use chaos wisely!*

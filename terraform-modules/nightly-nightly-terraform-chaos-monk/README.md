# Nightly Terraform Chaos Monkey

A whimsical-yet-useful Terraform module that introduces controlled chaos into your cloud infrastructure by randomly terminating resources to test resilience and chaos engineering practices.

## Features

- Randomly selects resources to terminate based on configurable probability
- Supports multiple cloud providers (AWS, GCP, Azure)
- Includes safety mechanisms to prevent catastrophic failures
- Generates detailed reports of chaos events
- Whimsical ASCII art and messages for team morale

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Configure chaos probability (0.0 to 1.0)
  chaos_probability = 0.1
  
  # Resource types to target
  target_resource_types = ["aws_instance", "aws_rds_instance"]
  
  # Safety exclusions
  excluded_tags = {
    environment = "production"
    critical    = "true"
  }
}
```

## Safety First

This module includes several safety mechanisms:
- Exclusion tags to protect critical resources
- Time-based chaos windows (only runs during business hours)
- Resource count limits to prevent mass destruction
- Detailed logging and reporting

## Whimsical Features

- ASCII art chaos monkey on each execution
- Random chaos quotes and messages
- "Monkey mood" indicator for team morale
- Chaos event celebration messages

## Installation

1. Clone this repository
2. Navigate to the chaos-monkey module
3. Run `terraform init` and `terraform apply`

## License

MIT License - Use responsibly and at your own risk!

---

> "Chaos isn't a pit. Chaos is a ladder. And sometimes, chaos is a monkey with a banana."

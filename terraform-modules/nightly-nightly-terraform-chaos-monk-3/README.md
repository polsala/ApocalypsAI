# Nightly Terraform Chaos Monkey

A whimsical-yet-useful Terraform module that introduces controlled chaos by randomly terminating cloud resources to test your system's resilience and chaos engineering practices.

## Features

- Randomly selects resources from your infrastructure
- Configurable chaos intervals and resource types
- Safety mechanisms to prevent total destruction
- Comprehensive logging and reporting
- Supports AWS, GCP, and Azure resources

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  # Enable chaos engineering
  chaos_enabled = true
  
  # Configure chaos intervals (in minutes)
  chaos_interval = 60
  
  # Resource types to target
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance",
    "gcp_compute_instance"
  ]
  
  # Safety mechanisms
  protected_resources = [
    "production-db",
    "critical-api"
  ]
  
  # Maximum resources to terminate per cycle
  max_destructions_per_cycle = 2
  
  # Chaos schedule (cron format)
  chaos_schedule = "0 */2 * * *" # Every 2 hours
}
```

## Safety Features

- **Protected Resources**: Specify resources that should never be destroyed
- **Destruction Limits**: Control maximum resources terminated per chaos cycle
- **Dry Run Mode**: Preview chaos actions before execution
- **Time Windows**: Restrict chaos to specific hours
- **Emergency Stop**: Quick disable mechanism

## Installation

1. Clone this repository
2. Navigate to the chaos-monkey module
3. Run `terraform init`
4. Configure your cloud provider credentials
5. Apply the module to your infrastructure

## Monitoring

The module creates CloudWatch/Stackdriver logs showing:
- Which resources were selected for chaos
- Destruction timestamps
- Safety checks that passed/failed
- Chaos effectiveness metrics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - Use responsibly and with proper safeguards!

## Disclaimer

This tool is designed for testing resilience in controlled environments. Use at your own risk and ensure proper backups and recovery procedures are in place.

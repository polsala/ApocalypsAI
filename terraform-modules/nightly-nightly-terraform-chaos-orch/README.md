# Nightly Terraform Chaos Orchestrator

A whimsical-yet-useful Terraform module that creates and destroys cloud resources on a schedule to test resilience and chaos engineering practices.

## Features
- Creates random cloud resources (instances, storage buckets, databases)
- Destroys resources after a configurable time period
- Supports multiple cloud providers (AWS, GCP, Azure)
- Includes automated tests with mock providers
- Perfect for testing disaster recovery and chaos engineering

## Usage

```hcl
module "chaos_orchestrator" {
  source = "./modules/chaos_orchestrator"
  
  # Configuration options
  chaos_schedule = "0 2 * * *"  # Daily at 2 AM
  resource_ttl   = "24h"
  max_resources  = 10
  providers      = ["aws", "gcp"]
}
```

## Testing

Run the automated tests:

```bash
cd tests
terraform init
terraform plan
```

## License

MIT

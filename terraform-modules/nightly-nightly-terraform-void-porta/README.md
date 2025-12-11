# Nightly Terraform Void Portal

A whimsical yet useful Terraform module that creates a 'void portal' infrastructure resource for tracking and managing cloud resources across providers.

## Features

- Creates a cross-cloud resource tracker
- Generates unique portal identifiers
- Provides resource inventory and cleanup capabilities
- Supports AWS, GCP, and Azure (extensible)

## Usage

```hcl
module "void_portal" {
  source = "./modules/nightly-terraform-void-portal"
  
  portal_name = "apocalypsis-gateway"
  providers = ["aws", "gcp", "azure"]
  
  # Optional: enable resource tracking
  track_resources = true
  
  # Optional: cleanup after 30 days
  auto_cleanup_days = 30
}
```

## Outputs

- `portal_id`: Unique identifier for your void portal
- `tracked_resources`: List of tracked resources across providers
- `cleanup_schedule`: Cron expression for automatic cleanup

## License

MIT - Use responsibly when traversing the void!

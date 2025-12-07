# Nightly Terraform Chaos Garden

A whimsical Terraform module that creates a garden of chaos resources for testing infrastructure resilience and disaster recovery scenarios.

## Features

- Creates a variety of AWS resources with intentional chaos patterns
- Configurable chaos levels (low, medium, high)
- Includes resource dependencies to test cascading failures
- Whimsical naming scheme (e.g., 'chaotic-rose', 'anarchic-oak')
- Built-in cleanup mechanisms

## Usage

```hcl
module "chaos_garden" {
  source = "./modules/chaos-garden"
  
  chaos_level = "medium"
  environment = "test"
  
  # Optional: specify which chaos patterns to enable
  enable_network_chaos = true
  enable_compute_chaos = true
  enable_storage_chaos = false
}
```

## Chaos Patterns

- **Network Chaos**: Creates security groups with random port openings
- **Compute Chaos**: Spawns instances with varying resource constraints
- **Storage Chaos**: Creates S3 buckets with unusual naming and permissions
- **Dependency Chaos**: Builds interconnected resources that test failure propagation

## Safety

- Resources are tagged with `chaos_garden=true` for easy identification
- Includes `destroy_after_hours` parameter to auto-cleanup
- Designed for testing environments only

## License

MIT

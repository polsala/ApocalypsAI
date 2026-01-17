# nightly-terraform-chaos-lab

A Terraform module that introduces controlled chaos into your cloud infrastructure for resilience testing.

## Features

- Randomly selects and destroys a specified percentage of resources
- Supports AWS, Azure, and GCP
- Configurable destruction percentage and resource tags
- Dry-run mode for testing

## Usage

```hcl
module "chaos_lab" {
  source = "./nightly-terraform-chaos-lab"

  providers = {
    aws = aws
  }

  resource_tags = {
    Environment = "test"
    ChaosReady  = "true"
  }

  destruction_ratio = 0.3
  dry_run           = false
}
```

## Inputs

| Name               | Description                                | Type     | Default |
|--------------------|--------------------------------------------|----------|---------|
| resource_tags      | Tags to identify chaos-ready resources     | map(any) | n/a     |
| destruction_ratio  | Ratio of resources to destroy (0.0 - 1.0)  | number   | 0.5     |
| dry_run            | Enable dry-run mode (no actual deletion)   | bool     | true    |

## Outputs

None.

## License

MIT

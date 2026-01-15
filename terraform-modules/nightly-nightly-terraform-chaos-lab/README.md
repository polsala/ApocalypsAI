# nightly-terraform-chaos-lab

A Terraform module that introduces controlled chaos into your infrastructure for resilience testing. It randomly selects and destroys a specified percentage of resources during apply.

## Features

- Simulates random infrastructure failures
- Configurable destruction rate
- Supports major cloud providers (AWS, GCP, Azure)
- Safe mode with dry-run option

## Usage

```hcl
module "chaos_lab" {
  source = "./nightly-terraform-chaos-lab"

  enabled         = true
  destruction_rate = 0.3 # 30% of resources may be destroyed
  resource_tags   = {
    chaos-enabled = "true"
  }
}
```

## Providers

- AWS
- Google Cloud
- AzureRM

## Notes

> ⚠️ This module is intended for testing environments only. Never use in production.

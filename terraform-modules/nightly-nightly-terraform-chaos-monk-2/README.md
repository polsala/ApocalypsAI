# Nightly Terraform Chaos Monkey

A Terraform module that introduces controlled chaos by randomly destroying and recreating cloud resources to test your infrastructure's resilience.

## Features
- Randomly selects resources to destroy/recreate
- Configurable chaos intensity
- Safe mode for testing
- Supports AWS, GCP, and Azure resources

## Usage

```hcl
module "chaos_monkey" {
  source = "./modules/chaos-monkey"
  
  enabled = true
  intensity = 0.1  # 10% chance per resource
  resources = [
    "aws_instance.web",
    "aws_db_instance.main"
  ]
  safe_mode = false
}
```

## Safety
- Always test in safe mode first
- Use with infrastructure-as-code
- Monitor your resources during chaos

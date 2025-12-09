Chaos Sandbox Terraform Module
===========================

Creates isolated AWS environment with:
- Randomized resource names
- Auto-deletion after 24h
- Network segmentation
- Chaos engineering hooks

Usage:
```hcl
module "chaos_sandbox" {
  source = "./nightly-chaos-sandbox-terraform"
  owner = "dev-team"
  environment = "test"
}
```

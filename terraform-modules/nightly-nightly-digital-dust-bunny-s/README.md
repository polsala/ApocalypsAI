## Digital Dust Bunny Sweeper

A Terraform module that provisions a cloud resource cleanup scheduler with playful ASCII art and whimsical logging. Prevents digital dust bunnies by automatically removing unused resources.

### Usage
```hcl
module "dust_bunny" {
  source = "./digital-dust-bunny-sweeper"
  schedule = "0 2 * * *"
  retention_days = 7
}
```

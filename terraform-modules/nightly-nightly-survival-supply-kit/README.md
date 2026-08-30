# Nightly Survival Supply Kit Terraform Module

## Overview
A whimsical Terraform module that, given a `supply_type` (e.g., `water`, `food`, `medicine`), outputs a list of recommended survival items. No real cloud resources are created; the module is pure locals and outputs, making it safe to run anywhere.

## Usage
```hcl
module "survival_kit" {
  source      = "./src"
  supply_type = "food"
}

output "items" {
  value = module.survival_kit.items
}
```
Running `terraform init` and `terraform apply` will produce an output like:
```
items = [
  "canned beans",
  "energy bars",
]
```

## Variables
- `supply_type` (string, default = "water"): Type of supplies you need.

## Outputs
- `items` (list(string)): List of recommended items.

## Testing
Run the provided Bash test:
```sh
cd tests && bash test_module.sh
```

# Nightly Apocalypse Safehouse Terraform Module

## Overview

This Terraform module creates a playful "post‑apocalypse safe‑house" on any cloud that supports the generic `null` provider. It generates a random pet‑style name, a unique ID, and tags the resources with a whimsical "radiation_shield" attribute.

## Usage

```hcl
module "safehouse" {
  source = "./"
}
```

Run `terraform init && terraform apply` to see the generated resources.

## Resources

- `random_pet.name` – random safe‑house name.
- `random_id.id` – unique identifier.
- `null_resource.radiation_shield` – placeholder representing a shield.

## Outputs

- `safehouse_name` – The generated safe‑house name.
- `safehouse_id` – The unique identifier.

## Testing

```sh
cd tests && ./validate.sh
```

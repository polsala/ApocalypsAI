# Nightly Safehouse Terraform Module

A whimsical Terraform module that creates a mock "safe‑house" for post‑apocalyptic simulations. It uses only the `null` and `random` providers, so it works entirely offline.

## Usage

```hcl
module "safehouse" {
  source = "github.com/yourorg/apocalypsai//terraform-modules/nightly-safehouse-module"
  name   = "my‑refuge"
}
```

## Inputs

- `name` (string) – Name of the safe‑house. Default: `"safehouse"`.

## Outputs

- `shelter_id` – Random identifier for the safe‑house.

## Testing

Run the provided test script:

```sh
cd terraform-modules/nightly-safehouse-module
bash tests/test_module.sh
```

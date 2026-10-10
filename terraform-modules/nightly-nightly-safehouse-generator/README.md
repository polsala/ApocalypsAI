# Nightly Safehouse Generator

Utility Terraform module that creates a whimsical "safehouse" for post‑apocalyptic survivors. It generates a random, memorable name using the `random_pet` provider and creates a local file with that name. The module outputs the safehouse name and the path to the file.

## Usage

```hcl
module "safehouse" {
  source = "./"
}
```

Run `terraform init` and `terraform apply` to create the safehouse file.

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| `directory` | Directory where the safehouse file will be created | string | `"./safehouse"` |

## Outputs

| Name | Description |
|------|-------------|
| `safehouse_name` | The generated safehouse name |
| `safehouse_path` | Full path to the created safehouse file |

## Testing

Run `./tests/test_module.sh` to verify the module validates and creates the expected resources.

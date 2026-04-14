# Terraform Random Pet Name Module

Generates a whimsical pet name using the `random_pet` provider. Optionally prepend a prefix.

## Usage

```hcl
module "pet_name" {
  source      = "./"
  name_prefix = "myapp"
}

output "pet_name" {
  value = module.pet_name.pet_name
}
```

## Inputs

- `name_prefix` (string, optional): Prefix to prepend to the generated name.

## Outputs

- `pet_name` (string): Generated pet name, e.g., `myapp-fluffy-bunny`.

## Testing

Run the validation script to ensure the module is syntactically correct:

```bash
./tests/validation_test.sh
```

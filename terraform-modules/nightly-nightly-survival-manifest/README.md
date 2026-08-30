# nightly-survival-manifest

Terraform module that creates a local JSON file representing a survival kit manifest.

## What it does

- Takes a map of item names to quantities.
- Generates `manifest.json` in the module directory using the `local_file` resource.
- Provides an output with the path to the generated file.

## Usage

```hcl
module "survival_manifest" {
  source = "./nightly-survival-manifest"
  items = {
    water        = 10
    canned_food  = 20
    first_aid_kit = 1
    flashlight   = 2
  }
}

output "manifest_path" {
  value = module.survival_manifest.manifest_path
}
```

Run the usual Terraform commands:

```bash
terraform init -backend=false
terraform apply -auto-approve
```

The module will create `manifest.json` containing something like:

```json
{"water":10,"canned_food":20,"first_aid_kit":1,"flashlight":2}
```

## Testing

A simple test script is provided under `tests/validate.sh`. It runs `terraform init`, `validate`, `apply` and checks that the file exists and contains the expected default content.

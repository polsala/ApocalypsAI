# Nightly Terraform Cryptic Forest

## Overview

`nightly-terraform-cryptic-forest` is a playful Terraform module that creates a set of mock "tree" resources using the **random** and **local** providers. Each tree is represented by a small text file containing a whimsical description. The module is perfect for:

- Demonstrating Terraform module structure.
- Providing dummy resources for CI pipelines that need to run `terraform init`/`validate` without touching real cloud services.
- Adding a touch of magic to your IaC demos.

## Features

- Configurable number of trees (`var.tree_count`).
- Generates unique tree names with `random_pet`.
- Writes a descriptive file for each tree under `trees/`.
- Outputs the list of generated tree names.

## Usage

```hcl
module "enchanted_forest" {
  source      = "./nightly-terraform-cryptic-forest"
  tree_count  = 5
}

output "forest_trees" {
  value = module.enchanted_forest.tree_names
}
```

## Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `tree_count` | `number` | `3` | Number of trees to create. |

## Outputs

| Name | Description |
|------|-------------|
| `tree_names` | List of generated tree identifiers. |

## Testing

A simple validation script is provided under `tests/validate.sh`. Run it with:

```bash
cd nightly-terraform-cryptic-forest
bash tests/validate.sh
```

If everything is set up correctly, you will see:

```
✅ Terraform module validation passed
```

Enjoy your enchanted forest! 🌳✨

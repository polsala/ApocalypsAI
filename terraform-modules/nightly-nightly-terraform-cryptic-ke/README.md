# nightly-terraform-cryptic-keeper

## Overview

`nightly-terraform-cryptic-keeper` is a tiny Terraform module that pretends to provision a secret vault.  It generates a whimsical name using the `random_pet` provider and outputs that name so you can reference it in other resources.

The module is deliberately simple – perfect for:

* Demo environments where you need a placeholder resource.
* Teaching Terraform basics without touching real cloud APIs.
* Adding a dash of fun to CI pipelines.

## Usage

```hcl
module "cryptic_vault" {
  source = "./nightly-terraform-cryptic-keeper"
  prefix = "demo"
}

output "vault_name" {
  value = module.cryptic_vault.vault_name
}
```

## Variables

| Name   | Description                     | Type   | Default |
|--------|---------------------------------|--------|---------|
| prefix | Optional prefix for the vault. | string | ""      |

## Outputs

| Name       | Description                                 |
|------------|---------------------------------------------|
| vault_name | The generated, whimsical vault name string. |

## Testing

A lightweight Bash test lives under `tests/`. Run it with:

```bash
cd nightly-terraform-cryptic-keeper
bash tests/test_module.sh
```

The test simply validates that the module files contain the expected Terraform blocks.

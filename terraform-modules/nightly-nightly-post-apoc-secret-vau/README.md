# Nightly Post‑Apoc Secret Vault

A whimsical Terraform module that generates a cryptographically‑secure random password, perfect for safeguarding your post‑apocalyptic secrets. The module is self‑contained, uses only the `random` provider, and can be dropped into any Terraform configuration.

## Usage

```hcl
module "secret_vault" {
  source = "./modules/nightly-post-apoc-secret-vault"

  length          = 24
  special         = true
  override_special = "!@#"
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| length | Length of the generated password | number | 16 |
| special | Include special characters | bool | true |
| override_special | Set of special characters to use | string | "!@#$%&*()-_=+[]{}<>?" |

## Outputs

| Name | Description |
|------|-------------|
| password | The generated password |

## Testing

Run the provided test script:

```sh
cd test
./test_module.sh
```

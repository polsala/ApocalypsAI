# Terraform Portal Gateway

Creates a whimsical portal using `null_resource` that prints a message when applied.

## Usage

```hcl
module "portal" {
  source = "git::https://example.com/your-repo.git//utils/terraform-portal-gateway"
}
```

Run `terraform init` and `terraform apply`.

## Inputs

- `portal_name` (string) – optional custom name for the portal.

## Outputs

- `message` – the portal opening message.

## Testing

Run the test script:

```bash
bash tests/test_portal.sh
```

# Nightly Safehouse S3 Terraform Module

Creates an Amazon S3 bucket configured for post‑apocalyptic data vaults:

* **Versioning** enabled by default so you never lose a file.
* **Lifecycle rule** that automatically expires objects after a configurable number of days.
* **Random password** generated with the `random` provider for secret storage.

## Usage
```hcl
module "safehouse" {
  source          = "./src"
  bucket_name     = "my‑post‑apoc‑vault"
  versioning      = true          # optional, defaults to true
  expiration_days = 30            # optional, defaults to 30
}
```

The module outputs:
* `bucket_id` – the bucket identifier.
* `bucket_arn` – the bucket ARN.
* `vault_password` – a randomly generated password (marked as sensitive).

## Providers
The module requires the following providers (declared in `src/main.tf`):
* `hashicorp/aws`
* `hashicorp/random`

No real AWS credentials are needed to run the included tests – they only invoke `terraform validate` and `terraform plan` with a dummy region.

## Testing
Run the test script:
```bash
cd tests && ./test.sh
```
It will initialise Terraform, validate the configuration, and execute a deterministic plan.

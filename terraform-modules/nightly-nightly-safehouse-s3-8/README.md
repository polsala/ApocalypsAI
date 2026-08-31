# nightly‑safehouse‑s3

A whimsical yet practical Terraform module that creates a secure S3 bucket suitable for storing precious supplies in a post‑apocalyptic safe‑house. The bucket has:

* Versioning enabled (optional)
* A lifecycle rule that expires objects after a configurable number of days
* An IAM user with programmatic access (access key & secret) generated automatically

## Features

* **Versioned storage** – keep a history of your critical files.
* **Automatic expiration** – objects older than `lifecycle_days` are removed.
* **One‑click credentials** – a dedicated IAM user and access keys are created for you.

## Usage

```hcl
module "safehouse_storage" {
  source = "./terraform-modules/nightly-safehouse-s3"

  bucket_name        = "my‑post‑apoc‑stash"
  versioning_enabled = true
  lifecycle_days     = 90
}

output "access_key_id" {
  value = module.safehouse_storage.access_key_id
}

output "secret_access_key" {
  value     = module.safehouse_storage.secret_access_key
  sensitive = true
}
```

## Variables

| Name                | Type    | Description                                          | Default |
|---------------------|---------|------------------------------------------------------|---------|
| `bucket_name`       | string  | Name of the S3 bucket (must be globally unique).    | n/a     |
| `versioning_enabled`| bool    | Enable versioning on the bucket.                     | `true`  |
| `lifecycle_days`    | number  | Number of days after which objects expire.           | `30`    |

## Outputs

| Name                | Description                                 |
|---------------------|---------------------------------------------|
| `bucket_id`         | The ID of the created bucket.               |
| `bucket_arn`        | The ARN of the created bucket.              |
| `access_key_id`     | IAM access key ID for the generated user.   |
| `secret_access_key` | IAM secret access key (sensitive).          |

## Testing

Run the provided test script to ensure the module validates correctly:

```bash
cd terraform-modules/nightly-safehouse-s3
./tests/validate.sh
```

The script runs `terraform init -backend=false` and `terraform validate` in a temporary directory.

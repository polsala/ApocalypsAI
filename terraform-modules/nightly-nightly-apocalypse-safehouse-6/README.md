# Nightly Apocalypse Safehouse S3

## Overview
A tiny, whimsical Terraform module that creates an **S3 bucket** configured for a post‑apocalyptic safe‑house:

* **Versioning** enabled – never lose a supply list.
* **Server‑side encryption** with AES‑256 – keep the secrets safe.
* **Lifecycle rule** that expires objects after 30 days – old rations are discarded automatically.
* Optional **initial supply file** (a placeholder object) can be added via the `initial_supply` variable.

## Usage
```hcl
module "safehouse" {
  source          = "./nightly-apocalypse-safehouse-s3"
  bucket_name     = "my‑post‑apoc‑supplies"
  region          = "us-east-1"
  initial_supply  = "Welcome to the safehouse!"
}
```

## Variables
| Name | Type | Description | Default |
|------|------|-------------|---------|
| `bucket_name` | `string` | Name of the S3 bucket (must be globally unique). | n/a |
| `region` | `string` | AWS region for the bucket. | `"us-east-1"` |
| `initial_supply` | `string` | Optional text content for a starter object named `welcome.txt`. Leave empty to skip. | `""` |

## Outputs
| Name | Description |
|------|-------------|
| `bucket_id` | The bucket name (ID). |
| `bucket_arn` | The full ARN of the bucket. |

## Testing
Run the provided test script to ensure the module validates syntactically:
```bash
cd nightly-apocalypse-safehouse-s3/tests
bash test_module.sh
```
The script runs `terraform init -backend=false` and `terraform validate`.

## License
MIT – feel free to adapt for your own wasteland.

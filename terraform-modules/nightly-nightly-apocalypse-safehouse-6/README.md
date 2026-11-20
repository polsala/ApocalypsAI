# Apocalyptic Safehouse S3 Terraform Module

## Overview
Creates an AWS S3 bucket configured for durability and secrecy, ideal for storing emergency supplies, logs, or artifacts after the world ends.

## Features
- Server‑side encryption (AES‑256)
- Versioning enabled
- Lifecycle rule that expires non‑current versions after 30 days
- Random suffix to avoid name collisions
- Optional custom bucket name

## Usage
```hcl
module "safehouse" {
  source = "./path/to/module"

  bucket_name = "my-safehouse"
}
```

## Variables
| Name | Type | Description | Default |
|------|------|-------------|---------|
| bucket_name | string | Custom bucket name (optional). If omitted, a random suffix is added. | "" |
| aws_region | string | AWS region to deploy resources. | "us-east-1" |

## Outputs
| Name | Description |
|------|-------------|
| bucket_id | The ID of the created bucket |
| bucket_arn | The ARN of the created bucket |

## Testing
Run the provided test script:
```sh
cd tests
./test_module.sh
```
It will initialise Terraform, validate the configuration and ensure no errors.

## License
MIT

# Nightly Chronos Anchor

The Nightly Chronos Anchor is a whimsical-yet-useful Terraform module designed to provision cloud resources with embedded temporal metadata. It tags resources with their creation epoch and a configurable "decay" policy, allowing for automated lifecycle management or simply tracking the age of your digital artifacts in the post-apocalyptic cloudscape.

## Features

- **Temporal Tagging:** Automatically tags provisioned resources with `chronos_epoch` (Unix timestamp of creation) and `chronos_decay_days`.
- **Configurable Decay:** Define a `decay_days` variable to indicate the intended lifespan or review period for the resource.
- **AWS S3 Bucket:** Currently provisions an AWS S3 bucket, easily extensible to other resource types.
- **Self-Contained:** Ready to be dropped into any Terraform project.

## Usage

1.  **Configure AWS Provider:** Ensure your AWS credentials are set up (e.g., via environment variables, AWS CLI config, or `~/.aws/credentials`).
2.  **Define the Module:** In your Terraform configuration, include the module and provide the required variables.

```terraform
module "my_chronos_bucket" {
  source = "./path/to/nightly-chronos-anchor/src" # Adjust path as needed
  
  bucket_name = "my-unique-chronos-bucket-{{timestamp}}" # Replace with a unique name
  region      = "us-east-1"
  decay_days  = 30 # Resource should be reviewed/decayed after 30 days
}

output "chronos_bucket_arn" {
  value = module.my_chronos_bucket.bucket_arn
}
```

3.  **Initialize and Apply:**
    ```bash
    terraform init
    terraform apply
    ```

## Inputs

| Name          | Description                                                               | Type     | Default | Required |
|---------------|---------------------------------------------------------------------------|----------|---------|----------|
| `bucket_name` | The name of the S3 bucket to create. Must be globally unique.             | `string` | n/a     | yes      |
| `region`      | The AWS region where the S3 bucket will be created.                       | `string` | `"us-east-1"` | no       |
| `decay_days`  | Number of days after which the resource is considered for "decay" (review/deletion). | `number` | `90`    | no       |

## Outputs

| Name             | Description                               |
|------------------|-------------------------------------------|
| `bucket_arn`     | The ARN of the created S3 bucket.         |
| `bucket_id`      | The ID (name) of the created S3 bucket.   |
| `chronos_epoch`  | The Unix timestamp (epoch) when the resource was provisioned. |

## Development & Testing

Tests are implemented using a simple bash script that leverages `terraform validate` and `terraform plan` to ensure the module's syntax is correct and that expected tags are present in the plan output without provisioning actual resources.

To run tests:
```bash
cd tests
./test_chronos_anchor.sh
```

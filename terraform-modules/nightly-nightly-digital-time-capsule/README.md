# Nightly Digital Time Capsule

A Terraform module to provision a secure, versioned cloud storage bucket for a digital time capsule, complete with lifecycle rules for long-term preservation.

This module creates an AWS S3 bucket configured for long-term, secure storage of important data, messages, or AI-generated wisdom. It includes features like versioning, server-side encryption, and lifecycle rules to transition data to colder, more cost-effective storage classes over time, simulating a 'digital burial' for future retrieval.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_time_capsule" {
  source = "./path/to/nightly-digital-time-capsule" # Or a remote source

  bucket_name = "my-apocalypsai-time-capsule-2024"
  tags = {
    Environment = "Production"
    Purpose     = "ApocalypsAI Time Capsule"
    Owner       = "ApocalypsAI Integrator"
  }
}

output "time_capscapsule_bucket_id" {
  value = module.my_time_capsule.bucket_id
}

output "time_capsule_bucket_arn" {
  value = module.my_time_capsule.bucket_arn
}
```

## Inputs

| Name        | Description                                     | Type      | Default | Required |
|-------------|-------------------------------------------------|-----------|---------|----------|
| `bucket_name` | The name of the S3 bucket for the time capsule. | `string`  | n/a     | yes      |
| `tags`      | A map of tags to assign to the bucket.          | `map(string)` | `{}`    | no       |

## Outputs

| Name          | Description                  |
|---------------|------------------------------|
| `bucket_id`   | The ID (name) of the S3 bucket. |
| `bucket_arn`  | The ARN of the S3 bucket.    |

## Tests

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script:

```bash
cd tests/
./test.sh
```

This script will perform `terraform init`, `terraform validate`, and `terraform plan -destroy` to ensure the module's configuration is syntactically correct and can be planned without actually provisioning cloud resources. This satisfies the offline and deterministic testing requirements.

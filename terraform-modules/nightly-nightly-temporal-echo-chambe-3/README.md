# Nightly Temporal Echo Chamber Provisioner

## Overview

The `nightly-temporal-echo-chamber-prov` is a whimsical-yet-useful Terraform module designed to provision an ephemeral cloud storage bucket. This "Temporal Echo Chamber" is perfect for capturing fleeting data, logs, or any digital whispers that need to be stored temporarily before fading into the void. It automatically purges its contents after a configurable number of days, ensuring that no echo lingers longer than intended.

## Features

*   **Ephemeral Storage**: Provisions an AWS S3 bucket with a lifecycle policy for automatic object deletion.
*   **Configurable Retention**: Easily set the number of days before echoes are purged.
*   **Versioned**: S3 bucket versioning is enabled to ensure lifecycle rules apply correctly to all object versions.
*   **Secure**: Private access control list by default.

## Usage

To use this module, you'll need Terraform installed and AWS credentials configured.

1.  **Create a `main.tf` file** in your project directory:

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your desired AWS region
    }

    module "my_echo_chamber" {
      source = "./path/to/nightly-temporal-echo-chamber-prov/src"

      prefix         = "my-apocalypsai-echo"
      retention_days = 14 # Echoes will fade after 14 days
      aws_region     = "us-east-1"
    }

    output "echo_chamber_name" {
      value = module.my_echo_chamber.bucket_id
    }

    output "echo_chamber_arn" {
      value = module.my_echo_chamber.bucket_arn
    }
    ```

2.  **Initialize Terraform**:

    ```bash
    terraform init
    ```

3.  **Review the plan** (optional but recommended):

    ```bash
    terraform plan
    ```

4.  **Apply the configuration** to provision your Echo Chamber:

    ```bash
    terraform apply
    ```

## Inputs

| Name             | Description                                                                 | Type   | Default | Required |
| :--------------- | :-------------------------------------------------------------------------- | :----- | :------ | :------- |
| `prefix`         | A unique prefix for the S3 bucket name. Must be lowercase and globally unique. | `string` | n/a     | yes      |
| `retention_days` | Number of days after which temporal echoes (objects) will be automatically purged from the chamber. | `number` | `7`     | no       |
| `aws_region`     | The AWS region to deploy the echo chamber.                                  | `string` | `us-east-1` | no       |

## Outputs

| Name                 | Description                                    |
| :------------------- | :--------------------------------------------- |
| `bucket_id`          | The ID (name) of the Temporal Echo Chamber S3 bucket. |
| `bucket_arn`         | The ARN of the Temporal Echo Chamber S3 bucket. |
| `bucket_domain_name` | The S3 bucket domain name.                     |

## Testing

To run the module's self-contained tests, navigate to the `tests/` directory and execute `test.sh`.

```bash
cd tests/
./test.sh
```

This script will perform `terraform init`, `terraform validate`, and `terraform plan` to ensure the module's syntax and structure are correct without deploying actual resources.

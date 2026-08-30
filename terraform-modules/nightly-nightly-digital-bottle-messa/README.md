# Nightly Digital Message Bottle (Terraform Module)

This Terraform module provisions a highly durable and resilient infrastructure on AWS to store a 'digital message in a bottle'. It's designed for situations where you need to store a critical, single message (or small set of files) that can be retrieved reliably, even in the face of regional outages or data loss scenarios.

Think of it as a digital time capsule or an emergency information drop-off point, ensuring your message persists through the digital apocalypse.

## Features

*   **Highly Durable Storage**: Utilizes AWS S3 with versioning enabled for robust object storage and historical message tracking.
*   **Metadata Tracking**: Employs AWS DynamoDB to store metadata about your messages (e.g., `MessageID`, `Timestamp`, `ContentHash`), allowing for easy lookup and management.
*   **Serverless & Cost-Effective**: DynamoDB is configured for `PAY_PER_REQUEST` billing, ensuring you only pay for what you use.
*   **Private by Default**: S3 bucket is configured with `private` ACL for secure storage.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "digital_bottle" {
  source = "./path/to/nightly-digital-bottle-message" # Or a Git/S3 source

  project_name = "my-apocalypse-project"
  aws_region   = "us-east-1"
}

output "bottle_s3_bucket" {
  value = module.digital_bottle.s3_bucket_name
}

output "bottle_dynamodb_table" {
  value = module.digital_bottle.dynamodb_table_name
}
```

### Inputs

| Name         | Description                                                 | Type   | Default       | Required |
| :----------- | :---------------------------------------------------------- | :----- | :------------ | :------- |
| `project_name` | A unique name for the project, used as a prefix for resources. | `string` | `apocalypsai` | no       |
| `aws_region`   | The AWS region where resources will be deployed.            | `string` | `us-east-1`   | no       |

### Outputs

| Name                    | Description                                              |
| :---------------------- | :------------------------------------------------------- |
| `s3_bucket_name`        | The name of the S3 bucket created for the digital message bottle. |
| `dynamodb_table_name`   | The name of the DynamoDB table created for message metadata. |

## Testing

This module includes automated tests using `terraform test` to ensure its configuration is valid and outputs are as expected. The tests are deterministic and run offline using mock providers.

To run the tests:

1.  Navigate to the module's root directory.
2.  Initialize Terraform (backend is not required for `terraform test` with mocks):
    ```bash
    terraform init -backend=false
    ```
3.  Run the tests:
    ```bash
    terraform test
    ```

This will execute the tests defined in `tests/test.tftest.hcl` against the module instantiated in `tests/main.tf`.

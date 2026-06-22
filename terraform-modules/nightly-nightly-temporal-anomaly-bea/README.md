# Nightly Temporal Anomaly Beacon

This Terraform module provisions a secure, versioned AWS S3 bucket designed to act as a "Temporal Anomaly Beacon." In the chaotic post-apocalyptic landscape, reliable data storage for tracking temporal distortions is paramount. This beacon provides a robust, highly available, and versioned repository for any readings, logs, or artifacts related to temporal anomalies.

## Features

*   **Secure**: Configured with server-side encryption (SSE-S3) and public access blocked by default.
*   **Versioned**: Keeps a history of all objects, crucial for tracking changes in temporal data.
*   **Highly Available**: Leverages AWS S3's inherent durability and availability.
*   **Lifecycle Management**: Automatically transitions older data to infrequent access storage and eventually expires it, optimizing costs.

## Usage

To deploy your own Temporal Anomaly Beacon, include this module in your Terraform configuration:

```terraform
module "anomaly_beacon" {
  source  = "./nightly-temporal-anomaly-beacon" # Adjust path if not local, e.g., "./" if in the same directory
  # source = "polsala/apocalypsai/nightly-temporal-anomaly-beacon" # Example for registry usage
  
  bucket_name_prefix = "temporal-beacon"
  aws_region         = "us-east-1"
  environment        = "production"
}

output "beacon_bucket_arn" {
  description = "The ARN of the Temporal Anomaly Beacon S3 bucket."
  value       = module.anomaly_beacon.bucket_arn
}

output "beacon_bucket_id" {
  description = "The ID (name) of the Temporal Anomaly Beacon S3 bucket."
  value       = module.anomaly_beacon.bucket_id
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to deploy.

## Inputs

| Name                 | Description                                                              | Type     | Default          | Required |
|----------------------|--------------------------------------------------------------------------|----------|------------------|----------|
| `bucket_name_prefix` | A prefix for the S3 bucket name. A unique suffix will be appended.       | `string` | `"anomaly-beacon"` | no       |
| `aws_region`         | The AWS region where the S3 bucket will be created.                      | `string` | n/a              | yes      |
| `environment`        | An environment tag for the bucket (e.g., "dev", "prod").                 | `string` | `"dev"`          | no       |

## Outputs

| Name                 | Description                                     |
|----------------------|-------------------------------------------------|
| `bucket_id`          | The name (ID) of the created S3 bucket.         |
| `bucket_arn`         | The ARN of the created S3 bucket.               |
| `bucket_domain_name` | The S3 bucket's regional domain name.           |

## Requirements

*   Terraform CLI (v1.0.0+)
*   Configured AWS credentials

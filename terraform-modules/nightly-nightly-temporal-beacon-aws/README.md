# Nightly Temporal Anomaly Beacon (AWS)

This Terraform module provisions an AWS S3 bucket designed to serve as a "Temporal Anomaly Beacon." While its primary function is to provide a stable, secure storage location for logs and data related to spacetime distortions (or any other critical data you deem worthy of a beacon), it also serves as a robust example of a well-configured S3 bucket.

## Features

*   **Secure Storage:** Configured with server-side encryption (SSE-S3) and public access blocked by default.
*   **Data Integrity:** Versioning is enabled to protect against accidental deletions or overwrites.
*   **Whimsical Tagging:** Automatically tags the bucket with `Purpose = "TemporalAnomalyBeacon"` for easy identification in your cloud landscape.
*   **Customizable:** Allows for a custom bucket name prefix and environment tagging.

## Usage

To deploy your own Temporal Anomaly Beacon, add this module to your Terraform configuration:

```terraform
module "temporal_beacon" {
  source = "./nightly-temporal-beacon-aws/src" # Adjust path if not in root
  
  bucket_name_prefix = "apocalypsai-temporal-beacon"
  environment        = "production"
  aws_region         = "us-east-1" # Or your desired region
}

output "beacon_bucket_arn" {
  description = "The ARN of the Temporal Anomaly Beacon S3 bucket."
  value       = module.temporal_beacon.bucket_arn
}

output "beacon_bucket_id" {
  description = "The ID (name) of the Temporal Anomaly Beacon S3 bucket."
  value       = module.temporal_beacon.bucket_id
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision the beacon.

## Inputs

| Name                 | Description                                    | Type     | Default     | Required |
| :------------------- | :--------------------------------------------- | :------- | :---------- | :------- |
| `bucket_name_prefix` | Prefix for the S3 bucket name. A unique suffix will be appended. | `string` | `null`      | yes      |
| `environment`        | The environment tag for the S3 bucket.         | `string` | `"dev"`     | no       |
| `aws_region`         | The AWS region to deploy the S3 bucket in.     | `string` | `us-east-1` | no       |

## Outputs

| Name                | Description                                    |
| :------------------ | :--------------------------------------------- |
| `bucket_arn`        | The ARN of the S3 bucket.                      |
| `bucket_id`         | The ID (name) of the S3 bucket.                |
| `bucket_domain_name`| The S3 bucket's domain name.                   |

## Development & Testing

Tests are designed to be run offline using `terraform plan` and `terraform show -json` to verify the module's output without provisioning actual resources.

To run tests:

```bash
cd tests
./test_assertions.sh
```

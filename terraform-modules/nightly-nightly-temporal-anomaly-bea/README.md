# Nightly Temporal Anomaly Beacon

A Terraform module designed to provision a cloud storage beacon for collecting and managing data related to temporal anomalies. This module sets up an AWS S3 bucket with whimsical tagging, versioning, public access blocking, and lifecycle rules for automatic archiving and expiration, simulating a self-managing data beacon.

## Features

*   **Whimsical Tagging**: Apply unique tags like `TemporalSignature`, `BeaconFrequency`, and `AnomalyClassification`.
*   **Data Versioning**: Keep track of all changes to objects within the beacon.
*   **Secure by Default**: Public access is blocked to protect sensitive anomaly data.
*   **Self-Archiving**: Automatically transition older data to Glacier for long-term, cost-effective storage.
*   **Self-Expiring**: Automatically delete data after a specified period to manage storage footprint.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "anomaly_beacon" {
  source = "./path/to/nightly-temporal-anomaly-beacon/src"

  bucket_name_prefix   = "my-anomaly-data-"
  temporal_signature   = "CHRONO_FLUX_DELTA_7"
  beacon_frequency     = "HOURLY_PULSE"
  anomaly_classification = "MINOR_RIPPLE"
  archive_days         = 60
  expire_days          = 180
}

output "beacon_bucket_id" {
  value = module.anomaly_beacon.bucket_id
}

output "beacon_bucket_arn" {
  value = module.anomaly_beacon.bucket_arn
}
```

## Requirements

*   Terraform (tested with >= 1.0)
*   AWS Provider (configured with appropriate credentials and region)

## Inputs

| Name                   | Description                                                               | Type     | Default              | Required |
| :--------------------- | :------------------------------------------------------------------------ | :------- | :------------------- | :------- |
| `bucket_name_prefix`   | A unique prefix for the S3 bucket name.                                   | `string` | n/a                  | yes      |
| `temporal_signature`   | A whimsical signature for the temporal anomaly.                           | `string` | `"UNKNOWN_SIGNATURE"` | no       |
| `beacon_frequency`     | The perceived frequency of temporal anomalies this beacon monitors.       | `string` | `"INFREQUENT"`      | no       |
| `anomaly_classification` | The classification of the temporal anomaly (e.g., 'Minor Ripple', 'Major Distortion'). | `string` | `"UNCLASSIFIED"`    | no       |
| `archive_days`         | Number of days after which objects are transitioned to GLACIER.           | `number` | `30`                 | no       |
| `expire_days`          | Number of days after which objects are expired (deleted).                 | `number` | `90`                 | no       |

## Outputs

| Name          | Description               |
| :------------ | :------------------------ |
| `bucket_id`   | The ID of the S3 bucket.  |
| `bucket_arn`  | The ARN of the S3 bucket. |

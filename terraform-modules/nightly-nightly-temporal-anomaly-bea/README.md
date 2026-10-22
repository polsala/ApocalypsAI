# Nightly Temporal Anomaly Beacon

A Terraform module designed to deploy a cloud-based "Temporal Anomaly Beacon" using AWS services. This beacon monitors specified log groups for patterns indicative of temporal distortions or anomalies and triggers an alarm, sending notifications via SNS.

## Features

*   **Log Monitoring**: Creates an AWS CloudWatch Log Group to ingest relevant logs.
*   **Pattern Detection**: Uses a CloudWatch Metric Filter to count occurrences of a user-defined "anomaly" pattern within the logs.
*   **Alarming**: Sets up a CloudWatch Metric Alarm that triggers when the anomaly count exceeds a specified threshold.
*   **Notifications**: Sends alerts to an AWS SNS Topic, which can then notify subscribers (e.g., via email).

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "temporal_anomaly_beacon" {
  source = "./path/to/nightly-temporal-anomaly-beacon" # Adjust path as needed

  project_name       = "ApocalypsAI"
  environment        = "production"
  anomaly_pattern    = "Temporal Distortion Detected"
  alarm_threshold    = 5
  notification_email = "integrator@apocalypsai.com"
  aws_region         = "us-east-1"
}

output "beacon_log_group_name" {
  value = module.temporal_anomaly_beacon.log_group_name
}

output "beacon_sns_topic_arn" {
  value = module.temporal_anomaly_beacon.sns_topic_arn
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to deploy the beacon.

## Inputs

| Name                 | Description                                                              | Type     | Default | Required |
| :------------------- | :----------------------------------------------------------------------- | :------- | :------ | :------- |
| `project_name`       | The name of the project, used for resource naming.                       | `string` | `""`    | yes      |
| `environment`        | The deployment environment (e.g., `dev`, `prod`), used for resource naming. | `string` | `""`    | yes      |
| `anomaly_pattern`    | The log pattern to search for in CloudWatch logs.                        | `string` | `""`    | yes      |
| `alarm_threshold`    | The number of anomalies within the period to trigger the alarm.          | `number` | `1`     | no       |
| `notification_email` | Email address to subscribe to the SNS topic for alerts.                  | `string` | `""`    | yes      |
| `aws_region`         | AWS region where resources will be deployed.                             | `string` | `""`    | yes      |

## Outputs

| Name                   | Description                                          |
| :--------------------- | :--------------------------------------------------- |
| `log_group_name`       | The name of the CloudWatch Log Group created.        |
| `sns_topic_arn`        | The ARN of the SNS Topic created for notifications.  |

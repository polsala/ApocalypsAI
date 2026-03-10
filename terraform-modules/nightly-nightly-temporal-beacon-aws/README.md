# Nightly Temporal Anomaly Beacon (AWS)

This Terraform module deploys a simple AWS infrastructure designed to act as a "Temporal Anomaly Beacon." It provisions an S3 bucket to store "anomaly logs" and an AWS Lambda function that can be triggered (e.g., by an external system or a scheduled event) to record a timestamp, a whimsical message, or process incoming "temporal data."

It's a foundational piece for any aspiring chrononaut's infrastructure, helping to mark and observe the subtle shifts in the spacetime continuum.

## Usage

To deploy your own Temporal Anomaly Beacon, add the following to your Terraform configuration:

```terraform
module "my_anomaly_beacon" {
  source      = "./path/to/nightly-temporal-beacon-aws/src"
  beacon_name = "chronal-drift-monitor"
  aws_region  = "us-east-1"
  log_level   = "INFO"
}

output "beacon_s3_bucket" {
  value = module.my_anomaly_beacon.s3_bucket_name
}

output "beacon_lambda_function" {
  value = module.my_anomaly_beacon.lambda_function_name
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision the resources.

## Inputs

| Name        | Description                                       | Type   | Default     | Required |
|-------------|---------------------------------------------------|--------|-------------|----------|
| `beacon_name` | A unique name for your temporal anomaly beacon.   | `string` | `"temporal-beacon"` | no       |
| `aws_region`  | The AWS region to deploy the beacon in.           | `string` | `"us-east-1"` | no       |
| `log_level`   | The logging level for the Lambda function.        | `string` | `"INFO"`    | no       |

## Outputs

| Name                   | Description                                  |
|------------------------|----------------------------------------------|
| `s3_bucket_name`       | The name of the S3 bucket created.           |
| `lambda_function_name` | The name of the Lambda function created.     |
| `lambda_invoke_arn`    | The ARN to invoke the Lambda function.       |

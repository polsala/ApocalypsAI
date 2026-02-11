# Nightly Digital Signal Fire

A Terraform module to deploy a highly available static website on AWS S3/CloudFront, acting as a digital signal fire for emergency messages or community status updates. In a world of shifting sands and uncertain signals, this utility ensures your message can always reach those who need it, broadcast across the digital wasteland.

## Features

*   **Highly Available**: Leverages AWS S3 for storage and CloudFront for global content delivery, ensuring resilience even in fragmented networks.
*   **Static Content**: Simple HTML/CSS for minimal overhead and maximum reliability.
*   **Easy Updates**: Content can be easily updated by modifying the S3 bucket's `index.html` or other static files.
*   **Customizable Message**: Deploy with an initial message, ready to be updated.

## Usage

To deploy your Digital Signal Fire, include this module in your Terraform configuration:

```terraform
module "signal_fire" {
  source = "./nightly-digital-signal-fire/src" # Adjust path if not local
  
  bucket_name_prefix = "apocalypsai-signal-fire" # Unique prefix for your S3 bucket
  initial_message    = "The Nightly Integrator Agent is online. All systems nominal. Stay vigilant!"
  aws_region         = "us-east-1" # Or your preferred AWS region
}

output "signal_fire_url" {
  value = module.signal_fire.cloudfront_domain_name
}
```

### Requirements

*   Terraform CLI installed
*   AWS CLI configured with appropriate credentials and permissions to create S3 buckets, S3 bucket policies, CloudFront distributions, and Origin Access Identities.

## Inputs

| Name                 | Description                                     | Type     | Default     | Required |
| :------------------- | :---------------------------------------------- | :------- | :---------- | :------- |
| `bucket_name_prefix` | A unique prefix for the S3 bucket name.         | `string` | `null`      | yes      |
| `initial_message`    | The initial message to display on the signal fire page. | `string` | `"Beacon online. Awaiting instructions."` | no       |
| `aws_region`         | The AWS region to deploy resources in.          | `string` | `"us-east-1"` | no       |

## Outputs

| Name                    | Description                                     |
| :---------------------- | :---------------------------------------------- |
| `s3_bucket_id`          | The ID of the S3 bucket created.                |
| `cloudfront_domain_name`| The domain name of the CloudFront distribution. |
| `cloudfront_arn`        | The ARN of the CloudFront distribution.         |

## Development & Testing

See the `tests/` directory for how to run local validation tests.

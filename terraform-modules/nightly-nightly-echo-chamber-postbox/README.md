# Nightly Echo Chamber Postbox

This Terraform module provisions a resilient, cloud-based message postbox using AWS Simple Queue Service (SQS) and Simple Notification Service (SNS). It's designed to facilitate asynchronous, inter-community communication in a scattered, post-apocalyptic world, ensuring messages can be published and consumed reliably.

## Features

*   **Reliable Messaging**: Utilizes AWS SQS for durable message storage.
*   **Broadcast Capability**: Leverages AWS SNS for publishing messages to multiple subscribers (in this case, the SQS queue).
*   **Simple Integration**: Provides clear outputs for queue URL and topic ARN for easy integration into other systems.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "echo_chamber_postbox" {
  source = "./path/to/nightly-echo-chamber-postbox/src"

  name_prefix = "apocalypsai-comm"
  region      = "us-east-1"
}

output "postbox_sqs_url" {
  description = "The URL of the SQS queue for consuming messages."
  value       = module.echo_chamber_postbox.sqs_queue_url
}

output "postbox_sns_topic_arn" {
  description = "The ARN of the SNS topic for publishing messages."
  value       = module.echo_chamber_postbox.sns_topic_arn
}
```

## Inputs

| Name        | Description                                       | Type     | Default     | Required |
| :---------- | :------------------------------------------------ | :------- | :---------- | :------- |
| `name_prefix` | A prefix used for naming all resources.           | `string` | `"echo-chamber"` | no       |
| `region`      | The AWS region where resources will be deployed.  | `string` | `"us-east-1"` | no       |

## Outputs

| Name                | Description                                     |
| :------------------ | :---------------------------------------------- |
| `sqs_queue_url`     | The URL of the created SQS queue.               |
| `sns_topic_arn`     | The ARN of the created SNS topic.               |

## Testing

The module includes a basic test setup that uses `terraform init`, `terraform validate`, and `terraform plan -destroy` to ensure the module's syntax is correct and it can be planned for destruction without errors. This is an offline, deterministic test that does not provision actual cloud resources.

To run the tests:

```bash
cd tests
./test.sh
```

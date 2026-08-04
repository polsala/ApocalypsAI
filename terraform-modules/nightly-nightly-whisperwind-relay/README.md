# Nightly Whisperwind Message Relay

A Terraform module designed to quickly deploy a simple, resilient, and low-cost message relay system. Ideal for establishing basic communication channels between scattered survivor settlements or automated outposts in a post-apocalyptic digital landscape. It provisions an AWS SQS queue and necessary IAM permissions.

## Features

*   **Resilient Messaging**: Utilizes AWS SQS for reliable message delivery.
*   **Low-Cost**: Designed for minimal operational overhead.
*   **Configurable**: Easily adjust queue parameters like visibility timeout and message retention.
*   **Whimsical Naming**: Embrace the spirit of the digital wasteland with a 'Whisperwind Relay'.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "settlement_comms_relay" {
  source = "./path/to/nightly-whisperwind-relay/src" # Adjust path as needed

  relay_name                = "alpha-settlement-relay"
  visibility_timeout_seconds = 60
  message_retention_seconds  = 259200 # 3 days
  delay_seconds             = 10
}

output "relay_url" {
  value       = module.settlement_comms_relay.sqs_queue_url
  description = "The URL of the Whisperwind Message Relay queue."
}
```

## Inputs

| Name                        | Description                                                                    | Type   | Default    | Required |
| :-------------------------- | :----------------------------------------------------------------------------- | :----- | :--------- | :------- |
| `relay_name`                | The name of the SQS queue (Whisperwind Relay).                                 | `string` | `whisperwind-relay` | no       |
| `visibility_timeout_seconds`| The duration (in seconds) that a message will be unavailable after a consumer retrieves it. | `number` | `30`       | no       |
| `message_retention_seconds` | The number of seconds Amazon SQS retains a message.                            | `number` | `345600`   | no       |
| `delay_seconds`             | The length of time (in seconds) that the delivery of all messages in the queue will be delayed. | `number` | `0`        | no       |

## Outputs

| Name            | Description                               |
| :-------------- | :---------------------------------------- |
| `sqs_queue_id`  | The ID of the SQS queue.                  |
| `sqs_queue_arn` | The ARN of the SQS queue.                 |
| `sqs_queue_url` | The URL of the SQS queue.                 |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider configured with appropriate credentials and region.

## Testing

To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script:

```bash
cd nightly-whisperwind-relay/tests
./test.sh
```

This script performs a `terraform init` and `terraform plan -json` to verify the module's planned resources and their attributes without deploying actual infrastructure.

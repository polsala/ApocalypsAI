# Nightly Whisperwind Message Relay

Provisions an AWS Whisperwind Message Relay, a robust and asynchronous communication channel for your post-apocalyptic infrastructure. This module sets up an Amazon SQS (Simple Queue Service) queue and an Amazon SNS (Simple Notification Service) topic, subscribing the queue to the topic. This allows for reliable, decoupled message delivery, perfect for broadcasting vital survival updates or coordinating scavenger missions without direct point-to-point dependencies.

## Features

*   **Decoupled Communication**: Send messages to an SNS topic, and all subscribed SQS queues receive them.
*   **Reliable Messaging**: SQS queues ensure messages are retained until processed.
*   **Configurable**: Customize queue and topic names, retention policies, and other parameters.
*   **Secure**: Automatically configures SQS queue policy to allow messages from the SNS topic.

## Usage

This module is designed to be used with Terraform.

### Prerequisites

*   [Terraform](https://www.terraform.io/downloads.html) installed.
*   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables) with permissions to create SQS queues, SNS topics, and manage their policies.

### Example

```terraform
provider "aws" {
  region = "us-east-1" # Or your preferred AWS region
}

module "survival_relay" {
  source = "./terraform-modules/nightly-whisperwind-message-relay/src" # Adjust path as necessary

  queue_name = "survival-alerts-queue"
  topic_name = "survival-alerts-topic"
  tags = {
    Environment = "Production"
    Purpose     = "CriticalAlerts"
  }
}

output "alert_queue_url" {
  description = "The URL of the survival alerts SQS queue."
  value       = module.survival_relay.sqs_queue_url
}

output "alert_topic_arn" {
  description = "The ARN of the survival alerts SNS topic."
  value       = module.survival_relay.sns_topic_arn
}
```

### Inputs

| Name                               | Description                                                               | Type        | Default                      | Required |
| :--------------------------------- | :------------------------------------------------------------------------ | :---------- | :--------------------------- | :------- |
| `queue_name`                       | The name of the SQS queue.                                                | `string`    | `"whisperwind-message-queue"`| no       |
| `topic_name`                       | The name of the SNS topic.                                                | `string`    | `"whisperwind-message-topic"`| no       |
| `queue_delay_seconds`              | The length of time, in seconds, for which the delivery of all messages in the queue is delayed. | `number`    | `0`                          | no       |
| `queue_max_message_size`           | The limit of how many bytes a message can contain before Amazon SQS rejects it. | `number`    | `262144` (256 KB)            | no       |
| `queue_message_retention_seconds`  | The number of seconds Amazon SQS retains a message.                       | `number`    | `345600` (4 days)            | no       |
| `queue_receive_wait_time_seconds`  | The length of time, in seconds, for which a ReceiveMessage call will wait for a message to arrive. | `number`    | `0`                          | no       |
| `queue_visibility_timeout_seconds` | The duration (in seconds) that an item is hidden from other consumers after a consumer retrieves it. | `number`    | `30`                         | no       |
| `tags`                             | A map of tags to assign to the resources.                                 | `map(string)`| `{ Project = "ApocalypsAI", Utility = "WhisperwindMessageRelay" }` | no       |

### Outputs

| Name              | Description                       |
| :---------------- | :-------------------------------- |
| `sqs_queue_url`   | The URL of the SQS queue.         |
| `sqs_queue_arn`   | The ARN of the SQS queue.         |
| `sns_topic_arn`   | The ARN of the SNS topic.         |

## Development & Testing

To run the automated tests for this module:

1.  Navigate to the `tests/` directory:
    ```bash
    cd terraform-modules/nightly-whisperwind-message-relay/tests/
    ```
2.  Run the test script:
    ```bash
    ./test.sh
    ```

The `test.sh` script performs the following:
*   Initializes Terraform in a test-specific configuration (`terraform init -backend=false`).
*   Validates the module's syntax and configuration (`terraform validate`).
*   Generates a Terraform plan (`terraform plan -no-color -detailed-exitcode`) and asserts that exactly 4 resources (SQS queue, SNS topic, SQS policy, SNS subscription) are planned for creation.

**Mock rationale**: The tests are designed to be deterministic and run offline after the initial provider download. They do not provision actual AWS resources. Instead, they rely on `terraform validate` for syntax checking and `terraform plan` output analysis to verify the module's expected behavior and resource definitions. This ensures the module's structure and variable handling are correct without incurring cloud costs or requiring live AWS interaction for every test run.

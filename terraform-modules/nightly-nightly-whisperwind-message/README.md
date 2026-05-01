# Nightly Whisperwind Message Relay

This Terraform module deploys a resilient, asynchronous message relay system using AWS Simple Queue Service (SQS) and Simple Notification Service (SNS). It's designed to ensure vital whispers reach their intended ears, even when the airwaves are... challenging.

## Features

*   **Asynchronous Communication**: Decouples message producers from consumers.
*   **Resilience**: Messages are retained in SQS, ensuring delivery even if consumers are temporarily offline.
*   **Scalability**: Easily handles varying message loads.
*   **Whimsical Naming**: Because even in the apocalypse, a little charm goes a long way.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary inputs.

```terraform
module "whisperwind_relay" {
  source = "./path/to/your/module/src" # Adjust this path to where you place the module

  queue_name = "my-apocalypse-queue"
  topic_name = "my-apocalypse-topic"

  tags = {
    Environment = "production"
    Project     = "Whisperwind"
    ManagedBy   = "ApocalypsAI"
  }
}

output "relay_queue_url" {
  value = module.whisperwind_relay.sqs_queue_url
}

output "relay_topic_arn" {
  value = module.whisperwind_relay.sns_topic_arn
}
```

## Inputs

| Name                            | Description                                                                                             | Type      | Default                               | Required |
| :------------------------------ | :------------------------------------------------------------------------------------------------------ | :-------- | :------------------------------------ | :------- |
| `queue_name`                    | The name of the SQS queue.                                                                              | `string`  | `"whisperwind-message-queue"`       | no       |
| `topic_name`                    | The name of the SNS topic.                                                                              | `string`  | `"whisperwind-message-topic"`       | no       |
| `queue_delay_seconds`           | The length of time, in seconds, for which the delivery of all messages in the queue is delayed.         | `number`  | `0`                                   | no       |
| `queue_max_message_size`        | The limit of how many bytes a message can contain before Amazon SQS rejects it.                         | `number`  | `262144` (256 KB)                     | no       |
| `queue_message_retention_seconds` | The number of seconds Amazon SQS retains a message.                                                     | `number`  | `345600` (4 days)                     | no       |
| `queue_receive_wait_time_seconds` | The length of time, in seconds, for which a ReceiveMessage call will wait for a message to arrive.      | `number`  | `0`                                   | no       |
| `queue_visibility_timeout_seconds`| The duration (in seconds) that an item is hidden from other consumers after a consumer retrieves it.    | `number`  | `30`                                  | no       |
| `tags`                          | A map of tags to assign to the created AWS resources.                                                   | `map(string)` | `{}`                                  | no       |

## Outputs

| Name            | Description                       |
| :-------------- | :-------------------------------- |
| `sqs_queue_arn` | The ARN of the SQS queue.         |
| `sqs_queue_url` | The URL of the SQS queue.         |
| `sns_topic_arn` | The ARN of the SNS topic.         |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 5.0`

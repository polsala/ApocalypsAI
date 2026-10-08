# Nightly Ephemeral Secret Cauldron

## Overview

This Terraform module conjures up temporary secrets in AWS Secrets Manager, designed for scenarios where credentials or sensitive data need to exist for a short, defined period before being banished back to the digital ether. It's ideal for CI/CD pipelines, temporary access tokens, or any ephemeral data storage needs.

The "ephemeral" nature is primarily controlled by the `recovery_window_in_days` variable, which dictates how long AWS Secrets Manager will retain the secret after it's marked for deletion. Setting this to its minimum (7 days) ensures a swift departure.

## Features

*   **Ephemeral Storage**: Creates an AWS Secrets Manager secret with a short recovery window.
*   **Secure**: Leverages AWS Secrets Manager's built-in encryption and access controls.
*   **Configurable**: Easily set the secret name, value, description, and recovery period.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_ephemeral_token" {
  source = "./path/to/nightly-ephemeral-secret-cauld/src"

  secret_name             = "my-app/temporary-api-key"
  secret_string           = "shhh-this-is-a-secret-value-123"
  description             = "Temporary API key for nightly deployment pipeline."
  recovery_window_in_days = 7 # Minimum for maximum ephemerality
}

output "temporary_secret_arn" {
  value = module.my_ephemeral_token.secret_arn
}

output "temporary_secret_name" {
  value = module.my_ephemeral_token.secret_name
}
```

### Requirements

*   [Terraform CLI](https://www.terraform.io/downloads.html) (v1.0.0 or higher)
*   [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) configured with appropriate permissions to manage Secrets Manager.

### Inputs

| Name                      | Description                                                                                                                              | Type     | Default                                                      | Required |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----------------------------------------------------------- | :------- |
| `secret_name`             | The name of the ephemeral secret.                                                                                                        | `string` | n/a                                                          | yes      |
| `secret_string`           | The actual secret value to store. Marked as sensitive.                                                                                   | `string` | n/a                                                          | yes      |
| `description`             | A description for the secret.                                                                                                            | `string` | `"An ephemeral secret managed by ApocalypsAI Nightly Integrator."` | no       |
| `recovery_window_in_days` | The number of days that Secrets Manager will wait before permanently deleting the secret. Must be between 7 and 30. Set to 7 for maximum ephemerality. | `number` | `7`                                                          | no       |

### Outputs

| Name          | Description                                  |
| :------------ | :------------------------------------------- |
| `secret_arn`  | The ARN of the created ephemeral secret.     |
| `secret_name` | The name of the created ephemeral secret.    |

## Ephemeral Nature & Cleanup

While this module provisions a secret with a short recovery window, **you are responsible for destroying the Terraform resources** when the secret is no longer needed. This can be done manually via `terraform destroy` or integrated into your CI/CD pipeline for automated cleanup after the secret has served its purpose. Once destroyed, AWS Secrets Manager will hold the secret for the `recovery_window_in_days` before permanent deletion.

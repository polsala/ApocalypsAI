## Nightly Terra Vault Guard

This Terraform module provisions a secure, versioned secrets vault using AWS Secrets Manager. It's designed to be a robust and auditable solution for storing sensitive information within your AWS infrastructure.

### Features

*   **AWS Secrets Manager Integration**: Leverages AWS's managed secrets service for secure storage.
*   **Versioned Secrets**: Automatically stores new versions of secrets, allowing for rollback and history.
*   **Resource Policies**: Configurable resource policies for fine-grained access control.
*   **Rotation Support**: Basic configuration for enabling automatic secret rotation (requires additional Lambda function setup).
*   **Auditing**: Integrates with AWS CloudTrail for auditing secret access and modifications.

### Usage

```hcl
module "secrets_vault" {
  source = "./polsala/ApocalypsAI/utils/nightly-terra-vault-guard"

  name        = "my-application-secrets"
  description = "Secrets for my awesome application"

  tags = {
    Environment = "production"
    Project     = "AwesomeApp"
  }

  # Optional: Configure resource policy for specific principals
  # resource_policy = jsonencode({
  #   "Version": "2012-10-17",
  #   "Statement": [
  #     {
  #       "Effect": "Allow",
  #       "Principal": {
  #         "AWS": "arn:aws:iam::123456789012:root"
  #       },
  #       "Action": "secretsmanager:GetSecretValue",
  #       "Resource": "*"
  #     }
  #   ]
  # })

  # Optional: Enable rotation (requires a separate Lambda function)
  # rotation_enabled = true
  # rotation_lambda_arn = "arn:aws:lambda:us-east-1:123456789012:function:my-secret-rotation-lambda"
}
```

### Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | The name of the secret. | `string` | n/a | yes |
| `description` | A description of the secret. | `string` | `null` | no |
| `tags` | A map of tags to assign to the secret. | `map(string)` | `{}` | no |
| `resource_policy` | A JSON string representing the resource policy for the secret. | `string` | `null` | no |
| `rotation_enabled` | Whether to enable secret rotation. | `bool` | `false` | no |
| `rotation_lambda_arn` | The ARN of the Lambda function to use for rotation. Required if `rotation_enabled` is true. | `string` | `null` | no |

### Outputs

| Name | Description |
|------|-------------|
| `secret_arn` | The ARN of the created secret. |
| `secret_name` | The name of the created secret. |
| `secret_version_id` | The ID of the latest version of the secret. |

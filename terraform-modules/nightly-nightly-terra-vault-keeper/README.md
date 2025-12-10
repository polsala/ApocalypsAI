## Nightly Terra Vault Keeper

A whimsical yet robust Terraform module designed to manage secrets securely within a cloud vault. This module not only provisions a secure vault but also includes a mechanism for automated secret rotation, ensuring your sensitive data remains protected against the ravages of time and potential breaches.

### Features

*   **Secure Vault Provisioning**: Creates a dedicated, encrypted vault for your secrets.
*   **Secret Management**: Allows for the definition and storage of individual secrets.
*   **Automated Rotation**: Configurable secret rotation policies to enhance security.
*   **Auditing**: Basic audit logging for secret access and rotation events.

### Usage

To use this module, include it in your Terraform configuration:

```hcl
module "vault_keeper" {
  source = "./path/to/nightly-terra-vault-keeper"

  # Required variables
  vault_name = "apocalypse-secrets"
  region     = "us-east-1"

  # Optional variables
  rotation_enabled = true
  rotation_interval = "24h"
  secret_definitions = {
    "api_key" = {
      value = "super-secret-key-123"
    }
    "db_password" = {
      value = "p@$$wOrd!"
    }
  }
}
```

### Inputs

*   `vault_name` (string, required): The name for the cloud vault.
*   `region` (string, required): The cloud region where the vault will be provisioned.
*   `rotation_enabled` (bool, optional): Whether to enable automated secret rotation. Defaults to `false`.
*   `rotation_interval` (string, optional): The interval for secret rotation (e.g., `"12h"`, `"7d"`). Required if `rotation_enabled` is `true`. Defaults to `"720h"` (30 days).
*   `secret_definitions` (map(object), optional): A map where keys are secret names and values are objects containing the secret `value`. Example: `{"my_secret": {"value": "my_secret_value"}}`.

### Outputs

*   `vault_arn`: The ARN of the provisioned cloud vault.
*   `secret_arns`: A map of secret names to their respective ARNs.

### Rotation Strategy

When `rotation_enabled` is set to `true`, the module will configure a scheduled event (e.g., a Lambda function triggered by CloudWatch Events) to automatically generate a new secret value and update the existing secret. The old value is typically retained for a short period for rollback purposes, depending on the underlying cloud provider's secret management service capabilities.

### Testing

This module includes basic integration tests that provision a minimal vault and add a secret. For rotation tests, manual verification or more complex integration testing with mocked cloud services would be required.

# Nightly Data Doomsday Bunker

## Overview

This Terraform module provisions an ultra-resilient AWS S3 bucket, meticulously engineered to safeguard vital information against temporal anomalies, digital decay, and the general chaos of a post-apocalyptic world. It's your digital time capsule, designed for long-term, secure archival of critical data, blueprints, or messages for future generations or survivors.

## Features

*   **Versioning**: Keeps a complete history of all object changes, allowing recovery from accidental deletions or overwrites.
*   **Server-Side Encryption**: Encrypts all data at rest using AWS S3-managed keys (SSE-S3) for enhanced security.
*   **Lifecycle Management**: Automatically transitions older versions of objects to more cost-effective storage classes (like Glacier) and eventually expires them after a configurable period, balancing cost and long-term retention.
*   **Public Access Block**: Ensures the bucket is never publicly accessible, preventing accidental data exposure.
*   **Secure Access**: Provides a framework for defining granular access policies.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

### Example `main.tf`

```terraform
module "doomsday_bunker" {
  source  = "./" # Adjust this path to where the module is located relative to your root module
  
  bucket_name_prefix = "apocalypsai-archive"
  environment        = "production"
  
  tags = {
    Project     = "ApocalypsAI"
    Purpose     = "DataArchival"
    Confidentiality = "High"
  }
}

output "bunker_id" {
  description = "The ID of the Doomsday Bunker S3 bucket."
  value       = module.doomsday_bunker.bucket_id
}

output "bunker_arn" {
  description = "The ARN of the Doomsday Bunker S3 bucket."
  value       = module.doomsday_bunker.bucket_arn
}
```

### Inputs

| Name               | Description                                                                 | Type    | Default             | Required |
|--------------------|-----------------------------------------------------------------------------|---------|---------------------|----------|
| `bucket_name_prefix` | A prefix for the S3 bucket name. The full name will be generated.           | `string`| `"doomsday-bunker"` | no       |
| `environment`      | The environment name (e.g., `prod`, `dev`) to be included in the bucket name. | `string`| `"prod"`            | no       |
| `tags`             | A map of tags to assign to the S3 bucket.                                   | `map`   | `{}`                | no       |

### Outputs

| Name                         | Description                                     |
|------------------------------|-------------------------------------------------|
| `bucket_id`                  | The ID (name) of the S3 bucket.                 |
| `bucket_arn`                 | The ARN of the S3 bucket.                       |
| `bucket_regional_domain_name`| The regional domain name of the S3 bucket.      |

## Requirements

*   Terraform 0.13+
*   AWS Provider configured with appropriate credentials.

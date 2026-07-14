# Nightly Cloud Cache of Curiosities

This Terraform module provisions a secure, versioned AWS S3 bucket designed to store "curiosities" – any important files, logs, or artifacts that need to be preserved with a touch of whimsical temporal decay. It ensures data integrity, access control, and automatic lifecycle management.

## Features

*   **Secure Storage**: Private S3 bucket with server-side encryption (SSE-S3) and blocked public access.
*   **Versioning**: Keeps multiple versions of an object, protecting against accidental deletions or overwrites.
*   **Temporal Decay Simulation**: Configurable lifecycle rules to transition objects to infrequent access storage and eventually expire them, simulating the natural decay of forgotten curiosities.
*   **Whimsical Naming**: Automatically generates a unique bucket name with a "curios" prefix.

## Usage

To use this module, include it in your Terraform configuration:

```terraform
module "curiosity_cache" {
  source = "./src" # Or a Git/registry source in a real-world scenario

  bucket_name_prefix    = "my-apocalypse-artifacts"
  retention_days        = 730 # Keep curiosities for 2 years
  transition_to_ia_days = 60  # Move to Infrequent Access after 60 days
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Staging"
    Purpose     = "CuriosityCache"
  }
}

output "curiosity_bucket_arn" {
  value       = module.curiosity_cache.bucket_arn
  description = "The ARN of the S3 bucket where curiosities are stored."
}
```

## Inputs

| Name                    | Description                                                                 | Type          | Default                 | Required |
| :---------------------- | :-------------------------------------------------------------------------- | :------------ | :---------------------- | :------- |
| `bucket_name_prefix`    | A prefix for the S3 bucket name. A unique suffix will be appended.          | `string`      | `"apocalypsai-curios"` | no       |
| `retention_days`        | Number of days after which objects in the bucket will be permanently deleted. | `number`      | `365`                   | no       |
| `transition_to_ia_days` | Number of days after which objects will transition to Infrequent Access.    | `number`      | `30`                    | no       |
| `tags`                  | A map of tags to assign to the S3 bucket.                                   | `map(string)` | `{}`                    | no       |

## Outputs

| Name                 | Description                                    |
| :------------------- | :--------------------------------------------- |
| `bucket_id`          | The ID (name) of the created S3 bucket.        |
| `bucket_arn`         | The ARN of the created S3 bucket.              |

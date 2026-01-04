# Nightly Cloud Hide-and-Seek Bucket

This Terraform module provisions a whimsical, ephemeral AWS S3 bucket designed for a "cloud resource hide-and-seek" game. The idea is to deploy this module, then challenge yourself or your team to find the bucket using AWS CLI, SDKs, or the console, and then decommission it.

It's a fun way to practice cloud resource discovery and management skills in a low-stakes environment.

## Features

- Creates a private AWS S3 bucket with a randomly generated, whimsical name.
- Applies specific tags (`Game: CloudHideAndSeek`, `WhimsyLevel: High`, `Ephemeral: True`, `CreatedBy: ApocalypsAI`) to make it identifiable (once found).
- Configurable bucket name prefix and additional common tags.

## Usage

1.  **Initialize Terraform**: Navigate to the module directory and run `terraform init` to download the necessary providers.

    ```bash
    terraform init
    ```

2.  **Configure the Module**: Create a `main.tf` file in your root Terraform configuration (e.g., `my-hide-seek-game/main.tf`) and reference this module:

    ```terraform
    module "hide_seek_bucket" {
      source = "./path/to/nightly-cloud-hide-seek-bucket" # Adjust path as needed

      # Optional: Provide a custom prefix for the bucket name
      # bucket_name_prefix = "my-secret-stash"

      # Optional: Add any other tags
      # common_tags = {
      #   "Team" = "Alpha"
      # }
    }

    output "bucket_id" {
      value = module.hide_seek_bucket.bucket_id
    }

    output "bucket_arn" {
      value = module.hide_seek_bucket.bucket_arn
    }
    ```

3.  **Deploy the Bucket**: Run `terraform apply` to provision the S3 bucket. Terraform will output the bucket's ID and ARN, but try not to look at them if you're playing the game!

    ```bash
    terraform apply
    ```

4.  **Play Hide-and-Seek!**
    -   **Seek**: Use AWS CLI commands (e.g., `aws s3 ls`, `aws s3api list-buckets --query 'Buckets[?starts_with(Name, `hide-seek-`) || starts_with(Name, `your-prefix-`)].Name'`), AWS SDKs, or the AWS Management Console to find the bucket. Look for the `Game: CloudHideAndSeek` tag!
    -   **Find**: Once you've identified the bucket, you've found it!
    -   **Decommission**: To clean up, run `terraform destroy` from your root Terraform configuration. This will remove the bucket.

    ```bash
    terraform destroy
    ```

## Requirements

-   Terraform CLI (v1.0+)
-   AWS Account and configured AWS credentials.

## Testing

To run the automated tests for this module:

1.  Navigate to the module directory.
2.  Run `terraform init`.
3.  Run `terraform test`.

    ```bash
    terraform init
    terraform test
    ```

The tests use Terraform's built-in testing framework with `mock_provider` blocks to ensure deterministic and offline execution without interacting with actual AWS resources.

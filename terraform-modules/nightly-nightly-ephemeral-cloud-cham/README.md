# Nightly Ephemeral Cloud Chamber

## Summary
This Terraform module provisions a self-contained, ephemeral AWS cloud environment designed for temporary testing, development, or demonstration purposes. It includes a basic VPC, subnet, internet gateway, route table, a security group, an EC2 instance, and an S3 bucket. The 'ephemeral' nature encourages regular teardown and recreation, promoting clean slate deployments and cost efficiency.

## Features
-   **Isolated Environment**: Creates a dedicated VPC and associated networking components.
-   **Compute**: Provisions a configurable EC2 instance.
-   **Storage**: Sets up a private S3 bucket with a unique name.
-   **Security**: Includes a basic security group allowing SSH and HTTP access to the EC2 instance.
-   **Customizable**: Allows configuration of AWS region, instance type, and resource tags.

## Usage

### Prerequisites
-   [Terraform](https://www.terraform.io/downloads.html) (v1.0.0 or higher) installed.
-   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).

### Deployment
1.  **Initialize Terraform**: Navigate to the `src` directory and initialize the Terraform working directory.
    ```bash
    cd terraform-modules/nightly-ephemeral-cloud-chamber/src
    terraform init
    ```
2.  **Review the Plan**: See what resources Terraform plans to create.
    ```bash
    terraform plan
    ```
3.  **Apply the Configuration**: Provision the resources in your AWS account.
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

### Teardown
To destroy all resources created by this module:
```bash
terraform destroy
```
Confirm with `yes` when prompted.

### Example `main.tf` (for calling this module)
To use this module in your own Terraform configuration, create a `main.tf` file like this:

```terraform
module "ephemeral_chamber" {
  source  = "./path/to/terraform-modules/nightly-ephemeral-cloud-chamber/src"

  aws_region         = "us-east-1"
  instance_type      = "t2.micro"
  bucket_name_prefix = "my-test-app-data"
  tags = {
    Project = "MyEphemeralProject"
    Owner   = "ApocalypsAI-User"
  }
}

output "chamber_instance_ip" {
  value = module.ephemeral_chamber.instance_public_ip
}

output "chamber_s3_bucket" {
  value = module.ephemeral_chamber.s3_bucket_name
}
```

## Inputs

| Name               | Description                                                                 | Type        | Default             |
|--------------------|-----------------------------------------------------------------------------|-------------|---------------------|
| `aws_region`       | The AWS region to deploy resources into.                                    | `string`    | `"us-east-1"`       |
| `instance_type`    | The EC2 instance type.                                                      | `string`    | `"t2.micro"`        |
| `ami_id`           | The AMI ID for the EC2 instance. If not provided, it fetches the latest Ubuntu 22.04 AMI. | `string` or `null` | `null`              |
| `bucket_name_prefix` | Prefix for the S3 bucket name. A random suffix will be added.               | `string`    | `"ephemeral-chamber"` |
| `tags`             | A map of tags to apply to all resources.                                    | `map(string)` | `{ ManagedBy = "ApocalypsAI", Purpose = "EphemeralCloudChamber" }` |

## Outputs

| Name                 | Description                                    |
|----------------------|------------------------------------------------|
| `instance_public_ip` | The public IP address of the ephemeral EC2 instance. |
| `s3_bucket_name`     | The name of the ephemeral S3 bucket.           |
| `vpc_id`             | The ID of the VPC created for the ephemeral environment. |

## Testing

This module includes automated tests using Terraform's native testing framework (`terraform test`). These tests are designed to be as deterministic and 'offline' as possible, validating the module's structure and planned resource changes without performing actual cloud resource creation.

To run tests:
```bash
cd terraform-modules/nightly-ephemeral-cloud-chamber/tests
terraform test
```

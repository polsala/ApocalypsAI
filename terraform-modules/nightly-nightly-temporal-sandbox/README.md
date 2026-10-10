# Nightly Temporal Sandbox

This Terraform module deploys a whimsical, yet functional, ephemeral AWS cloud sandbox. It's designed for quick, isolated experimentation with "temporal anomalies" (or any other short-lived tasks) without leaving behind persistent infrastructure. All deployed resources are tagged with an `ExpiryDate`, making them prime candidates for automated cleanup by a separate "Temporal Janitor" utility (not included here, but highly recommended!).

## Features

*   **Ephemeral by Design**: Resources are tagged with an `ExpiryDate` based on a configurable Time-To-Live (TTL).
*   **Isolated Environment**: Deploys a dedicated VPC, subnet, and security group.
*   **Basic Compute**: Includes a single EC2 instance for your experiments.
*   **Whimsical Naming**: Resources are named with a "Temporal Sandbox" theme.

## Usage

1.  **Prerequisites**:
    *   [Terraform](https://www.terraform.io/downloads) installed.
    *   AWS CLI configured with credentials that have permissions to create VPCs, EC2 instances, and related resources.

2.  **Module Integration**:
    Create a `main.tf` file in your project:

    ```terraform
    module "temporal_sandbox" {
      source = "./nightly-temporal-sandbox/src" # Adjust path if necessary

      aws_region      = "us-east-1"
      instance_type   = "t2.micro"
      ttl_hours       = 24 # Sandbox will expire in 24 hours
      sandbox_name    = "anomaly-test-001"
    }

    output "sandbox_instance_id" {
      value       = module.temporal_sandbox.sandbox_id
      description = "The ID of the deployed EC2 instance."
    }

    output "sandbox_expiry_timestamp" {
      value       = module.temporal_sandbox.expiry_timestamp
      description = "The UTC timestamp when the sandbox is intended to expire."
    }
    ```

3.  **Initialize & Apply**:

    ```bash
    terraform init
    terraform apply
    ```

    Confirm the plan and type `yes` to deploy.

4.  **Cleanup**:
    When your temporal experiments are complete (or after the `ttl_hours` have passed), you can destroy the sandbox:

    ```bash
    terraform destroy
    ```

    Alternatively, rely on an external "Temporal Janitor" script to find and destroy resources based on the `ExpiryDate` tag.

## Inputs

| Name            | Description                                   | Type     | Default                      | Required |
| :-------------- | :-------------------------------------------- | :------- | :--------------------------- | :------- |
| `aws_region`    | The AWS region to deploy resources into.      | `string` | `"us-east-1"`                | no       |
| `instance_type` | The EC2 instance type for the sandbox.        | `string` | `"t2.micro"`                 | no       |
| `ttl_hours`     | Time-To-Live for the sandbox in hours.        | `number` | `24`                         | no       |
| `sandbox_name`  | A unique name for this temporal sandbox.      | `string` | `"default-temporal-sandbox"` | no       |

## Outputs

| Name                   | Description                                          |
| :--------------------- | :--------------------------------------------------- |
| `sandbox_id`           | The ID of the deployed EC2 instance.                 |
| `expiry_timestamp`     | The UTC timestamp (RFC3339) when the sandbox is intended to expire. |
| `vpc_id`               | The ID of the created VPC.                           |
| `subnet_id`            | The ID of the created subnet.                        |

## Testing

The tests ensure that the Terraform module's plan output contains the expected resources and tags without actually deploying anything to AWS.

To run the tests:

```bash
cd nightly-temporal-sandbox/tests
./test_plan.sh
```

This script will:
1.  Initialize Terraform in a temporary directory.
2.  Run `terraform plan -json` to generate a plan.
3.  Use `jq` to verify the presence of key resources (`aws_vpc`, `aws_instance`) and the `ExpiryDate` tag on the EC2 instance, as well as the `expiry_timestamp` output.

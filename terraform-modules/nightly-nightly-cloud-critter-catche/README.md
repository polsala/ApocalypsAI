# Nightly Cloud Critter Catcher

The Nightly Cloud Critter Catcher is a whimsical-yet-useful Terraform module designed to provision a tiny, ephemeral cloud instance (a "critter") that automatically self-destructs after a configurable lifespan. This is perfect for quick, isolated tests, temporary demos, or any scenario where you need a short-lived compute resource without worrying about leaving it running and incurring unexpected costs.

## Features

*   **Ephemeral Instances**: Critters are designed to live for a short, defined period.
*   **Automatic Self-Destruct**: Each critter comes with a built-in timer that initiates its own termination.
*   **Cost-Efficient**: Prevents lingering resources and unexpected cloud bills.
*   **Customizable**: Configure instance type, AMI, and lifespan.

## Usage

1.  **Prerequisites**:
    *   [Terraform](https://www.terraform.io/downloads.html) installed.
    *   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).

2.  **Module Integration**:
    Create a `main.tf` file in your project and reference the module:

    ```terraform
    module "my_ephemeral_critter" {
      source = "./path/to/nightly-cloud-critter-catcher/src" # Adjust path as needed

      critter_name      = "my-test-critter"
      region            = "us-east-1"
      instance_type     = "t2.micro"
      ami_id            = "ami-053b0d534c279acc9" # Example Amazon Linux 2 AMI in us-east-1
      lifespan_minutes  = 15 # Critter will live for 15 minutes
      # vpc_security_group_ids = ["sg-xxxxxxxxxxxxxxxxx"] # Optional: specify existing security groups
      # subnet_id              = "subnet-xxxxxxxxxxxxxxxxx" # Optional: specify existing subnet
    }

    output "critter_public_ip" {
      value = module.my_ephemeral_critter.public_ip
    }
    ```

    **Note**: The `ami_id` must be valid for the specified `region`. You can find current AMIs in the AWS console or via the AWS CLI.

3.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

4.  **Plan and Apply**:
    Review the planned changes and then apply them to create your critter:
    ```bash
    terraform plan
    terraform apply
    ```

    Your critter will be provisioned and will automatically terminate itself after the `lifespan_minutes` duration.

## Inputs

| Name                   | Description                                                                 | Type     | Default           | Required |
| :--------------------- | :-------------------------------------------------------------------------- | :------- | :---------------- | :------- |
| `critter_name`         | A whimsical name for your cloud critter.                                    | `string` | `"ephemeral-critter"` | no       |
| `region`               | The AWS region to deploy the critter in.                                    | `string` | `"us-east-1"`     | no       |
| `ami_id`               | The AMI ID for the critter instance. Must be valid for the chosen region.   | `string` | `"ami-053b0d534c279acc9"` | no       |
| `instance_type`        | The EC2 instance type for the critter.                                      | `string` | `"t2.micro"`      | no       |
| `lifespan_minutes`     | The number of minutes the critter will live before self-terminating.        | `number` | `10`              | no       |
| `vpc_security_group_ids` | List of security group IDs to associate with the instance.                  | `list(string)` | `[]`              | no       |
| `subnet_id`            | The ID of the subnet to launch the instance into. If not provided, AWS chooses. | `string` | `null`            | no       |

## Outputs

| Name              | Description                               |
| :---------------- | :---------------------------------------- |
| `instance_id`     | The ID of the provisioned EC2 instance.   |
| `public_ip`       | The public IP address of the critter.     |

## Testing

The module includes offline tests that validate the Terraform configuration and plan output without requiring actual AWS credentials or resource provisioning. See `tests/run_tests.sh` for details.

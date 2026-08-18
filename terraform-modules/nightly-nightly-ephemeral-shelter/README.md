# Nightly Ephemeral Shelter

A Terraform module to quickly provision a minimal, temporary cloud compute instance and associated resources. Think of it as a "pop-up bunker" for your short-lived computational needs in the digital wasteland. Ideal for running isolated scripts, testing small code snippets, or providing a temporary staging ground before the next temporal anomaly hits.

## Features

*   **Minimalist Design**: Provisions only essential resources (VPC, Subnet, Security Group, EC2 Instance, SSH Key Pair).
*   **Ephemeral by Nature**: Designed for quick deployment and easy, complete teardown.
*   **Secure Access**: Automatically generates an SSH key pair or uses an existing one for secure access.
*   **Customizable**: Supports various instance types, AMIs, and custom tags.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

### Prerequisites

*   Terraform CLI installed (v1.0+ recommended).
*   AWS CLI configured with credentials that have permissions to create EC2 instances, VPCs, Security Groups, and Key Pairs.

### Example `main.tf`

```terraform
# Configure the AWS provider
provider "aws" {
  region = "us-east-1" # Or your desired region
}

# Configure the TLS provider for SSH key generation
provider "tls" {}

module "my_ephemeral_shelter" {
  source = "./path/to/nightly-ephemeral-shelter/src" # Adjust path as needed

  name_prefix = "my-unique-shelter" # A unique identifier for your shelter
  region      = "us-east-1"
  ami_id      = "ami-053b0d53c279acc90" # Example: Amazon Linux 2 AMI (HVM), SSD Volume Type in us-east-1
  instance_type = "t2.micro"
  create_key_pair = true # Set to false if you want to use an existing key
  # ssh_key_name = "my-existing-key" # Required if create_key_pair is false

  tags = {
    Purpose = "TemporaryCompute"
    Owner   = "ApocalypsAI-Agent"
  }
}

output "shelter_public_ip" {
  value = module.my_ephemeral_shelter.public_ip
}

output "shelter_ssh_command" {
  value = module.my_ephemeral_shelter.ssh_command
  sensitive = true
}

output "shelter_private_key_pem" {
  value = module.my_ephemeral_shelter.private_key_pem
  sensitive = true
}
```

### Deployment Steps

1.  **Save the example**: Save the above content as `main.tf` in a new directory.
2.  **Initialize Terraform**: Run `terraform init` in your directory. This downloads the necessary provider plugins.
3.  **Review the plan**: Run `terraform plan` to see what resources will be created.
4.  **Apply the configuration**: Run `terraform apply` and type `yes` when prompted to create the resources.
5.  **Retrieve SSH Key**: If `create_key_pair` was `true`, the private key will be outputted. Save it to a file (e.g., `my-unique-shelter.pem`) and set appropriate permissions: `chmod 400 my-unique-shelter.pem`.
6.  **Connect**: Use the `shelter_ssh_command` output to connect to your instance.

### Teardown

It is crucial to destroy ephemeral resources when they are no longer needed to avoid incurring unnecessary cloud costs.

1.  **Destroy resources**: Run `terraform destroy` in your directory and type `yes` when prompted.

## Inputs

| Name            | Description                                                                                             | Type        | Default                                                               | Required |
| :-------------- | :------------------------------------------------------------------------------------------------------ | :---------- | :-------------------------------------------------------------------- | :------- |
| `name_prefix`   | A unique prefix for all resources to avoid naming conflicts.                                            | `string`    | n/a                                                                   | yes      |
| `region`        | AWS region to deploy resources into.                                                                    | `string`    | `"us-east-1"`                                                       | no       |
| `ami_id`        | The AMI ID for the EC2 instance. Use a region-specific Amazon Linux 2 AMI.                              | `string`    | `"ami-053b0d53c279acc90"` (Amazon Linux 2 in us-east-1)             | no       |
| `instance_type` | The EC2 instance type.                                                                                  | `string`    | `"t2.micro"`                                                        | no       |
| `create_key_pair` | Whether to create a new SSH key pair for the instance. If `false`, `ssh_key_name` must be provided.       | `bool`      | `true`                                                                | no       |
| `ssh_key_name`  | The name of an existing EC2 key pair to use. Required if `create_key_pair` is `false`.                  | `string`    | `null`                                                                | no       |
| `tags`          | A map of tags to assign to the EC2 instance.                                                            | `map(string)` | `{}`                                                                  | no       |

## Outputs

| Name                | Description                                                               | Sensitive |
| :------------------ | :------------------------------------------------------------------------ | :-------- |
| `instance_id`       | The ID of the provisioned EC2 instance.                                   | no        |
| `public_ip`         | The public IP address of the EC2 instance.                                | no        |
| `private_key_pem`   | The private key in PEM format (only if `create_key_pair` is `true`).      | yes       |
| `ssh_command`       | Example SSH command to connect to the instance.                           | yes       |

## Testing

The module includes a basic test script (`tests/test.sh`) that performs `terraform validate` on a test configuration. This ensures the module's syntax and variable definitions are correct without deploying actual resources.

To run tests:

1.  Navigate to the `tests/` directory.
2.  Run `./test.sh`.

**Note on Offline Testing**: The `terraform init` command within `test.sh` will attempt to download provider plugins if they are not already cached in the `.terraform` directory. For a truly offline test run, ensure the `aws` and `tls` provider plugins are present in the `.terraform/plugins` directory before execution. `terraform validate` itself is an offline operation once plugins are available.

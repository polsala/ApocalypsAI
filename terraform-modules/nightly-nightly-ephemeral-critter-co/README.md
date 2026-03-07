# Nightly Ephemeral Cloud Critter Corral

A Terraform module to provision and de-provision ephemeral cloud critters (VMs/containers) for quick, isolated experiments. Think of it as a temporary playpen for your code, where resources are spun up, used, and then vanish without a trace, keeping your cloud environment tidy.

## 🚀 Usage

This module provisions a single AWS EC2 instance, acting as your "cloud critter."

### Prerequisites

*   Terraform installed (v1.0.0+)
*   AWS CLI configured with appropriate credentials and default region.

### Example

To use this module, create a `main.tf` file in your Terraform project:

```terraform
# main.tf
provider "aws" {
  region = "us-east-1" # Or your desired region
}

module "my_ephemeral_critter" {
  source = "./path/to/nightly-ephemeral-critter-corral/src" # Adjust path as needed

  region        = "us-east-1"
  instance_type = "t2.micro"
  ami_id        = "ami-053b0d53c279acc90" # IMPORTANT: Use a valid AMI ID for your chosen region!
                                         # This example is for Amazon Linux 2 in us-east-1.
  name_prefix   = "my-experiment"
  additional_tags = {
    "Project" = "ApocalypsAI-Experiment"
    "Owner"   = "IntegratorAgent"
  }
}

output "critter_id" {
  value       = module.my_ephemeral_critter.instance_id
  description = "The ID of the ephemeral critter instance."
}

output "critter_ip" {
  value       = module.my_ephemeral_critter.public_ip
  description = "The public IP of the ephemeral critter instance."
}
```

1.  **Initialize Terraform**:
    ```bash
    terraform init
    ```
2.  **Plan the deployment**:
    ```bash
    terraform plan
    ```
3.  **Apply the changes (provision the critter)**:
    ```bash
    terraform apply
    ```
    Confirm with `yes`.
4.  **When done, destroy the critter**:
    ```bash
    terraform destroy
    ```
    Confirm with `yes`. This will remove all resources created by the module.

## ⚙️ Module Inputs

| Name            | Description                                                | Type        | Default                                       | Required |
| :-------------- | :--------------------------------------------------------- | :---------- | :-------------------------------------------- | :------- |
| `region`        | AWS region to deploy the critter in.                       | `string`    | `"us-east-1"`                                 | no       |
| `instance_type` | The EC2 instance type for the critter.                     | `string`    | `"t2.micro"`                                  | no       |
| `ami_id`        | The AMI ID for the critter. Must be valid for the region.  | `string`    | `"ami-053b0d53c279acc90"` (Amazon Linux 2, us-east-1) | no       |
| `name_prefix`   | Prefix for the critter's name tag.                         | `string`    | `"apocalypsai-ephemeral"`                     | no       |
| `additional_tags` | Additional tags to apply to the critter.                 | `map(string)` | `{}`                                          | no       |

## 📤 Module Outputs

| Name          | Description                                         |
| :------------ | :-------------------------------------------------- |
| `instance_id` | The ID of the provisioned EC2 critter instance.     |
| `public_ip`   | The public IP address of the EC2 critter instance.  |

## 🧪 Testing

The tests for this module are designed to be deterministic and run offline, focusing on syntax validation and module integrity without provisioning actual cloud resources.

### Running Tests

1.  Navigate to the utility's root directory:
    ```bash
    cd nightly-ephemeral-critter-corral
    ```
2.  Execute the test script:
    ```bash
    bash tests/test.sh
    ```

### Test Rationale

The `tests/test.sh` script performs the following:
*   Creates a temporary directory.
*   Copies the module's source and a test configuration (`tests/main.tf`) into it.
*   Runs `terraform init -backend=false` to prepare the working directory without attempting to connect to a backend.
*   Executes `terraform validate` against the test configuration. This checks for syntax errors, correct variable usage, and module references.
*   # Mock rationale: The `tests/main.tf` file declares an `aws` provider with dummy credentials (`mock_access_key`, `mock_secret_key`). This allows `terraform validate` to parse the provider block without attempting actual AWS API calls, ensuring the test remains offline and deterministic. While `terraform plan` would typically require valid credentials to resolve remote data (like AMI details), `validate` primarily checks the local configuration's correctness.

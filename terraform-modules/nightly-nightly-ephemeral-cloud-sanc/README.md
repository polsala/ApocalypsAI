# Nightly Ephemeral Cloud Sanctuary

## Summary
This Terraform module provisions a self-destructing, ephemeral AWS cloud sanctuary. It's designed for temporary operations, testing, or demonstrating stateless applications, providing an isolated environment that can be easily created and torn down.

## Whimsical Purpose
In the ever-shifting digital wasteland, sometimes you need a temporary haven, a fleeting mirage of stability. The Ephemeral Cloud Sanctuary offers just that: a safe, isolated space that appears when needed and gracefully vanishes, leaving no trace, only to be reborn anew. Perfect for testing your latest survival contraption without permanent commitment!

## Features
-   **Isolated VPC**: A dedicated network space for your ephemeral resources.
-   **Subnet**: A basic subnet within the VPC.
-   **S3 Bucket**: A private S3 bucket for temporary storage, with a unique, randomized name.
-   **Ephemeral by Design**: Encourages practices where resources are treated as disposable.

## Usage
To use this module, include it in your Terraform configuration and provide the necessary inputs.

### Example `main.tf`
```terraform
provider "aws" {
  region = "us-east-1"
}

module "my_ephemeral_sanctuary" {
  source = "./path/to/nightly-ephemeral-cloud-sanctuary/src"

  project_name    = "my-survival-project"
  aws_region      = "us-east-1"
  vpc_cidr_block  = "10.0.0.0/16"
  subnet_cidr_block = "10.0.1.0/24"
}

output "sanctuary_vpc_id" {
  value = module.my_ephemeral_sanctuary.vpc_id
}

output "sanctuary_bucket_name" {
  value = module.my_ephemeral_sanctuary.s3_bucket_name
}
```

### Inputs
| Name              | Description                                     | Type   | Default         | Required |
|-------------------|-------------------------------------------------|--------|-----------------|----------|
| `project_name`    | A unique name for the project, used in resource naming. | `string` | `"apocalypsai"` | no       |
| `aws_region`      | The AWS region to deploy resources into.        | `string` | `"us-east-1"`   | no       |
| `vpc_cidr_block`  | CIDR block for the VPC.                         | `string` | `"10.0.0.0/16"` | no       |
| `subnet_cidr_block` | CIDR block for the subnet.                      | `string` | `"10.0.1.0/24"` | no       |

### Outputs
| Name             | Description                               | Value |
|------------------|-------------------------------------------|-------|
| `vpc_id`         | The ID of the created VPC.                | `string` |
| `subnet_id`      | The ID of the created subnet.             | `string` |
| `s3_bucket_name` | The name of the created S3 bucket.        | `string` |

## Testing
To run the offline, deterministic tests for this module, navigate to the utility's root directory and execute the `test.sh` script:

```bash
cd nightly-ephemeral-cloud-sanctuary
bash tests/test.sh
```

This script will initialize Terraform, validate the module's configuration, and attempt to generate a destroy plan, ensuring the module is syntactically correct and can be planned for teardown without requiring actual AWS credentials.

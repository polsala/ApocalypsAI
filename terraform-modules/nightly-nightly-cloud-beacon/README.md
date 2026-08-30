# Nightly Cloud Beacon

A Terraform module to deploy a simple, ephemeral cloud beacon (static website) broadcasting a daily 'whisper of hope' or 'survival tip' to the digital ether.

## Summary

In the vast, silent expanse of the digital wasteland, the Nightly Cloud Beacon serves as a whimsical yet practical utility. It provisions a basic static website on AWS S3, configured for public access, to broadcast a configurable message. Think of it as a digital message in a bottle, floating through the cloud currents, a small signal of resilience and connection from the ApocalypsAI network.

Practically, this module demonstrates fundamental AWS S3 static website hosting using Terraform, including bucket creation, website configuration, and a public access policy. It's a great starting point for learning basic IaC for static content.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "my_cloud_beacon" {
  source = "./path/to/nightly-cloud-beacon/src" # Adjust path as needed

  bucket_name_prefix = "my-apocalypsai-signal"
  region             = "us-east-1"
  message_seed       = "The stars still shine, even if we can't see them."
}

output "beacon_url" {
  value = module.my_cloud_beacon.website_endpoint
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to deploy your beacon.

## Inputs

| Name               | Description                                       | Type     | Default                      | Required |
|--------------------|---------------------------------------------------|----------|------------------------------|----------|
| `bucket_name_prefix` | Prefix for the S3 bucket name. A random suffix will be appended. | `string` | `"apocalypsai-beacon"`      | no       |
| `region`           | AWS region to deploy resources.                   | `string` | `"us-east-1"`                | no       |
| `message_seed`     | The core message or seed for the beacon's content. | `string` | `"Hope flickers, but never dies."` | no       |

## Outputs

| Name             | Description                                   |
|------------------|-----------------------------------------------|
| `website_endpoint` | The URL of the deployed static website beacon. |
| `bucket_name`    | The name of the S3 bucket created.            |

## Requirements

*   Terraform CLI (v1.0.0 or higher)
*   AWS Provider configured with appropriate credentials.

## Testing

The tests for this module are implemented as a Bash script that leverages `terraform plan -json` to verify the planned infrastructure without actually deploying resources to AWS. This ensures the tests are deterministic and offline.

To run the tests:

```bash
cd nightly-cloud-beacon/tests
./test.sh
```

The `test.sh` script will:
1.  Initialize Terraform in the test directory.
2.  Run `terraform plan -json` to generate a plan output.
3.  Use `jq` to parse the JSON output and assert the presence and configuration of expected AWS resources (S3 bucket, website configuration, policy, and index.html object) and module outputs.

This approach mocks the AWS environment by analyzing the declarative plan, ensuring the module's structure and resource definitions are correct without incurring cloud costs or requiring live AWS access during testing.

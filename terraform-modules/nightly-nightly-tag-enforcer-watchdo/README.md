# Nightly Tag Enforcer Watchdog

This Terraform module provisions an AWS Config Rule to enforce mandatory tagging on specified AWS resource types. In the post-apocalyptic cloud, proper tagging is crucial for resource identification, cost allocation, security, and overall accountability. This watchdog ensures your scavenged or provisioned resources aren't left untagged in the digital wasteland.

## Features

*   **Mandatory Tag Enforcement**: Defines an AWS Config Rule that checks for the presence of specified tags on selected resource types.
*   **Customizable**: Easily configure the rule name, description, required tags (key-value pairs), and the AWS resource types to monitor.
*   **Compliance Monitoring**: Helps maintain order and accountability in your cloud infrastructure.

## Usage

To use this module, include it in your root Terraform configuration and provide the necessary variables.

```terraform
module "tag_enforcer_watchdog" {
  source = "./modules/nightly-tag-enforcer-watchdog/src" # Adjust path as needed

  rule_name       = "apocalypsai-mandatory-tags"
  rule_description = "Ensure all critical resources have Environment and Owner tags."
  required_tags = {
    "Environment" = "production"
    "Owner"       = "ApocalypsAI-Team"
  }
  resource_types = [
    "AWS::EC2::Instance",
    "AWS::S3::Bucket",
    "AWS::RDS::DBInstance"
  ]
}

output "config_rule_arn" {
  description = "The ARN of the created AWS Config Rule."
  value       = module.tag_enforcer_watchdog.config_rule_arn
}
```

## Module Inputs

| Name             | Description                                                              | Type         | Default                                 | Required |
| :--------------- | :----------------------------------------------------------------------- | :----------- | :-------------------------------------- | :------- |
| `rule_name`      | The name for the AWS Config Rule.                                        | `string`     | `"nightly-required-tags-rule"`        | no       |
| `rule_description` | A description for the AWS Config Rule.                                   | `string`     | `"Ensures specified tags are present on resources." ` | no       |
| `required_tags`  | A map of key-value pairs representing the tags that must be present.     | `map(string)`| `{ "Environment": "production", "Project": "ApocalypsAI" }` | no       |
| `resource_types` | A list of AWS resource types to which the Config Rule applies.           | `list(string)`| `["AWS::EC2::Instance", "AWS::S3::Bucket"]` | no       |

## Module Outputs

| Name              | Description                                |
| :---------------- | :----------------------------------------- |
| `config_rule_arn` | The ARN of the created AWS Config Rule.    |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider `~> 4.0`

## Testing

This module includes a `test_module.sh` script for offline, deterministic validation. It performs syntax checks and simulates a Terraform plan to verify the expected Config Rule configuration without interacting with a live AWS environment.

To run the tests:

```bash
./tests/test_module.sh
```

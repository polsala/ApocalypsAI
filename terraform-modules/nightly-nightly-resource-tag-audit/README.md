# Nightly Resource Tag Audit

## Summary

This Terraform module acts as a digital scavenger, auditing your AWS resources to identify those missing crucial 'survival tags'. In the post-apocalyptic cloud, proper tagging is essential for resource identification, cost allocation, security, and overall wasteland management. This module helps you maintain order by reporting on non-compliant resources, allowing you to quickly address tagging gaps.

## Features

-   **Tag Compliance Check**: Compares existing resource tags against a list of required tag keys and optional values.
-   **Detailed Reporting**: Outputs a list of resources that are missing required tags, specifying which keys are absent or have incorrect values.
-   **Offline Testable**: Designed to be tested without actual AWS API calls by processing mock resource data.

## Usage

To use this module, provide it with a list of resource objects (each containing an ARN and its current tags) and a map of required tags. The module will then output a report of non-compliant resources.

### Example `main.tf`

```terraform
module "survival_tag_audit" {
  source = "./path/to/nightly-resource-tag-audit/src" # Adjust path as necessary

  resources_to_audit = [
    {
      arn  = "arn:aws:s3:::my-critical-cache"
      tags = { "Environment" = "prod", "Owner" = "ApocalypsAI" }
    },
    {
      arn  = "arn:aws:ec2:us-east-1:123456789012:instance/i-0abcdef1234567890"
      tags = { "Environment" = "dev" }
    },
    {
      arn  = "arn:aws:lambda:us-west-2:123456789012:function:my-function"
      tags = {}
    }
  ]

  required_tags = {
    "Environment" = "" # Key must exist, value can be anything
    "Owner"       = "ApocalypsAI" # Key must exist and value must match
    "Project"     = "" # Key must exist, value can be anything
  }
}

output "audit_results" {
  value = module.survival_tag_audit.audit_report
}
```

### Inputs

-   `resources_to_audit` (list(object({arn = string, tags = map(string)}))): A list of resource objects to audit. Each object must have an `arn` (string) and `tags` (map of strings).
-   `required_tags` (map(string)): A map where keys are the required tag names. If a value is an empty string (`""`), only the presence of the key is checked. If a value is specified (e.g., `"ApocalypsAI"`), both the key and its exact value must match.

### Outputs

-   `audit_report` (list(object({arn = string, missing_tag_keys = list(string)}))): A list of resources found to be non-compliant. Each object includes the `arn` of the resource and a `missing_tag_keys` list indicating which required tags were either absent or had incorrect values.

## Development & Testing

This module includes a self-contained test suite to ensure its logic functions correctly without requiring actual AWS credentials or API calls. The tests use mock resource data to simulate various tagging scenarios.

### Running Tests

1.  **Prerequisites**: Ensure you have Terraform CLI and `jq` installed.
2.  Navigate to the `tests/` directory within the module.
3.  Run the test script:
    ```bash
    ./test.sh
    ```

The `test.sh` script will initialize Terraform, apply a test configuration (which only computes outputs based on mock inputs, no cloud resources are provisioned), and then use `jq` to parse the output and assert against expected results. This ensures the module's logic for identifying missing tags is sound.

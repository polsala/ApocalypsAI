# Nightly Whispering Cloud Beacon

This Terraform module provisions a minimal, resilient static website in AWS S3, designed to act as a "whispering beacon" in the digital wasteland. It allows survivors to broadcast messages of hope, critical information, or survival tips across the internet, even when traditional communication channels fail.

The module sets up a publicly accessible S3 bucket configured for static website hosting, uploads an initial HTML message, and applies the necessary bucket policies to ensure global reach.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "whispering_beacon" {
  source = "./terraform-modules/nightly-whispering-cloud-beacon/src" # Adjust path as needed

  bucket_name_prefix  = "my-apocalypsai-signal"
  aws_region          = "us-east-1"
  beacon_message_html = "<h1>The Signal Lives!</h1><p>Find shelter at coordinates X,Y,Z. Supplies available.</p>"
  index_document      = "index.html"
}

output "beacon_url" {
  value       = module.whispering_beacon.beacon_url
  description = "The URL of the deployed static website beacon."
}
```

## Inputs

| Name                | Description                                                              | Type   | Default                  | Required |
|---------------------|--------------------------------------------------------------------------|--------|--------------------------|----------|
| `bucket_name_prefix`| A unique prefix for the S3 bucket name. The full name will be generated. | `string` | `"apocalypsai-beacon"`    | no       |
| `aws_region`        | The AWS region to deploy the beacon.                                     | `string` | `"us-east-1"`            | no       |
| `beacon_message_html`| The HTML content for the initial beacon message.                         | `string` | `"<h1>Whispers of Hope from ApocalypsAI</h1><p>The signal lives on. Stay strong, survivors!</p>"` | no       |
| `index_document`    | The index document for the static website.                               | `string` | `"index.html"`           | no       |

## Outputs

| Name        | Description                                     |
|-------------|-------------------------------------------------|
| `beacon_url`| The URL of the deployed static website beacon.  |
| `bucket_name`| The name of the S3 bucket created for the beacon.|

## Requirements

-   Terraform CLI (v1.0.0+)
-   AWS CLI configured with appropriate credentials (for actual deployment)
-   `jq` (for running tests)

## Development & Testing

The module includes a self-contained test suite that uses `terraform validate` and `terraform plan` to ensure correctness without deploying actual resources.

To run tests:

```bash
cd terraform-modules/nightly-whispering-cloud-beacon
./tests/test_module.sh
```

**Mock rationale for tests:** The tests leverage Terraform's built-in validation and plan generation capabilities. `terraform validate` checks syntax and configuration, while `terraform plan` generates an execution plan. By inspecting this plan's JSON output with `jq`, we can deterministically verify that the module *intends* to create the correct AWS resources with the expected properties, all without making any actual API calls to AWS. The `-backend=false` flag for `terraform init` further ensures no state is managed, keeping tests isolated and offline.

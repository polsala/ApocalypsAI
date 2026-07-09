# Nightly Cloud Sanctuary Beacon

A Terraform module to deploy a resilient, static "sanctuary beacon" webpage in the cloud, signaling safety or distress. This beacon is designed for high availability and minimal cost, using AWS S3 for static website hosting.

## Features

*   **Static Website Hosting**: Leverages AWS S3 for a highly available and scalable static webpage.
*   **Customizable Message**: Display any message to the community (e.g., "All Clear!", "Distress Signal", "Rendezvous Point").
*   **Optional DNS Integration**: Automatically create a Route 53 A record for a custom domain.
*   **Minimal Cost**: S3 static websites are extremely cost-effective.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

```terraform
module "sanctuary_beacon" {
  source = "./path/to/nightly-cloud-sanctuary-beacon/src" # Adjust path as needed

  region              = "us-east-1"
  beacon_message      = "All Clear! The Oasis is Safe."
  create_dns_record   = true
  domain_name         = "your-apocalypse-domain.com" # Replace with your domain
  subdomain           = "sanctuary"
}

output "beacon_url" {
  value = module.sanctuary_beacon.beacon_url
}
```

## Inputs

| Name                | Description                                                              | Type    | Default             | Required |
| :------------------ | :----------------------------------------------------------------------- | :------ | :------------------ | :------- |
| `region`            | AWS region to deploy the beacon.                                         | `string`| `"us-east-1"`       | no       |
| `beacon_message`    | The message to display on the sanctuary beacon webpage.                  | `string`| `"All Clear! Sanctuary Found."` | no       |
| `create_dns_record` | Whether to create a Route 53 A record for the beacon.                    | `bool`  | `false`             | no       |
| `domain_name`       | The domain name for the Route 53 record (e.g., `example.com`). Required if `create_dns_record` is `true`. | `string`| `"example.com"`     | no       |
| `subdomain`         | The subdomain for the Route 53 record (e.g., `beacon`). Required if `create_dns_record` is `true`. | `string`| `"beacon"`          | no       |

## Outputs

| Name         | Description                                        |
| :----------- | :------------------------------------------------- |
| `beacon_url` | The URL of the deployed sanctuary beacon webpage.  |

## Running Tests

The tests for this module perform static validation and plan generation without deploying actual resources.

```bash
cd nightly-cloud-sanctuary-beacon/tests
./validate.sh
```

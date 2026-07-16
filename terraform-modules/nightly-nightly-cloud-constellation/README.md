# Nightly Cloud Constellation Mapper

This whimsical Terraform module helps you map your cloud resources to the cosmos! It provisions an AWS S3 bucket and tags it with a chosen constellation name and celestial coordinates, turning your infrastructure into a personal star chart.

## Features

*   Provisions an AWS S3 bucket.
*   Applies custom tags for `Constellation` and `CelestialCoordinates`.
*   Outputs a "star map entry" for your newly charted cloud resource.
*   A fun way to organize and identify resources in a celestial theme.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "my_celestial_bucket" {
  source = "./nightly-cloud-constellation-mapper" # Adjust path if not local
  
  bucket_name_prefix    = "apocalypsai-data"
  constellation_name    = "Orion's Belt Storage"
  celestial_coordinates = "RA 05h 35m 17s, Dec -05d 22m 28s"
  region                = "us-east-1"
}

output "my_bucket_constellation_entry" {
  value = module.my_celestial_bucket.constellation_map_entry
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to provision your celestial bucket.

## Inputs

| Name                  | Description                                    | Type     | Default | Required |
| :-------------------- | :--------------------------------------------- | :------- | :------ | :------- |
| `bucket_name_prefix`  | A prefix for the S3 bucket name.               | `string` | `null`  | yes      |
| `constellation_name`  | The whimsical name of the constellation.       | `string` | `null`  | yes      |
| `celestial_coordinates` | The celestial coordinates for your resource. | `string` | `null`  | yes      |
| `region`              | The AWS region to deploy the S3 bucket in.     | `string` | `null`  | yes      |

## Outputs

| Name                        | Description                                     |
| :-------------------------- | :---------------------------------------------- |
| `s3_bucket_id`              | The ID of the created S3 bucket.                |
| `s3_bucket_arn`             | The ARN of the created S3 bucket.               |
| `constellation_map_entry`   | A formatted string representing the star map entry. |

## Requirements

*   Terraform `~> 1.0`
*   AWS Provider configured with appropriate credentials.

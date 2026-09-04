# Nightly Cloud Beacon

## Summary
A Terraform module to provision a highly available static website beacon for community messages on AWS S3 and CloudFront.

## Description
In the post-apocalyptic digital wasteland, reliable communication is paramount. The Nightly Cloud Beacon provides a robust, low-cost, and highly available static website infrastructure on AWS. It's perfect for broadcasting emergency messages, sharing vital community updates, or simply hosting a digital "light in the darkness." This module sets up an S3 bucket for content storage, configures it for static website hosting, and deploys an AWS CloudFront distribution for global content delivery with HTTPS.

## Usage
To use this module, include it in your Terraform configuration and provide the required variables. You will need AWS credentials configured for Terraform.

```terraform
module "community_beacon" {
  source = "./path/to/nightly-cloud-beacon/src"

  bucket_name_prefix = "my-community-beacon"
  index_document     = "index.html"
  error_document     = "error.html"
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Production"
  }
}

output "beacon_website_url" {
  description = "The URL of the static website beacon."
  value       = module.community_beacon.cloudfront_domain_name
}

output "s3_website_endpoint" {
  description = "The S3 static website endpoint (for direct access, less secure)."
  value       = module.community_beacon.website_endpoint
}
```

After configuring, run `terraform init`, `terraform plan`, and `terraform apply`.

## Inputs

| Name                 | Description                                     | Type     | Default        | Required |
|----------------------|-------------------------------------------------|----------|----------------|----------|
| `bucket_name_prefix` | A unique prefix for the S3 bucket name.         | `string` | n/a            | yes      |
| `index_document`     | The default document for the website.           | `string` | `"index.html"` | no       |
| `error_document`     | The error document for the website.             | `string` | `"error.html"` | no       |
| `tags`               | A map of tags to apply to the created resources. | `map`    | `{}`           | no       |

## Outputs

| Name                       | Description                                     |
|----------------------------|-------------------------------------------------|
| `website_endpoint`         | The S3 static website endpoint URL.             |
| `cloudfront_domain_name`   | The CloudFront distribution domain name.        |
| `cloudfront_zone_id`       | The CloudFront distribution hosted zone ID.     |

## Testing
To run the module's self-contained tests, navigate to the `tests/` directory and execute the `run_tests.sh` script.

```bash
cd terraform-modules/nightly-cloud-beacon/tests
./run_tests.sh
```

This script will initialize Terraform, validate the module's configuration, and perform a dry run (`terraform plan`) to ensure syntax and variable resolution are correct without provisioning actual cloud resources.

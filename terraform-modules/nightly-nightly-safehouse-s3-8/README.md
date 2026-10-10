Nightly Safehouse S3 Terraform Module

This module creates an AWS S3 bucket configured for a post‑apocalyptic safe‑house:
  * Versioning enabled so you never lose a supply list
  * Server‑side encryption (AES‑256) for data at rest
  * Lifecycle rule that expires objects older than 30 days (to keep the bucket tidy)
  * Optional tags for cost allocation

Usage:
  1. Add the module to your Terraform configuration:
     module "safehouse" {
       source      = "./terraform-modules/nightly-safehouse-s3"
       bucket_name = "my‑safehouse‑supplies"
       tags = {
         Environment = "post‑apocalypse"
         Owner       = "survivors"
       }
     }

  2. Run the usual Terraform workflow:
     terraform init -backend=false
     terraform apply -auto-approve

Variables:
  bucket_name (string, required) – Name of the S3 bucket. Must be globally unique.
  tags        (map(string), optional) – Key/value pairs to tag the bucket.

Outputs:
  bucket_id  – The ID of the created bucket.
  bucket_arn – The ARN of the created bucket.

The module does not create any IAM policies; you must grant the necessary permissions to the executing role.

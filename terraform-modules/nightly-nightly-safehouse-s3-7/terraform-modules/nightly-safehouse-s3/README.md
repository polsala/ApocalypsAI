Nightly Safehouse S3 Terraform Module

Overview:
This module creates an AWS S3 bucket configured for durability and security, ideal for storing critical post‑apocalyptic data. It enables versioning, server‑side encryption (AES‑256), a lifecycle rule that expires objects after 30 days, and adds a whimsical tag "radiation_level" with a random value between 1 and 10.

Usage Example:
module "safehouse" {
  source      = "./terraform-modules/nightly-safehouse-s3"
  bucket_name = "my-safehouse-bucket"
}

Inputs:
- bucket_name (string, required): Name of the S3 bucket to create.

Outputs:
- bucket_id: ID of the created bucket.
- bucket_arn: ARN of the created bucket.

Testing:
Run the validation script:
./tests/test_validate.sh

Note:
The module uses the AWS and Random providers. Ensure they are available in your Terraform environment.

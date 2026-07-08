# Mock rationale: This test configuration is designed to be run with `terraform validate` and `terraform plan`.
# These commands perform offline syntax checking and plan generation without requiring actual AWS credentials or resource provisioning.
# By instantiating the module with dummy values, we ensure that the module's HCL is valid, variables are correctly defined and used,
# and outputs are accessible, all without incurring cloud costs or deploying real infrastructure.
# The `null_resource` is a common pattern in Terraform testing to ensure a successful plan without creating actual resources.

# Configure a dummy AWS provider. This is for syntax validation only and does not require actual credentials for `terraform validate`.
# For `terraform plan`, it would attempt to connect, but we are primarily testing `validate` offline.
provider "aws" {
  region = "us-east-1" # A valid region is needed for schema validation
  # access_key = "mock_access_key" # Mocked credentials for plan, if needed, but not for validate
  # secret_key = "mock_secret_key" # Mocked credentials for plan, if needed, but not for validate
}

module "test_beacon" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-beacon"
  content_file_path  = "beacon_message.html" # Refers to the file in the src directory
  region             = "us-east-1"
}

# This null_resource ensures that the module's outputs can be accessed, further validating the module.
resource "null_resource" "output_check" {
  triggers = {
    cloudfront_url = module.test_beacon.cloudfront_domain_name
    s3_endpoint    = module.test_beacon.s3_bucket_website_endpoint
  }

  # This provisioner will not run during `terraform plan` or `terraform validate`
  # but its presence ensures the syntax is correct for accessing outputs.
  provisioner "local-exec" {
    command = "echo 'CloudFront URL: ${self.triggers.cloudfront_url}' && echo 'S3 Endpoint: ${self.triggers.s3_endpoint}'"
    # Mock rationale: This command is a placeholder to demonstrate output access. It will not execute during offline validation.
    # It confirms that the output variables are correctly defined and exposed by the module.
  }
}

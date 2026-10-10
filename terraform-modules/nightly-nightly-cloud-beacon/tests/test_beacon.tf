# Mock rationale: This test configuration is designed to be run offline using 'terraform validate'.
# It ensures the module's syntax is correct and its variables are properly defined and used,
# without requiring actual AWS credentials or deploying real cloud resources.
# The 'null_resource' is used to simulate a dependency or action that would typically occur
# during a real deployment, making the test more robust in checking module interaction,
# but it performs no actual cloud operations.

provider "aws" {
  region = "us-east-1" # Mock region for validation
  # No actual credentials needed for 'terraform validate'
}

module "test_beacon_instance" {
  source = "../src" # Path to the module being tested

  bucket_name_prefix = "test-apocalypsai-beacon"
  content_message    = "Test message for the ApocalypsAI beacon."
  aws_region         = "us-east-1"
}

resource "null_resource" "validate_outputs" {
  # Mock rationale: This null_resource simulates a check on the module's outputs.
  # It doesn't perform any actual action but ensures the outputs are accessible
  # and correctly formatted according to the module's definition.
  triggers = {
    cloudfront_url = module.test_beacon_instance.cloudfront_domain_name
    s3_endpoint    = module.test_beacon_instance.s3_bucket_website_endpoint
    s3_id          = module.test_beacon_instance.s3_bucket_id
  }

  provisioner "local-exec" {
    command = "echo 'CloudFront URL: ${self.triggers.cloudfront_url}' && echo 'S3 Endpoint: ${self.triggers.s3_endpoint}'"
    # Mock rationale: The command itself is a no-op for testing purposes,
    # but it demonstrates that the outputs are resolvable.
  }
}

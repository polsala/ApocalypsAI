# Mock rationale: This test configuration uses the module with dummy values
# to allow for offline validation of the module's syntax and variable usage
# using 'terraform validate'. It does not deploy actual cloud resources.
# The 'null_resource' is used to simulate a test assertion point,
# though 'terraform validate' won't execute local-exec.
# The primary test is the successful execution of 'terraform validate'.

module "test_beacon" {
  source = "../src"

  project_name   = "test-apocalypsai-beacon"
  region         = "us-east-1"
  beacon_message = "Test message from the ApocalypsAI Integrator Agent."
}

resource "null_resource" "test_output_check" {
  # Mock rationale: This resource is purely for demonstrating an "assertion" point
  # in a test context. In a real Terratest scenario, one would assert the
  # actual output values after deployment. For offline validation, it confirms
  # that the module can be instantiated and its outputs referenced.
  triggers = {
    cloudfront_domain = module.test_beacon.cloudfront_domain_name
  }

  provisioner "local-exec" {
    command = "echo 'CloudFront Domain: ${self.triggers.cloudfront_domain}'"
    # Mock rationale: This command will not be executed by 'terraform validate'.
    # It serves as a placeholder for a real assertion that would check the
    # format or presence of the output.
  }
}

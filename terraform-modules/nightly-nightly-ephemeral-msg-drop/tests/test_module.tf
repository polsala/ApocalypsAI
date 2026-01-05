# Mock rationale: This test uses `terraform validate` for syntax and basic configuration checks.
# It also uses `null_resource` with `local-exec` to simulate rendering the user_data script
# and checking its content, without actually provisioning AWS resources. This allows for offline,
# deterministic verification of the script's logic. The provider block uses dummy credentials
# to satisfy `terraform validate` without making actual AWS API calls.

# Define a local provider block for the test module to satisfy terraform validate
# This provider block is purely for validation and will not be used for actual deployment
# when running `terraform validate` or `terraform plan` on the test module itself.
provider "aws" {
  region = "us-east-1"
  # Mock rationale: These are dummy credentials to satisfy the provider configuration
  # for `terraform validate`. They are not used for actual AWS API calls during offline testing.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_session_token"
}

module "test_message_drop" {
  source = "../" # Referencing the parent module
  # Override defaults for testing specific scenarios
  aws_region            = "us-east-1"
  ami_id                = "ami-00000000000000000" # A dummy AMI for validation, must be a valid format
  instance_type         = "t3.nano"
  message_content       = "Test message for self-destruct sequence."
  self_destruct_minutes = 5
  key_pair_name         = "test-key" # Can be empty if not used
}

resource "null_resource" "check_user_data_script" {
  # This resource exists purely for testing the user_data content offline.
  # It uses a local-exec provisioner to simulate the script content.
  triggers = {
    user_data_content = module.test_message_drop.user_data_script_content
  }

  provisioner "local-exec" {
    command = <<EOT
      echo "${self.triggers.user_data_content}" > user_data_test.sh
      if ! grep -q "Test message for self-destruct sequence." user_data_test.sh; then
        echo "Error: Message content not found in user_data_test.sh"
        exit 1
      fi
      if ! grep -q "sudo shutdown -h +5 &" user_data_test.sh; then
        echo "Error: Shutdown command not found or incorrect in user_data_test.sh"
        exit 1
      fi
      rm user_data_test.sh
      echo "User data script content check passed."
    EOT
    interpreter = ["bash", "-c"]
    working_dir = path.module
  }
}

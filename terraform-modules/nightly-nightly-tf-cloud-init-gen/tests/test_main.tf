provider "template" {}

module "test_module" {
  source = ".."

  instance_name    = "TestServer"
  banner_message   = "Testing the fun banner!"
  user_data_script = "echo 'This is a test script.' > /tmp/test.txt"
  package_list     = ["htop", "vim"]
}

output "test_user_data" {
  value = module.test_module.user_data
}

# Mock rationale: The template provider is used for rendering, and its behavior is deterministic.
# No external API calls or complex state management are involved, making direct mocking unnecessary.
# The test asserts the output of the rendered template based on provided inputs.

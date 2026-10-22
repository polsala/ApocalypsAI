provider "random" {}

module "test_module" {
  source = ".."

  server_name = "TestServer"
  boot_script = "echo 'Hello, World!' > /tmp/hello.txt"
}

output "generated_user_data" {
  value = module.test_module.user_data
}

# Mock rationale: The 'random' provider is used for generating a random suffix. 
# In a real Terraform run, this would interact with a random number generator. 
# For testing, we don't need to mock the provider itself, but rather ensure the template renders correctly.
# The 'templatefile' function is deterministic for a given input.

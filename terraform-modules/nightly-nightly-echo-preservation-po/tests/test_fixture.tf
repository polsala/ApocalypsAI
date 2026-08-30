# Mock rationale: This file acts as a test fixture, calling the module
# with specific inputs to verify its syntax and structure during `terraform validate`.
# It does not provision real resources, making the test deterministic and offline.

module "test_echo_chamber" {
  source = "../src"

  name_prefix           = "test-echo"
  environment           = "staging"
  retention_days_standard = 7
  retention_days_glacier  = 14
  tags = {
    "Project" = "ApocalypsAI"
    "Purpose" = "Test"
  }
}

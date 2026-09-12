provider "aws" {
  region = "us-east-1" # Mock region for validation
  # Mock rationale: Terraform validate and plan do not require actual AWS credentials
  # if the resources are well-defined and don't rely on data sources that fetch live state.
  # For this module, all inputs are variables, so a dummy provider configuration is sufficient.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_session_token"
}

module "hibernation_test" {
  source = "../src"

  name_prefix       = "test-hibernation"
  region            = "us-east-1"
  resource_tags     = {
    "Environment" = "dev",
    "Project"     = "ApocalypsAI"
  }
  stop_cron_schedule  = "cron(0 22 * * ? *)"
  start_cron_schedule = "cron(0 8 * * ? *)"
}

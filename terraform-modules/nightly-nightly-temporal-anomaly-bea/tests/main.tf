# Mock rationale: This file serves as a mock instantiation of the module
# for offline validation and planning. It does not provision real resources.
# It ensures the module's syntax is correct and its variables are properly defined.

provider "aws" {
  region = "us-east-1" # Mock rationale: Required by Terraform for provider configuration, but no actual AWS calls are made during validate/plan.
  # Mock rationale: Dummy credentials for offline validation.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_anomaly_beacon" {
  source = "../src" # Path to the module being tested

  project_name       = "TestProject"
  environment        = "test"
  anomaly_pattern    = "TEST_ANOMALY_PATTERN"
  alarm_threshold    = 2
  notification_email = "test@example.com"
  aws_region         = "us-east-1"
}

output "test_log_group_name" {
  value = module.test_anomaly_beacon.log_group_name
}

output "test_sns_topic_arn" {
  value = module.test_anomaly_beacon.sns_topic_arn
}

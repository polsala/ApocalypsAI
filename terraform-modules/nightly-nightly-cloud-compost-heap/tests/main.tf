provider "aws" {
  region = "us-east-1"
  # Mock rationale: For `terraform validate`, no actual AWS credentials are required.
  # The provider block is needed for HCL parsing, but no API calls are made.
  # For `terraform plan` or `apply`, credentials would be needed, but these tests
  # are designed to be offline and deterministic, focusing on syntax and module interface.
  # We use a dummy access key and secret key to satisfy provider configuration requirements
  # without needing actual valid credentials for offline validation.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "cloud_compost_heap_test" {
  source  = "../src"

  project_name                      = "TestCompost"
  region                            = "us-east-1"
  enable_s3_compost_bucket          = true
  enable_ebs_stale_volume_detector  = true
  enable_ec2_stale_instance_detector = true
  stale_instance_age_days           = 60

  tags = {
    TestEnv = "True"
  }
}

module "cloud_compost_heap_minimal_test" {
  source  = "../src"

  project_name                      = "MinimalCompost"
  region                            = "us-west-2"
  enable_s3_compost_bucket          = false
  enable_ebs_stale_volume_detector  = false
  enable_ec2_stale_instance_detector = false

  tags = {
    Minimal = "True"
  }
}

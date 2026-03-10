provider "aws" {
  region = "us-east-1" # Mock region for plan-time validation
  # No actual credentials needed for 'terraform plan'
}

module "test_beacon" {
  source      = "../src"
  beacon_name = "test-chronal-rift"
  aws_region  = "us-east-1"
  log_level   = "DEBUG"
}

output "test_s3_bucket_name" {
  value = module.test_beacon.s3_bucket_name
}

output "test_lambda_function_name" {
  value = module.test_beacon.lambda_function_name
}

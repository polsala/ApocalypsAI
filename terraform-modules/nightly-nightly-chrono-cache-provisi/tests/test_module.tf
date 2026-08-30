provider "aws" {
  region = "us-east-1"
  # Mock rationale: This provider block is for local testing of the module.
  # It does not require actual AWS credentials for `terraform validate` or `terraform plan`
  # if the AWS provider is already cached locally by `terraform init`. For `terraform plan`,
  # it simulates a dry run without creating real resources. In a real deployment,
  # the root module consuming this module would configure the AWS provider.
}

module "test_chrono_cache" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-cache"
  expiration_days    = 14
  aws_region         = "us-east-1"
}

output "test_bucket_id" {
  value = module.test_chrono_cache.bucket_id
}

output "test_bucket_arn" {
  value = module.test_chrono_cache.bucket_arn
}

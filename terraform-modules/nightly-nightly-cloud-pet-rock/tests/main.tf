provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline testing, we don't actually need AWS credentials.
  # Terraform plan will validate syntax and module structure without API calls.
  # If actual deployment was needed, credentials would be required.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_pet_rock_basic" {
  source               = "../"
  bucket_name_prefix   = "test-pet-rock-basic"
  enable_website_hosting = false
  aws_region           = "us-east-1"
}

module "test_pet_rock_website" {
  source               = "../"
  bucket_name_prefix   = "test-pet-rock-website"
  enable_website_hosting = true
  aws_region           = "us-east-1"
}

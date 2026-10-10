# Mock rationale: This test configuration uses the module with dummy values
# to ensure the module's HCL syntax is valid and well-formed.
# It does not provision actual cloud resources.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Mock rationale: Dummy credentials for offline validation.
  # These are not used for actual provisioning during 'terraform validate'.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_celestial_bucket" {
  source = "../src" # Path to the module under test
  
  bucket_name_prefix    = "test-apocalypsai"
  constellation_name    = "Andromeda Galaxy Cluster"
  celestial_coordinates = "RA 00h 42m 44s, Dec +41d 16m 09s"
  region                = "us-east-1"
}

output "test_s3_bucket_id" {
  value = module.test_celestial_bucket.s3_bucket_id
}

output "test_constellation_map_entry" {
  value = module.test_celestial_bucket.constellation_map_entry
}

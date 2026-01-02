# Example: Basic Chaos Monkey Configuration

# Configure providers for testing
provider "aws" {
  region  = "us-east-1"
  alias   = "test"
  
  # Skip actual AWS calls for testing
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}

# Create some test resources for the chaos monkey to target
resource "aws_instance" "test_instance" {
  provider = aws.test
  
  # This is a mock instance for testing
  # In real usage, you'd have actual AWS instances
  count         = 3
  instance_type = "t3.micro"
  ami           = "ami-0abcdef1234567890"
  
  tags = {
    Name = "chaos-test-instance-${count.index}"
    ChaosEligible = "true"
  }
}

resource "aws_s3_bucket" "test_bucket" {
  provider = aws.test
  
  bucket = "chaos-test-bucket-${random_pet.bucket_suffix.id}"
  
  tags = {
    Name = "Chaos Test Bucket"
    ChaosEligible = "true"
  }
}

resource "random_pet" "bucket_suffix" {
  length = 4
}

# Chaos Monkey Module Configuration
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos for this test environment
  enabled = true
  
  # 20% chance of destroying a resource
  destruction_probability = 0.2
  
  # Target these resource types
  target_resources = [
    "aws_instance",
    "aws_s3_bucket"
  ]
  
  # Exclude the bucket suffix resource
  excluded_resources = [
    "random_pet.bucket_suffix"
  ]
  
  # Maximum 2 destructions per run
  max_destructions_per_run = 2
  
  # Only run on weekdays
  chaos_schedule = "weekdays"
  
  # Dry run mode for safety
  dry_run = true
  
  # Minimum age of 1 hour before targeting
  min_resource_age_hours = 1
  
  # Chaos tags filter
  chaos_tags = {
    ChaosEligible = "true"
  }
  
  # Backup before destruction
  backup_before_destruction = true
}

# Output the chaos report
output "chaos_report" {
  value = module.chaos_monkey.chaos_status
}

output "safety_warnings" {
  value = module.chaos_monkey.safety_warnings
}

output "eligible_resources" {
  value = module.chaos_monkey.eligible_resources
}

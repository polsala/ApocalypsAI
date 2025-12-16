# Test configuration for chaos garden module

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

# Test module configuration
module "chaos_garden_test" {
  source = "../"

  environment = "test"
  region      = "us-west-2"

  chaos_scenarios = [
    "network_latency",
    "resource_deletion",
    "service_disruption"
  ]

  max_concurrent_experiments = 2
  experiment_duration        = "10m"
  rollback_enabled          = true

  enable_monitoring = true
  alert_email       = "test@example.com"

  tags = {
    Environment = "test"
    Team        = "QA"
    Project     = "ChaosEngineering"
    Terraform   = "true"
  }
}

# Test resources
resource "aws_instance" "test_target" {
  count         = 1
  ami           = "ami-0abcdef1234567890" # Replace with a valid AMI ID
  instance_type = "t3.micro"
  subnet_id     = "subnet-12345" # Replace with a valid subnet ID

  tags = {
    Name           = "test-chaos-target"
    Environment    = "test"
    ChaosTarget    = "true"
    Terraform      = "true"
  }
}

# Test outputs
output "test_chaos_garden_url" {
  value       = module.chaos_garden_test.chaos_garden_url
  description = "Test chaos garden URL"
}

output "test_experiment_bucket" {
  value       = module.chaos_garden_test.experiment_results_bucket
  description = "Test experiment results bucket"
}

output "test_sns_topic" {
  value       = module.chaos_garden_test.sns_topic_arn
  description = "Test SNS topic ARN"
}

output "test_lambda_arn" {
  value       = module.chaos_garden_test.lambda_function_arn
  description = "Test Lambda function ARN"
}

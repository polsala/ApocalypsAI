# Example: Basic Chaos Garden Setup

provider "aws" {
  region = "us-west-2"
}

module "chaos_garden" {
  source = "../.."

  # Environment configuration
  environment = "staging"
  region      = "us-west-2"

  # Chaos scenarios to enable
  chaos_scenarios = [
    "network_latency",
    "resource_deletion",
    "service_disruption"
  ]

  # Safety controls
  max_concurrent_experiments = 2
  experiment_duration        = "15m"
  rollback_enabled          = true

  # Monitoring and alerts
  enable_monitoring = true
  alert_email       = "ops@example.com"

  # Tags
  tags = {
    Team      = "SRE"
    Project   = "ChaosEngineering"
    Terraform = "true"
  }
}

# Example: Tag instances for chaos experiments
resource "aws_instance" "chaos_target" {
  count         = 2
  ami           = "ami-0abcdef1234567890" # Replace with a valid AMI ID
  instance_type = "t3.micro"
  subnet_id     = "subnet-12345" # Replace with a valid subnet ID

  tags = {
    Name           = "chaos-target-${count.index + 1}"
    Environment    = "staging"
    ChaosTarget    = "true"
    Terraform      = "true"
  }
}

output "chaos_garden_dashboard_url" {
  value       = "https://${module.chaos_garden.chaos_garden_url}"
  description = "URL to access the chaos garden dashboard"
}

output "experiment_results_bucket" {
  value       = module.chaos_garden.experiment_results_bucket
  description = "S3 bucket containing experiment results"
}

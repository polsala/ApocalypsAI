# Mock rationale: This configuration is used to test the module's syntax and variable
# definitions without requiring actual AWS credentials or resources.
# It ensures the module can be initialized and planned successfully.
# The AWS provider block is included to satisfy the module's provider requirements,
# but no actual AWS API calls will be made during 'terraform validate' or 'terraform plan'
# in a CI/CD environment without proper AWS credentials configured.
# The outputs will be empty or default values in such a scenario, which is expected
# for an offline structural test.

provider "aws" {
  region = "us-east-1" # Dummy region for validation
  # No credentials provided for offline testing
}

module "ebs_decay_detector" {
  source = "../src"

  region = "us-west-2"
  tags_filter = {
    "Environment" = "dev"
    "Project"     = "apocalypsai"
  }
}

output "test_unattached_ids" {
  value = module.ebs_decay_detector.unattached_ebs_volume_ids
}

output "test_unattached_count" {
  value = module.ebs_decay_detector.unattached_ebs_volumes_count
}

output "test_unattached_details" {
  value = module.ebs_decay_detector.unattached_ebs_volumes_details
}

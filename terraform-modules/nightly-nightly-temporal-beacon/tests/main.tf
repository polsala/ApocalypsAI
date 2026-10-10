provider "aws" {
  region = "us-east-1"
  # Mock rationale: The provider block is required for Terraform syntax validation,
  # but no actual AWS resources will be provisioned during the offline test.
  # Access keys are omitted as they are not needed for 'terraform plan'.
}

module "temporal_beacon_test" {
  source = "../src"

  aws_region          = "us-east-1"
  vpc_id              = "vpc-mockid1234567890"
  public_subnet_ids   = [
    "subnet-mockid1234567890a",
    "subnet-mockid1234567890b"
  ]
  instance_type       = "t2.nano"
  desired_capacity    = 1
  beacon_message      = "Test Beacon Signal!"
}

output "test_alb_dns" {
  value = module.temporal_beacon_test.alb_dns_name
  description = "DNS name of the test ALB."
}

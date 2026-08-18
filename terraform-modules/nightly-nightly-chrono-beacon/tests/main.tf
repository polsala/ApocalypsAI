provider "aws" {
  region = "us-east-1" # Mock rationale: Required by Terraform for plan, but no actual API calls made.
}

module "chrono_beacon_test" {
  source = "../src"

  region          = "us-east-1"
  instance_type   = "t2.micro"
  vpc_id          = "vpc-0abcdef1234567890" # Mock rationale: Dummy VPC ID for plan validation.
  subnet_ids      = ["subnet-0123456789abcdef", "subnet-0fedcba9876543210"] # Mock rationale: Dummy subnet IDs.
  desired_capacity = 1
  min_size         = 1
  max_size         = 1
  ami_id           = "ami-0abcdef1234567890" # Mock rationale: Dummy AMI ID for plan validation.
}

output "beacon_url_test" {
  value = module.chrono_beacon_test.beacon_url
}

output "lb_dns_name_test" {
  value = module.chrono_beacon_test.load_balancer_dns_name
}

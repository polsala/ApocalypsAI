# Mock rationale: This provider block uses dummy credentials and region
# to allow `terraform init` and `terraform plan` to run successfully
# without requiring actual AWS authentication or deploying real resources.
# It simulates the presence of an AWS environment for validation purposes.
provider "aws" {
  region     = "us-east-1" # A common region for testing
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_session_token" # For temporary credentials
}

# Mock rationale: This data source is used to simulate the existence of a default VPC
# in the mock AWS environment. Terraform needs this to validate the security group
# resource, even if no real VPC is being queried.
data "aws_vpc" "default" {
  default = true
}

module "test_outpost" {
  source = "../src" # Path to the module being tested

  aws_region      = "us-east-1"
  instance_type   = "t2.micro"
  ami_id          = "ami-053b0d53c279acc90" # Example: Amazon Linux 2 AMI (HVM), SSD Volume Type
  key_name        = "test-key-pair"
  allowed_cidrs   = ["192.168.1.0/24"]
  outpost_name    = "TestTemporalAnomalyDetector"
}

output "test_public_ip" {
  value = module.test_outpost.public_ip
}

output "test_instance_id" {
  value = module.test_outpost.instance_id
}

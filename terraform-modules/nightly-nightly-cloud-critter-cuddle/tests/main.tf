# Mock rationale: This test configuration uses dummy values for AWS resources
# and relies on `terraform plan` to validate syntax and module structure
# without requiring actual AWS credentials or provisioning real infrastructure.
# The `source = "../src"` points to the module locally.

module "test_critter_cuddler" {
  source = "../src"

  name                = "test-critter"
  instance_type       = "t2.micro"
  ami_id              = "ami-0abcdef1234567890" # Dummy AMI ID
  key_name            = "test-key-pair"         # Dummy Key Pair
  vpc_id              = "vpc-0123456789abcdef0" # Dummy VPC ID
  subnet_id           = "subnet-0fedcba9876543210" # Dummy Subnet ID
  sleep_cron_expression = "cron(0 22 * * ? *)"
  wake_cron_expression  = "cron(0 8 * * ? *)"

  tags = {
    Environment = "Test"
    ManagedBy   = "ApocalypsAI"
  }
}

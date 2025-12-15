provider "aws" {
  region = "us-east-1"
  # Mock rationale: The provider block is required for Terraform to validate syntax,
  # but no actual AWS credentials are needed for `terraform validate` or `terraform plan`
  # when using mocks or asserting against the plan output.
  # We use a dummy region and rely on the test script to prevent actual apply.
  access_key = "mock_access_key" # Mock rationale: Dummy value for validation
  secret_key = "mock_secret_key" # Mock rationale: Dummy value for validation
}

module "ephemeral_garden_test" {
  source = "../" # Referencing the parent module

  name_prefix                 = "test-garden"
  ami_id                      = "ami-0abcdef1234567890"
  instance_type               = "t2.micro"
  subnet_id                   = "subnet-test-123"
  vpc_security_group_ids      = ["sg-test-456"]
  s3_object_expiration_days   = 1
  db_allocated_storage        = 10
  db_engine                   = "postgres"
  db_engine_version           = "13.4"
  db_instance_class           = "db.t2.micro"
  db_name                     = "testdb"
  db_username                 = "testuser"
  db_password                 = "TestPassword123!"
  db_subnet_group_name        = "test-db-subnet-group"
}

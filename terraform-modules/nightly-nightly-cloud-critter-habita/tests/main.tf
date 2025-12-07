module "critter_habitat_test" {
  source = "../src"

  region        = "us-east-1"
  critter_name  = "TestCritter"
  instance_type = "t2.nano"
  ami_id        = "ami-0abcdef1234567890" # Mock AMI ID for deterministic planning
  key_name      = "test-key"
}

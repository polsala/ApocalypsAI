module "test_critter_zone" {
  source = "../src"

  project_name = "test-apocalypsai"
  environment  = "test"
  critter_name = "TestCritter"
  aws_region   = "us-east-1"
}

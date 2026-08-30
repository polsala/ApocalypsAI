module "constellation_mapper" {
  source = "../"

  aws_region               = "us-east-1"
  project_name             = "test-apocalypsai"
  environment              = "test"
  project_tag_key          = "TestProject"
  environment_tag_key      = "TestEnv"
  scan_schedule_expression = "rate(1 hour)"
}

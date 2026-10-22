provider "aws" {
  region = "us-east-1" # Mock region for plan, actual deployment would use a real one
}

module "test_rift_monitor" {
  source = "../src"

  prefix         = "test-apocalypsai"
  s3_bucket_name = "test-apocalypsai-rift-monitor-code-bucket"
  schedule_expression = "rate(1 minute)"
  stable_time = "2023-10-27T10:00:00Z"
  rift_threshold_seconds = 600 # 10 minutes for testing
}

output "lambda_name" {
  value = module.test_rift_monitor.lambda_function_name
}

output "event_rule_name" {
  value = module.test_rift_monitor.cloudwatch_event_rule_name
}

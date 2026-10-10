# Mock rationale: This test configuration uses the module with default values
# to ensure it can be initialized, validated, and planned without errors.
# It does not provision actual AWS resources, making it deterministic and offline
# after initial provider download.
# The 'null_resource' is a common pattern in Terraform testing to provide a target
# for 'terraform apply' if needed, but here it's just to ensure the module is
# correctly referenced and its outputs are accessible for potential assertions
# in a shell script.

module "test_relay" {
  source = "../../src"

  queue_name = "test-whisperwind-queue"
  topic_name = "test-whisperwind-topic"
  tags = {
    Environment = "Test"
  }
}

output "test_sqs_queue_url" {
  value = module.test_relay.sqs_queue_url
}

output "test_sns_topic_arn" {
  value = module.test_relay.sns_topic_arn
}

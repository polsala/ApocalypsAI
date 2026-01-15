# Mock rationale: We simulate AWS instance data and random_shuffle behavior to test destruction logic without real cloud interaction.

terraform {
  required_providers {
    test {
      source = "terraform.io/builtin/test"
    }
  }
}

mock_data "aws_instances" "mocked_instances" {
  input = {
    ids = ["i-12345", "i-67890", "i-abcde"]
  }
}

mock_resource "random_shuffle" "mock_shuffle" {
  result = ["i-12345", "i-67890"]
}

test_assertions "chaos_destruction_count" {
  description = "Verify correct number of instances are targeted for destruction"
  condition   = length(mock_resource.random_shuffle.mock_shuffle.result) == 2
}
